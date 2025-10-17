# Sistema Experto - SOLDASUR

## 📋 Descripción General

El **Sistema Experto** es un motor basado en reglas que guía al usuario paso a paso en el cálculo y dimensionamiento de sistemas de calefacción. Utiliza una base de conocimiento estructurada en formato JSON que define un árbol de decisiones conversacional.

## 🏗️ Arquitectura del Sistema

### Componentes Principales

1. **ExpertEngine** (`app/expert_engine.py`)
   - Motor principal del sistema experto
   - Procesa el flujo conversacional basado en nodos
   - Ejecuta cálculos automáticos
   - Soporta enriquecimiento con RAG

2. **Base de Conocimiento** (`app/peisa_advisor_knowledge_base.json`)
   - Árbol de decisiones en formato JSON
   - Define preguntas, opciones y cálculos
   - Estructura de nodos interconectados

3. **Orchestrator** (`app/orchestrator.py`)
   - Coordina entre el sistema experto y el RAG
   - Clasifica intenciones del usuario
   - Maneja modos de conversación (experto, RAG, híbrido)

4. **API FastAPI** (`app/main.py`)
   - Endpoints REST para interacción
   - Gestión de conversaciones
   - Integración con interfaz web

## 🔄 Flujo de Funcionamiento

### 1. Inicialización
```
Usuario → /start → Orchestrator → ExpertEngine → Nodo "inicio"
```

### 2. Procesamiento de Interacciones
```
Usuario selecciona opción/ingresa datos
    ↓
Orchestrator clasifica intención
    ↓
ExpertEngine procesa entrada
    ↓
Actualiza contexto (variables)
    ↓
Avanza al siguiente nodo
    ↓
Retorna pregunta/resultado
```

### 3. Tipos de Nodos

#### **Nodo de Pregunta con Opciones**
```json
{
  "id": "inicio",
  "pregunta": "¿Qué tipo de calefacción desea calcular?",
  "opciones": [
    { "texto": "Piso radiante", "siguiente": "superficie_piso" },
    { "texto": "Radiadores", "siguiente": "objetivo_radiadores" }
  ]
}
```

#### **Nodo de Entrada de Usuario**
```json
{
  "id": "superficie_piso",
  "pregunta": "¿Cuál es la superficie útil (en m²)?",
  "tipo": "entrada_usuario",
  "variable": "superficie",
  "siguiente": "tipo_piso"
}
```

#### **Nodo de Cálculo**
```json
{
  "id": "calculo_piso_radiante",
  "tipo": "calculo",
  "parametros": {
    "potencia_m2": { "norte": 100, "sur": 125 }
  },
  "acciones": [
    "carga_termica = superficie * potencia_m2[zona_geografica]",
    "longitud_total = superficie * densidad_caño"
  ],
  "siguiente": "resultado_piso_radiante"
}
```

#### **Nodo de Respuesta**
```json
{
  "id": "resultado_piso_radiante",
  "tipo": "respuesta",
  "texto": "PISO RADIANTE:\n- Superficie: {{superficie}} m²\n- Potencia: {{carga_termica}} W",
  "opciones": [
    { "texto": "Calcular radiadores", "siguiente": "objetivo_radiadores" }
  ]
}
```

## 🎯 Funcionalidades Clave

### Gestión de Variables
- **Contexto persistente**: Mantiene variables durante toda la conversación
- **Reemplazo de variables**: Usa `{{variable}}` en textos
- **Soporte Jinja2**: Expresiones complejas en plantillas

### Cálculos Automáticos
- **Expresiones matemáticas**: Evalúa fórmulas en nodos de cálculo
- **Funciones especiales**:
  - `filter_radiators()`: Filtra modelos según preferencias
  - `format_radiator_recommendations()`: Formatea recomendaciones
  - `ceil()`: Redondeo hacia arriba

### Enriquecimiento RAG
- **Información adicional**: Complementa respuestas con datos del RAG
- **Contexto inteligente**: Usa variables del experto para consultas RAG

## 🚀 Cómo Ejecutar el Sistema

### Requisitos Previos
```bash
# Instalar dependencias
pip install -r requirements.txt
```

### Opción 1: Ejecutar el Servidor Completo (RECOMENDADO)
```bash
# Desde la raíz del proyecto
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Opción 2: Ejecutar directamente main.py
```bash
# Desde la raíz del proyecto
python app/main.py
```

### Opción 3: Usando PowerShell (Windows)
```powershell
# Navegar al directorio del proyecto
cd c:\Users\Franco\Desktop\proyecto_final_soldasur\soldasur_2025\pp2-soldasur-2c-2025

# Activar entorno virtual si existe
# .\venv\Scripts\Activate.ps1

# Ejecutar servidor
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Verificar que el Sistema Está Corriendo
Al ejecutar, deberías ver en la consola:
```
🚀 INICIANDO SISTEMA UNIFICADO PEISA - SOLDASUR
📋 Inicializando Expert Engine...
✅ Expert Engine listo
✅ RAG Engine V2 listo
🔗 Configurando dependencias mutuas...
✅ Dependencias configuradas
🎭 Inicializando Orquestador...
✅ Orquestador listo
🎉 SISTEMA UNIFICADO LISTO

📡 Servidor disponible en: http://localhost:8000
📚 Documentación API: http://localhost:8000/docs
💬 Chat Unificado: http://localhost:8000/
```

## 🌐 Acceso a la Interfaz

Una vez ejecutado el servidor, accede a:

- **Chat Unificado**: http://localhost:8000/
- **Documentación API**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📡 Endpoints API

### POST /start
Inicia una nueva conversación
```json
{
  "conversation_id": "user123",
  "mode": "expert"  // "expert", "rag", o "hybrid"
}
```

**Respuesta:**
```json
{
  "conversation_id": "user123",
  "node_id": "inicio",
  "type": "question",
  "text": "¿Qué tipo de calefacción desea calcular?",
  "options": ["Piso radiante", "Radiadores"],
  "mode": "expert",
  "mode_label": "🤖 Modo Experto"
}
```

### POST /reply
Envía respuesta del usuario
```json
{
  "conversation_id": "user123",
  "message": "",
  "option_index": 0,  // Para seleccionar opciones
  "input_values": {"value": "50"}  // Para entrada numérica
}
```

**Respuesta:**
```json
{
  "conversation_id": "user123",
  "node_id": "superficie_piso",
  "type": "question",
  "text": "¿Cuál es la superficie útil a calefaccionar?",
  "input_type": "number",
  "input_label": "Ingrese el valor"
}
```

### GET /health
Verifica estado del sistema
```json
{
  "status": "ok",
  "service": "PEISA - SOLDASUR S.A",
  "expert_engine": "ready",
  "rag_engine": "ready",
  "orchestrator": "ready"
}
```

## 🎭 Modos de Operación

### 1. Modo Experto (🤖)
- **Flujo guiado paso a paso**
- Preguntas estructuradas
- Cálculos automáticos
- Recomendaciones precisas
- Ideal para usuarios que necesitan guía

**Activar:**
```json
POST /start
{
  "conversation_id": "user123",
  "mode": "expert"
}
```

### 2. Modo RAG (💬)
- **Chat libre con IA**
- Búsqueda semántica
- Respuestas generativas
- Consulta de productos
- Ideal para preguntas abiertas

**Activar:**
```json
POST /start
{
  "conversation_id": "user123",
  "mode": "rag"
}
```

### 3. Modo Híbrido (⚡)
- **Combina ambos sistemas**
- Sugerencias inteligentes
- Transición fluida entre modos
- Aclaraciones durante flujo guiado
- Modo por defecto

**Activar:**
```json
POST /start
{
  "conversation_id": "user123",
  "mode": "hybrid"
}
```

## 🔍 Ejemplo de Flujo Completo

### Cálculo de Piso Radiante

**Paso 1: Inicio**
```
Usuario: [Inicia conversación]
Sistema: "¿Qué tipo de calefacción desea calcular?"
Opciones: ["Piso radiante", "Radiadores"]
```

**Paso 2: Selección**
```
Usuario: Selecciona opción 0 (Piso radiante)
Sistema: "¿Cuál es la superficie útil a calefaccionar (en m²)?"
```

**Paso 3: Superficie**
```
Usuario: Ingresa "50"
Sistema: "¿Qué tipo de pavimento tiene el ambiente?"
Opciones: ["Cerámica", "Madera", "Alfombra"]
```

**Paso 4: Tipo de piso**
```
Usuario: Selecciona opción 0 (Cerámica)
Sistema: "¿En qué zona del país se encuentra?"
Opciones: ["Zona Centro/Norte", "Zona Sur"]
```

**Paso 5: Zona**
```
Usuario: Selecciona opción 1 (Zona Sur)
Sistema: [Ejecuta cálculos automáticamente]
```

**Paso 6: Resultado**
```
Sistema: "PISO RADIANTE:
- Superficie: 50 m²
- Potencia estimada: 6250 W
- Caños: 250 m
- Circuitos sugeridos: 3 de hasta 100 m

¿Deseás calcular también RADIADORES para otro ambiente?"
Opciones: ["Sí", "No"]
```

### Cálculo de Radiadores

**Paso 1: Objetivo**
```
Sistema: "¿Cuál es el principal objetivo para los radiadores?"
Opciones: ["Calefacción principal", "Complementaria", "Secado de toallas"]
```

**Paso 2: Dimensiones**
```
Usuario: Selecciona "Calefacción principal"
Sistema: "Indique las dimensiones del ambiente (largo, ancho y alto en metros):"
Inputs: [largo, ancho, alto]
```

**Paso 3: Ingreso de dimensiones**
```
Usuario: largo=5, ancho=4, alto=2.7
Sistema: "Nivel de aislación térmica del ambiente:"
Opciones: ["Alta", "Media", "Baja"]
```

**Paso 4-7: Preferencias**
```
Usuario selecciona:
- Aislación: "Media"
- Instalación: "Superficie"
- Estilo: "Moderno"
- Color: "Blanco"
```

**Paso 8: Cálculo y Recomendación**
```
Sistema: [Ejecuta cálculos]
- Volumen = 5 × 4 × 2.7 = 54 m³
- Carga térmica = 54 × 40 = 2160 kcal/h
- Filtra modelos compatibles

Sistema: "Basado en tus necesidades, te recomendamos:

1. TROPICAL 500
   - Potencia efectiva: 185 kcal/h
   - Módulos estimados: 12
   - Descripción: Radiador de aluminio de alta eficiencia
   - Colores disponibles: blanco, negro

2. BROEN 500
   - Potencia efectiva: 185 kcal/h
   - Módulos estimados: 12
   - Descripción: Radiador de acero con diseño moderno
   - Colores disponibles: blanco, cromo

3. GAMMA 500
   - Potencia efectiva: 172 kcal/h
   - Módulos estimados: 13
   - Descripción: Radiador de aluminio estilo minimalista
   - Colores disponibles: blanco, negro"
```

## 🛠️ Personalización

### Agregar Nuevos Nodos
Edita `app/peisa_advisor_knowledge_base.json`:
```json
{
  "id": "nuevo_nodo",
  "pregunta": "Tu pregunta aquí",
  "opciones": [
    { "texto": "Opción 1", "siguiente": "siguiente_nodo" }
  ]
}
```

### Agregar Nuevos Modelos de Radiadores
Edita `app/models.py`:
```python
RADIATOR_MODELS = {
    "NUEVO_MODELO": {
        "type": "principal",
        "installation": "superficie",
        "style": "moderno",
        "potencia": 200,
        "coeficiente": 1.0,
        "colors": ["blanco", "negro"],
        "description": "Descripción del modelo"
    }
}
```

### Modificar Parámetros de Cálculo
En `peisa_advisor_knowledge_base.json`, nodo de cálculo:
```json
{
  "id": "calculo_piso_radiante",
  "tipo": "calculo",
  "parametros": {
    "potencia_m2": { "norte": 100, "sur": 125 },  // Modificar aquí
    "densidad_caño": 5,  // Metros de caño por m²
    "longitud_maxima_circuito": 100  // Metros máximos por circuito
  }
}
```

## 🐛 Troubleshooting

### Error: "Sistema no inicializado"
**Causa**: Los motores no se inicializaron correctamente al arrancar el servidor.

**Solución**:
1. Verifica que todos los archivos existan:
   - `app/peisa_advisor_knowledge_base.json`
   - `app/expert_engine.py`
   - `app/rag_engine_v2.py`
   - `embeddings/products.faiss`
2. Reinicia el servidor
3. Revisa los logs de inicio en la consola

### Error: "Nodo no encontrado"
**Causa**: El ID del nodo no existe en la base de conocimiento.

**Solución**:
1. Abre `app/peisa_advisor_knowledge_base.json`
2. Verifica que el `id` del nodo sea correcto
3. Verifica que todos los nodos `siguiente` apunten a IDs válidos

### Error: "RAG Engine no inicializado"
**Causa**: El sistema RAG no pudo cargar los embeddings.

**Solución**:
```bash
# Regenerar embeddings
python ingest/ingest.py
```

### Error en cálculos: "Error evaluando expresión"
**Causa**: Error en la sintaxis de las expresiones de cálculo.

**Solución**:
1. Revisa las expresiones en nodos tipo `calculo`
2. Verifica que las variables referenciadas existan en el contexto
3. Ejemplo correcto:
   ```json
   "acciones": [
     "carga_termica = superficie * potencia_m2[zona_geografica]"
   ]
   ```

### Error: "Por favor ingrese valores numéricos válidos"
**Causa**: El usuario ingresó texto en un campo numérico.

**Solución**: El sistema maneja esto automáticamente, mostrando el mensaje de error al usuario.

### Puerto 8000 ya en uso
**Causa**: Otra aplicación está usando el puerto 8000.

**Solución**:
```bash
# Opción 1: Usar otro puerto
python -m uvicorn app.main:app --reload --port 8001

# Opción 2: Matar el proceso en el puerto 8000 (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

## 📚 Estructura de Archivos

```
pp2-soldasur-2c-2025/
├── app/
│   ├── main.py                              # Servidor FastAPI principal
│   ├── expert_engine.py                     # Motor del sistema experto
│   ├── orchestrator.py                      # Orquestador híbrido
│   ├── rag_engine_v2.py                     # Motor RAG
│   ├── models.py                            # Modelos de radiadores
│   ├── peisa_advisor_knowledge_base.json    # Base de conocimiento
│   ├── soldasur2025.html                    # Interfaz web
│   ├── soldasur.js                          # Lógica frontend
│   └── soldasur.css                         # Estilos
├── embeddings/
│   └── products.faiss                       # Índice vectorial
├── data/
│   ├── products_catalog.json                # Catálogo de productos
│   └── raw/Products_db.xlsx                 # Base de datos original
├── docs/
│   ├── SISTEMA_EXPERTO.md                   # Esta documentación
│   └── README_RAG_OLLAMA.md                 # Documentación RAG
└── requirements.txt                         # Dependencias Python
```

## 💡 Ventajas del Sistema Experto

✅ **Guía estructurada**: Paso a paso sin confusión  
✅ **Cálculos precisos**: Fórmulas validadas por expertos  
✅ **Personalización**: Recomendaciones basadas en preferencias  
✅ **Escalable**: Fácil agregar nuevos flujos y productos  
✅ **Híbrido**: Combina reglas con IA generativa  
✅ **Trazabilidad**: Historial completo de decisiones  
✅ **Sin entrenamiento**: No requiere datos de entrenamiento  
✅ **Determinístico**: Resultados predecibles y consistentes  

## 🎓 Conceptos Técnicos

### Sistema Basado en Reglas
El sistema experto usa **reglas IF-THEN** implícitas en la estructura de nodos:
```
IF usuario selecciona "Piso radiante"
THEN ir a nodo "superficie_piso"

IF zona == "sur" AND superficie == 50
THEN carga_termica = 50 * 125 = 6250 W
```

### Motor de Inferencia
El `ExpertEngine` actúa como motor de inferencia:
1. **Evalúa condiciones**: Opciones seleccionadas, valores ingresados
2. **Aplica reglas**: Navegación entre nodos según decisiones
3. **Ejecuta acciones**: Cálculos matemáticos automáticos
4. **Actualiza base de hechos**: Contexto de variables persistente

### Base de Conocimiento
Estructura JSON que representa el conocimiento del dominio:
- **Nodos**: Puntos de decisión o información
- **Aristas**: Transiciones entre nodos (campo `siguiente`)
- **Variables**: Hechos almacenados durante la conversación
- **Reglas**: Implícitas en las opciones y cálculos

### Integración RAG
El sistema puede enriquecerse con RAG para:
- **Explicar conceptos**: "¿Qué es la carga térmica?"
- **Buscar productos**: "Muéstrame radiadores blancos"
- **Responder tangencialmente**: Preguntas durante el flujo
- **Información adicional**: Complementar respuestas del experto

### Clasificación de Intenciones
El `IntentClassifier` usa patrones regex para determinar:
- **GUIDED_CALCULATION**: Usuario quiere flujo guiado
- **FREE_QUERY**: Usuario hace pregunta abierta
- **PRODUCT_SEARCH**: Usuario busca productos
- **CLARIFICATION**: Usuario pide aclaración
- **SWITCH_MODE**: Usuario cambia de modo
- **HYBRID**: Combinación de intenciones

## 🔧 Configuración Avanzada

### Variables de Entorno
Crea un archivo `.env` en la raíz:
```env
# Puerto del servidor
PORT=8000

# Modo de debug
DEBUG=True

# Ruta a base de conocimiento
KNOWLEDGE_BASE_PATH=app/peisa_advisor_knowledge_base.json

# Configuración RAG
EMBEDDINGS_PATH=embeddings/products.faiss
PRODUCTS_CATALOG=data/products_catalog.json
```

### Logging
Configura logging en `app/main.py`:
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### CORS (para desarrollo frontend)
En `app/main.py`:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📊 Métricas y Monitoreo

### Endpoint de Métricas
```python
@app.get("/metrics")
async def get_metrics():
    return {
        "total_conversations": len(orchestrator.contexts),
        "active_conversations": sum(1 for c in orchestrator.contexts.values() 
                                   if c.session_metadata['interaction_count'] > 0),
        "expert_mode_usage": sum(1 for c in orchestrator.contexts.values() 
                                if c.mode == "expert"),
        "rag_mode_usage": sum(1 for c in orchestrator.contexts.values() 
                             if c.mode == "rag")
    }
```

## 🧪 Testing

### Test Manual con cURL
```bash
# Iniciar conversación
curl -X POST http://localhost:8000/start \
  -H "Content-Type: application/json" \
  -d '{"conversation_id": "test123", "mode": "expert"}'

# Enviar respuesta
curl -X POST http://localhost:8000/reply \
  -H "Content-Type: application/json" \
  -d '{"conversation_id": "test123", "option_index": 0}'

# Health check
curl http://localhost:8000/health
```

### Test con Python
```python
import requests

# Iniciar conversación
response = requests.post("http://localhost:8000/start", json={
    "conversation_id": "test123",
    "mode": "expert"
})
print(response.json())

# Seleccionar opción
response = requests.post("http://localhost:8000/reply", json={
    "conversation_id": "test123",
    "option_index": 0
})
print(response.json())
```

## 🚀 Despliegue en Producción

### Usando Gunicorn
```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Usando Docker
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t peisa-advisor .
docker run -p 8000:8000 peisa-advisor
```

## 📖 Referencias

- **FastAPI**: https://fastapi.tiangolo.com/
- **Uvicorn**: https://www.uvicorn.org/
- **Jinja2**: https://jinja.palletsprojects.com/
- **Sistema Experto (Wikipedia)**: https://es.wikipedia.org/wiki/Sistema_experto

---

**Desarrollado por**: SOLDASUR S.A.  
**Versión**: 2.0  
**Última actualización**: 2025

**¿Necesitas ayuda?** Consulta los logs del servidor o revisa la documentación adicional en `docs/`
