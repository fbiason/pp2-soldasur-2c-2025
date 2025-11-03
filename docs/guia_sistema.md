# Guía técnica del sistema: Experto + Chatbot (RAG)

Esta guía explica en detalle cómo funciona el sistema híbrido de SOLDASUR: el sistema experto (IA simbólica basada en reglas) y el chatbot (RAG con LLM), cómo se relacionan los archivos, y los conceptos técnicos clave para estudiar y extender la solución.


## Visión general

El proyecto combina dos enfoques de IA complementarios:
- Sistema experto (IA simbólica): flujo guiado con árbol de decisiones y reglas de cálculo para dimensionar calefacción (piso radiante, radiadores y calderas).
- Chatbot con RAG (Retrieval-Augmented Generation): recuperación semántica de productos y generación de respuestas usando un LLM local (Ollama), especializado para recomendar productos del catálogo PEISA.

Arquitectura a alto nivel:
1) Front-end web (HTML + JS + Tailwind): `app/soldasur2025.html`, `app/soldasur.js`, `app/modules/**`
2) Sistema experto (reglas + cálculos + plantillas): `app/modules/expertSystem/*`, base de conocimiento `app/peisa_advisor_knowledge_base.json`
3) Chatbot RAG (FAISS + embeddings + LLM): `app/modules/chatbot/*`, `app/rag_engine_v2.py`, embeddings en `embeddings/`
4) Orquestación y API (FastAPI): `app/main.py`, `app/orchestrator.py`, utilidades en `app/app.py`


## Mapa de archivos y responsabilidades

- Front-end
  - `app/soldasur2025.html`: página principal con el widget de chat.
  - `app/soldasur.js`: UI del widget; integra menús, modos y navegación.
  - `app/modules/expertSystem/expertSystem.js`: flujo guiado del experto en el cliente (UX y cálculos básicos para demo).
  - `app/modules/chatbot/chatbot.js`: integración del chat con Ollama desde el navegador y renderizado de productos.

- Sistema experto (backend Python)
  - `app/modules/expertSystem/expert_engine.py`: motor experto asincrónico; interpreta la base de conocimiento, procesa entradas, ejecuta cálculos y puede enriquecer con RAG.
  - `app/peisa_advisor_knowledge_base.json`: árbol de decisión (nodos de preguntas, respuestas, cálculos).
  - `app/app.py`: helpers históricos compatibles con `main.py` (reemplazo de variables, cálculos, filtrado, etc.).
  - `app/modules/expertSystem/product_loader.py`: carga dinámica de productos desde Excel/CSV (mock) y construye diccionarios de radiadores, calderas y piso radiante.
  - `app/modules/expertSystem/models.py`: expone `RADIATOR_MODELS` y recarga.

- Chatbot + RAG
  - `app/modules/chatbot/llm_wrapper.py`: wrapper de Ollama con prompt de sistema (rol de "Soldy") y post-procesamiento (brevedad, sanitización de precios, etc.).
  - `app/rag_engine_v2.py`: motor RAG completo (SentenceTransformers + FAISS + LLM); búsqueda vectorial, filtrado por contexto del experto y respuesta final.
  - `ingest/ingest.py`: pipeline para generar embeddings FAISS y base SQLite desde un CSV.
  - `query/query.py`: consulta al índice FAISS con filtros semánticos y estructurados.

- API y orquestación
  - `app/main.py`: API FastAPI (endpoints /start, /reply, /ask) y servido de `soldasur2025.html`.
  - `app/orchestrator.py`: orquestador inteligente para combinar modos EXPERTO, RAG e HÍBRIDO según intención.

- Datos y modelos
  - `data/products_catalog.json`: catálogo de productos PEISA (usado por RAG y front-end).
  - `embeddings/products.faiss` y `embeddings/products.db`: índice vectorial FAISS y catálogo relacional.
  - `configs/params.yaml`: ejemplo de parámetros (no crítico para ejecución actual).


## Sistema experto (IA simbólica por reglas)

El sistema experto guía al usuario mediante nodos (preguntas/respuestas/cálculos) definidos en `app/peisa_advisor_knowledge_base.json`.

Tipos de nodos principales:
- pregunta: muestra texto y puede tener `opciones` (ramas) o requerir `entrada_usuario`.
- calculo: ejecuta expresiones declarativas en `acciones` para derivar nuevas variables y salta al siguiente nodo.
- respuesta: devuelve un texto (con variables interpoladas) y puede ser final o con nuevas `opciones`.
- opciones_dinamicas: genera opciones en tiempo de ejecución con base en variables calculadas.

Archivo clave: `expert_engine.py`
- `ExpertEngine.process(...)` avanza el estado: lee el nodo actual, aplica la selección/entrada, ejecuta cálculos y retorna el siguiente mensaje.
- `ExpertEngine._perform_calculation(...)` ejecuta `acciones` con un entorno seguro y funciones auxiliares expuestas (p. ej. `filter_radiators`, `recommend_boiler`, `recommend_radiator_from_catalog`).
- Interpolación de variables: `{{var}}` y soporte Jinja2 (`Template.render`).
- Enriquecimiento RAG opcional por nodo: `_enrich_with_rag` consulta al motor RAG para aportar contexto adicional si `enrich_with_rag: true`.

Ejemplo de flujo (radiadores):
1) `dimensiones_radiador` pide `largo`, `ancho`, `alto`.
2) `nivel_aislacion` y preferencias de `tipo_instalacion`, `estilo_diseno`, `color_preferido`.
3) Nodo `recomendar_modelos` (tipo calculo):
   - `volumen = largo * ancho * alto`
   - `carga_termica = volumen * (50 | 40 | 30)` según aislación
   - `modelos_recomendados = filter_radiators(...)` usando catálogo dinámico
   - `modelos_recomendados_formateados = format_radiator_recommendations(...)`
4) `mostrar_recomendaciones`: muestra texto listo para el usuario.

Catálogo dinámico: `product_loader.py`
- Lee `data/raw/Products_db.xlsx` (o `data/processed/products_mock.csv` como fallback) y genera estructuras para radiadores, calderas y piso radiante.
- Para radiadores, determina instalación, estilo, colores y un `coeficiente` (según modelo 350/500/600/700/800/1000) para estimar potencia efectiva.
- Expone accesos:
  - `get_radiators_dict()` → `RADIATOR_MODELS`
  - `get_all_products()` → lista unificada de todos los productos cargados.

Interpolación y plantillas:
- Los textos de respuesta/pregunta admiten `{{variable}}` y también expresiones Jinja2 (por ejemplo: `{{potencia_requerida|round(0)}}`).

Seguridad del evaluador:
- Las expresiones de `acciones` se ejecutan con `eval` restringiendo `__builtins__` y exponiendo solo funciones auxiliares controladas (no se permite acceso a filesystem ni imports arbitrarios).


## Chatbot con RAG (Retrieval-Augmented Generation)

Objetivo: responder en lenguaje natural sobre necesidades del usuario recomendando productos concretos del catálogo.

Componentes:
- Embeddings: `SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')` para `rag_engine_v2.py` y `distiluse-base-multilingual-cased-v2` en el pipeline de `ingest.py`/`query.py`.
- Índice FAISS: `IndexFlatIP` con vectores normalizados (similaridad coseno). Archivos: `embeddings/products.faiss`, `embeddings/products.db`.
- LLM local (Ollama): modelo por defecto `llama3.2:3b`. Wrapper: `OllamaLLM` en `llm_wrapper.py`.

Flujo RAG (`RAGEngineV2.query`):
1) Búsqueda vectorial: `search_products(question, top_k)` → textos de productos a vector, búsqueda FAISS por similitud.
2) Filtrado contextual: si hay `expert_context`, se filtra por familia o potencia aproximada.
3) Generación: se llama a `llm.generate(question, relevant_products)` con un prompt de sistema diseñado para vender/recomendar.
4) Respuesta: se retorna `answer`, `products` (top 2), `sources` y metadatos de modo.

Wrapper del LLM (`llm_wrapper.py`):
- Prompt de sistema fuerte: obliga a mencionar al menos 1 producto por nombre y a responder con 2-3 oraciones, en tono argentino.
- Manejo de precios: detección de consultas de precios y respuesta estándar pidiendo localidad (Río Grande / Ushuaia).
- Post-procesamiento: brevedad, sanitización de precios, punto final consistente.

Front-end del chatbot (`modules/chatbot/chatbot.js`):
- Carga catálogo `data/products_catalog.json` en el navegador.
- Filtra productos relevantes en el cliente para construir un system prompt específico por consulta.
- Llama a la API REST de Ollama (`/api/chat` local) y presenta la respuesta.
- Detecta productos mencionados en texto y renderiza tarjetas clicables ("Ver"/"Consultar").


## Orquestador de conversación (modos EXPERTO / RAG / HÍBRIDO)

Archivo: `app/orchestrator.py`
- `IntentClassifier`: clasifica intención con patrones (cálculo guiado, pregunta libre, búsqueda de producto, cambio de modo, aclaración en medio del flujo).
- `UnifiedContext`: estado unificado (nodo experto actual, variables, historial RAG, preferencias).
- `ConversationOrchestrator`: enruta cada mensaje al motor correspondiente y construye respuestas híbridas si aplica.

Principios de diseño:
- Si el usuario expresa “quiero calcular/dimensionar…”, prioriza EXPERTO.
- Si pregunta “¿qué es/ventajas/diferencias…?”, prioriza RAG.
- En modo HÍBRIDO combina: contesta con RAG y sugiere próximo paso del EXPERTO basado en variables faltantes.

Nota: La UI actual usa una versión cliente del flujo experto y del chatbot. El orquestador y los endpoints están listos para consolidar el flujo 100% por backend si se desea.


## API y páginas

- `app/main.py` (FastAPI)
  - GET `/` → sirve `app/soldasur2025.html`.
  - POST `/start` → inicia conversación del experto (estado por `conversation_id`).
  - POST `/reply` → procesa opción/inputs, resuelve nodo, devuelve siguiente mensaje.
  - GET `/ask?question=...` → demo RAG rápido usando `query/search_filtered` + `llm_wrapper.answer`.
  - GET `/health` → estado del servicio.

- Front-end
  - La página carga los módulos JS (`expertSystem.js`, `chatbot.js`, `soldasur.js`) y muestra el widget flotante. El chatbot llama directo a Ollama local vía fetch.


## Pipeline de datos y embeddings

- `ingest/ingest.py` toma un CSV tipo `data/processed/products_mock.csv` y genera:
  - SQLite `embeddings/products.db` con la tabla `products` (campos: type, family, model, description, power_w, etc.).
  - Índice FAISS `embeddings/products.faiss` con embeddings normalizados (coseno ≈ producto interno).

- `query/query.py` carga el índice y la DB, embebe la consulta, busca top-K, y aplica filtros adicionales:
  - Detección de requerimiento de potencia en W (regex de "17 kW", "17000 W", etc.)
  - Filtro por tipo (por ejemplo caldera) y por potencia mínima.

Consejos RAG:
- Ajustar top_k y el modelo de embeddings según cobertura/precisión.
- Mantener los textos de producto ricos en señal semántica (features, ventajas, aplicaciones) para mejorar recuperación.


## Conceptos técnicos clave

- IA simbólica (sistema experto): reglas declarativas + árbol de decisión. Ventajas: determinismo, explicabilidad, control de negocio. Ideal para cálculos y formularios guiados.
- RAG (Retrieval-Augmented Generation): combina recuperación semántica (FAISS + embeddings) con generación (LLM). Ventajas: respuestas actualizadas al catálogo, factualidad y foco.
- Embeddings: representación densa de textos; similaridad coseno para medir cercanía semántica. Modelos multilingües elegidos para español.
- FAISS: librería de búsqueda vectorial eficiente. `IndexFlatIP` con vectores L2-normalizados permite ranking por coseno.
- Prompt engineering: prompt de sistema fuerte para forzar mención de productos, estilo y longitud; post-procesado para consistencia.
- Modo híbrido: usa señales de ambos mundos (variables presentes/faltantes del experto + intención en lenguaje natural) para encaminar al usuario.


## Cómo extender o modificar

- Agregar reglas/pasos al experto:
  - Editar `app/peisa_advisor_knowledge_base.json` agregando nodos (pregunta/respuesta/cálculo) y enlazando `siguiente`.
  - Para cálculos, añadir expresiones en `acciones` (p. ej. `nuevavar = largo * ancho`). Las funciones auxiliares disponibles están en `expert_engine.py` y `app/app.py`.

- Actualizar catálogo de productos:
  - Fuente dinámica (Excel): actualizar `data/raw/Products_db.xlsx`. El loader reconstruye estructuras; o exportar a JSON con `ProductLoader.export_to_json`.
  - Para RAG, regenerar embeddings desde CSV con `ingest/ingest.py` y reemplazar `embeddings/*.faiss`/`*.db`.

- Ajustar RAG/LLM:
  - Cambiar modelo de embeddings en `rag_engine_v2.py`.
  - Cambiar el modelo de Ollama o el prompt en `llm_wrapper.py` (variable `self.system_prompt`).

- Integrar 100% backend:
  - Usar `ConversationOrchestrator` desde endpoints dedicados (no solo UI cliente). Mantiene contexto cross-modo por `conversation_id`.


## Ejecución local (referencia)

Requisitos comunes:
- Python 3.10+
- Paquetes de `requirements.txt` (incluye fastapi, uvicorn, sentence-transformers, faiss-cpu, pandas, etc.).
- Ollama instalado y corriendo en `http://127.0.0.1:11434` con el modelo `llama3.2:3b` descargado.

Pasos (opcionales):
1) Generar embeddings desde CSV (si querés reindexar):
   - Ejecutar `ingest/ingest.py data/processed/products_mock.csv`.
2) Iniciar API:
   - `uvicorn app.main:app --reload --port 8000`
3) Abrir `http://localhost:8000/` y usar el widget de Soldy.

Nota: El chatbot del front-end llama directo a Ollama desde el navegador; asegurate de que el CORS y el host estén accesibles.


## Buenas prácticas y edge cases

- Validación numérica: los nodos `entrada_usuario` convierten "4,5" a float con `.` y capturan ValueError.
- Potencias y unidades: el sistema maneja W ↔ kcal/h con factor 0.859845; sé consistente al mostrar.
- Catálogo vacío: `chatbot.js` y `expert_engine.py` contemplan fallbacks (mensajes claros si no hay datos).
- Seguridad eval: no expongas funciones peligrosas en el entorno de `eval`. Mantener `__builtins__` bloqueado.
- Latencia RAG: el primer uso de `SentenceTransformer` carga el modelo; podés precargar en arranque para mejorar UX.


## Resumen

- El sistema experto resuelve cálculos determinísticos y guía al usuario paso a paso con reglas explícitas.
- El chatbot con RAG entiende lenguaje natural y recomienda productos concretos del catálogo con ayuda del LLM.
- La orquestación permite combinar ambos enfoques para ofrecer una experiencia flexible, precisa y explicable.

Con esta guía podés estudiar el diseño, modificar reglas y catálogo, y extender el RAG/LLM para nuevos casos de uso.
