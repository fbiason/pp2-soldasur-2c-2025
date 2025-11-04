# SoldaSur IA Chatbot

Asistente para asesoramiento en calefacción (PEISA) que combina un sistema experto (IA simbólica por reglas) y un chatbot con RAG + LLM local (Ollama).

## Características

- Modo Chat (RAG + LLM): recomendaciones en lenguaje natural de productos PEISA, mencionando al menos un producto por nombre.
- Modo Experto (reglas): cálculo guiado de potencia para piso radiante, radiadores y calderas con resultados explicables.
- Catálogo actualizable por scraping del sitio de PEISA.
- 100% local (Ollama); sin dependencias de APIs externas.

## Inicio rápido

Requisitos
- Python 3.10+
- Ollama instalado y corriendo: https://ollama.ai
- Modelo LLM local:
   ```bash
   ollama pull llama3.2:3b
   ```

Instalación
```bash
# Crear y activar entorno (Windows)
python -m venv venv
venv\Scripts\activate

# Dependencias
pip install -r requirements.txt
```

Ejecución
- Opción A (frontend estático):
   ```bash
   cd app
   python -m http.server 8000
   # Abrir http://localhost:8000/soldasur2025.html
   ```
- Opción B (backend FastAPI):
   ```bash
   python -m uvicorn app.main:app --reload
   # Abrir http://localhost:8000/
   ```

## Arquitectura (resumen)

- Front-end: `app/soldasur2025.html`, `app/soldasur.js`
   - UI del widget con 3 entradas: Guíame (experto), Tengo una pregunta (chat), Buscar productos.
- Sistema Experto: `app/modules/expertSystem/expert_engine.py` + `app/peisa_advisor_knowledge_base.json`
   - Nodos de preguntas/cálculos/respuestas; funciones auxiliares de recomendación.
- Chatbot RAG: `app/modules/chatbot/llm_wrapper.py`, `app/modules/chatbot/rag_engine_v2.py`
   - Recuperación con FAISS + embeddings y generación con Ollama.
- Scraping: `app/modules/scraping/product_scraper.py`
   - Actualiza `data/products_catalog.json` (descripciones, ventajas, URL).
- API/Orquestación: `app/main.py`, `app/orchestrator.py`
   - Endpoints de conversación y clasificador de intención (híbrido listo para consolidar).

## Documentación

- Glosario: `docs/GLOSARIO.md`
- Chatbot: `docs/CHATBOT.md`
- Sistema Experto: `docs/SISTEMA_EXPERTO.md`
- Scraping: `docs/SCRAPING.md`
- Manual para escalar: `docs/MANUAL_ESCALAMIENTO.md`

## Estructura del proyecto (completa)

```
LICENSE
Makefile
README.md
requirements.txt
__pycache__/
app/
   app.py
   ESTRUCTURA.txt
   main.py
   models.py
   orchestrator.py
   peisa_advisor_knowledge_base.json
   soldasur.css
   soldasur.js
   soldasur.js.backup
   soldasur2025.html
   __pycache__/
   img/
   modules/
      chatbot/
         chatbot.js
         llm_wrapper.py
         rag_engine_v2.py
         __pycache__/
      expertSystem/
         expert_engine.py
         expertSystem.js
         models.py
         product_loader.py
         README.md
         __pycache__/
      scraping/
         inspect_peisa.py
         product_scraper.py
configs/
   params.yaml
data/
   products_catalog.json
embeddings/
   products.faiss
images/
ingest/
   ingest.py
models/
notebooks/
   exploration.ipynb
query/
   query.py
   __pycache__/
scripts/
   test_embeddings.py
docs/
   GLOSARIO.md
   CHATBOT.md
   SISTEMA_EXPERTO.md
   SCRAPING.md
   MANUAL_ESCALAMIENTO.md
```

## Tareas comunes

- Actualizar catálogo por scraping:
   ```bash
   python app/modules/scraping/product_scraper.py
   ```
- Regenerar embeddings (opcional):
   ```bash
   python ingest/ingest.py data/processed/products_mock.csv
   ```
- Probar consulta RAG filtrada:
   ```bash
   python query/query.py "¿Tienen calderas de más de 17000 W?"
   ```

## Troubleshooting

- “No responde el chatbot”: verificar que Ollama esté activo en `http://127.0.0.1:11434` y el modelo descargado.
- “Sin productos”: correr el scraper o validar `data/products_catalog.json`.
- Respuestas largas: bajar `num_predict` o reforzar post-procesado en `llm_wrapper.py`.

## Equipo 2 – PP2 SOLDASUR 2C 2025

Integrantes: Cussi Nicolás · Biason Franco · Bolaña Silvia · Luna Luciano

Metodología: Ágil (Scrum) con sprints, plan/desarrollo/cierre; gestión en Trello y GitHub.

## Licencia

Este proyecto se distribuye bajo los términos de la licencia incluida en `LICENSE`.