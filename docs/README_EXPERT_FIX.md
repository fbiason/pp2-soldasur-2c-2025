## README — Cambios aplicados y explicación del Sistema Experto

Fecha: 18 de octubre de 2025

Este documento resume los cambios realizados para corregir un fallo en el flujo guiado del sistema experto y describe, a alto nivel, cómo funciona el motor experto y cómo probar la solución localmente.

---

## Resumen del problema

Antes del arreglo, al iniciar el flujo guiado ("Guíame en un cálculo") y elegir el tipo de calefacción, si el usuario seleccionaba "Radiadores" o "Calderas" la interfaz cliente interceptaba esa opción y mostraba el catálogo de productos en vez de avanzar por el flujo del sistema experto. El sistema funcionaba correctamente para "Piso radiante" porque el flujo y los nodos estaban implementados en la base de conocimiento.

Esto causaba que únicamente "Piso radiante" ejecutase los cálculos esperados y los otros dos tipos quedaran atascados mostrando el catálogo.

---

## Cambios realizados

1) Front-end (`app/soldasur.js`)
- Restricción en la lógica de navegación por catálogo: ahora la selección de una categoría de producto (p. ej. "Radiadores", "Calderas") se trata como navegación al catálogo *solo* si el usuario está en el menú principal (condición `conversationStep === 0`). Esto evita que las respuestas dentro del flujo experto sean interpretadas como intención de ver productos.
- Mapeo estándar de la variable: cuando el usuario responde la pregunta "¿Qué tipo de calefacción deseas calcular?" la selección se guarda tanto en `userInputs.tipo` (compatibilidad hacia atrás) como en `userInputs.tipo_calefaccion` y en `contextData.tipo_calefaccion`. El backend (`expert_engine` y `rag_engine_v2`) usa `tipo_calefaccion` para filtrar y enrutar adecuadamente.

Archivos modificados:
- `app/soldasur.js` — cambio principal en `handleOptionClick(...)` y asignación de `tipo_calefaccion`.

2) Documentación rápida
- Se añadió una nota en la documentación de Quickstart indicando la variable estándar `tipo_calefaccion` (si corresponde). También se creó este README con la explicación extendida.

---

## Por qué esta corrección resuelve el problema

El fallo no estaba en el motor experto (que ya contiene nodos para Radiadores y Calderas en `peisa_advisor_knowledge_base.json`), sino en la UI que interceptaba selecciones. Al garantizar que la navegación por catálogo solo se realice desde el menú principal, las opciones respondidas en el contexto del flujo experto se procesan por el motor experto y se ejecutan los nodos de cálculo y respuesta correspondientes.

Además, el uso de la clave `tipo_calefaccion` unifica el campo que el backend espera para filtrar productos o elegir cálculos (esto ya se manejaba parcialmente en `expert_engine.py` y `rag_engine_v2.py`).

---

## Cómo funciona el Sistema Experto (visión general)

Componentes principales:
- Base de conocimiento: `app/peisa_advisor_knowledge_base.json` — grafo de nodos con `id`, `pregunta`, `opciones`, `tipo` y nodos `calculo` que contienen `acciones` y `parametros`.
- Motor experto: `app/expert_engine.py` — carga la base, procesa nodos, evalúa cálculos (eval de expresiones controladas) y puede enriquecer respuestas con un motor RAG.
- Orquestador: `app/orchestrator.py` — decide si enrutar a modo experto, RAG o híbrido según la intención.
- Interfaz: `app/soldasur.js` — UI conversacional que guía al usuario y llama al motor experto o al RAG según el modo.

Flujo de uso (simplificado):
1. Usuario inicia el flujo guiado (modo experto) desde la UI.
2. La UI muestra la pregunta inicial (tipo de calefacción).
3. La selección se guarda en el contexto (`tipo_calefaccion`) y el motor experto avanza por nodos definidos en la base.
4. Si el nodo es de tipo `calculo`, el motor ejecuta las `acciones` (expresiones) y guarda resultados en el contexto.
5. El motor produce una respuesta formateada (tipo `respuesta`) o pregunta siguiente. Opcionalmente, se hace enriquecimiento RAG si el nodo lo solicita.

Tipos de nodos (en la base):
- `pregunta`: muestra texto y opciones o entrada de usuario.
- `entrada_usuario`: espera números o múltiples inputs; el motor valida y guarda en `context`.
- `calculo`: contiene `parametros` y `acciones`; las acciones son expresiones evaluadas en un contexto controlado para producir resultados (p. ej. `carga_termica = superficie * potencia_m2[zona_geografica]`).
- `respuesta`: texto final o intermedio que puede incluir variables interpoladas.

Helpers y funciones relevantes disponibles al evaluar expresiones:
- `filter_radiators(...)` — filtra modelos según preferencias y carga térmica.
- `format_radiator_recommendations(models, heat_load)` — formatea recomendaciones.
- `recommend_boiler(power_required_w, boiler_type, catalog)` — recomienda calderas según potencia.
- `recommend_floor_heating_kit(surface_m2, catalog)` — selecciona kits de piso radiante adecuados.
- `recommend_radiator_from_catalog(power_required_w, catalog)` — busca radiadores en el catálogo.
- `load_product_catalog(catalog_path)` — carga catálogo JSON si se necesita.

Seguridad: las expresiones en nodos se evalúan con un contexto limitado (`eval` con builtins restringidos y un diccionario local con las funciones listadas arriba). Aún así, si ampliás la base, revisá que las expresiones sean seguras.

---

## Pasos para probar localmente (rápido)

1. Activar entorno Python y dependencias (si corresponde):
```bash
python -m venv .venv
source .venv/Scripts/activate    # en Windows con bash
pip install -r requirements.txt
```
2. Servir la carpeta `app/` y abrir `soldasur2025.html`:
```bash
cd app
python -m http.server 8000
# Abrir http://localhost:8000/soldasur2025.html
```
3. O ejecutar con live server:
Instalar la extension y en el archivo soldasur2025.html hacer click derecho en el codigo y seleccionar "open with live server". 


4. Flujo de prueba (end-to-end):
- Iniciar chat → seleccionar "Guíame en un cálculo" → cuando pregunte "¿Qué tipo de calefacción deseas calcular?" seleccionar "Radiadores" o "Calderas".
- Comprobar que el chat pide superficie, zona y aislación, que ejecuta el cálculo y muestra recomendaciones (en vez del catálogo).
4. Verificar menú principal: volver al menú principal y seleccionar "Buscar productos" → "Radiadores" para comprobar que ahí sí muestra el catálogo.

---

