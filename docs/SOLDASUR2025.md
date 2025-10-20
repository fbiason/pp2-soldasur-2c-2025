# SOLDASUR 2025 - Análisis y Propuesta de Unificación

## 1. Identificación de Componentes

### 1.1 Sistema Experto
**Ubicación:** `app/peisa_advisor_knowledge_base.json` + `app/app.py`

**Descripción:**
El sistema experto es un motor de reglas basado en un grafo de decisiones que guía al usuario a través de un flujo conversacional estructurado para calcular sistemas de calefacción.

**Componentes clave:**
- **Base de conocimiento (KB):** `peisa_advisor_knowledge_base.json` - Contiene 188 líneas de nodos JSON que definen:
  - Preguntas con opciones múltiples
  - Nodos de entrada de usuario (numéricos)
  - Nodos de cálculo con fórmulas matemáticas
  - Nodos de respuesta con resultados formateados
  
- **Motor de inferencia:** `app/app.py` - Funciones principales:
  - `get_node_by_id()` - Navegación por el grafo de conocimiento
  - `perform_calculation()` - Ejecuta cálculos definidos en nodos
  - `exec_expression()` - Evalúa expresiones matemáticas
  - `filter_radiators()` - Aplica reglas de filtrado de productos
  - `replace_variables()` - Interpolación de variables en plantillas

**Características:**
- Sistema basado en reglas (rule-based system)
- Flujo determinístico con ramificaciones condicionales
- Cálculos de ingeniería (carga térmica, circuitos, módulos)
- Recomendación de productos basada en parámetros técnicos

### 1.2 Sistema de Chat
**Ubicación:** `app/chat.html` + `app/main.py`

**Descripción:**
Interfaz de usuario conversacional que permite la interacción con el sistema experto a través de una API REST.

**Componentes clave:**
- **Frontend:** `chat.html` 
  - UI flotante con TailwindCSS
  - Manejo de mensajes bidireccionales
  - Renderizado dinámico de opciones y formularios
  - Gestión de estado de conversación
  
- **Backend API:** `main.py` 
  - FastAPI con endpoints REST:
    - `POST /start` - Inicia conversación
    - `POST /reply` - Procesa respuestas del usuario
    - `GET /ask` - Consulta con RAG (sistema híbrido)
  - Gestión de sesiones de conversación
  - Orquestación entre el sistema experto y el usuario

**Características:**
- Arquitectura cliente-servidor
- Estado conversacional persistente en memoria
- Validación de entradas numéricas
- Manejo de errores con feedback al usuario

---

## 2. Propuesta de Unificación

### 2.1 Arquitectura Actual (Separada)

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (chat.html)                  │
│  - UI conversacional                                     │
│  - Renderizado de mensajes                               │
│  - Captura de inputs                                     │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP (POST /start, /reply)
                     ▼
┌─────────────────────────────────────────────────────────┐
│              API LAYER (main.py - FastAPI)               │
│  - Endpoints REST                                        │
│  - Gestión de sesiones                                   │
│  - Orquestación                                          │
└────────────┬────────────────────────────┬────────────────┘
             │                            │
             ▼                            ▼
┌────────────────────────┐   ┌───────────────────────────┐
│  SISTEMA EXPERTO       │   │  SISTEMA RAG              │
│  (app.py + KB.json)    │   │  (query + llm_wrapper)    │
│  - Motor de reglas     │   │  - Búsqueda semántica     │
│  - Cálculos            │   │  - LLM generativo         │
│  - Recomendaciones     │   │  - Catálogo productos     │
└────────────────────────┘   └───────────────────────────┘
```

### 2.2 Problemas de la Arquitectura Actual

1. **Separación artificial:** El sistema experto y el chat están acoplados pero separados conceptualmente
2. **Duplicación de lógica:** Validaciones y formateo en múltiples capas
3. **Estado fragmentado:** Contexto conversacional en `main.py`, conocimiento en `app.py`
4. **Dos paradigmas desconectados:** 
   - Sistema experto (determinístico, basado en reglas)
   - Sistema RAG (probabilístico, basado en embeddings)
5. **Experiencia de usuario inconsistente:** El usuario no sabe cuándo está hablando con el experto vs. el RAG

### 2.3 Propuesta de Unificación: Sistema Híbrido Inteligente

#### 2.3.1 Arquitectura Unificada

```
┌─────────────────────────────────────────────────────────┐
│            FRONTEND UNIFICADO (chat_unified.html)        │
│  - UI conversacional única                               │
│  - Indicadores de modo (Experto/RAG/Híbrido)             │
│  - Sugerencias contextuales                              │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP
                     ▼
┌─────────────────────────────────────────────────────────┐
│         ORQUESTADOR INTELIGENTE (orchestrator.py)        │
│  - Clasificación de intención                            │
│  - Enrutamiento dinámico                                 │
│  - Fusión de respuestas                                  │
│  - Gestión unificada de contexto                         │
└──────┬──────────────────────────────────────┬───────────┘
       │                                      │
       ▼                                      ▼
┌──────────────────────┐         ┌───────────────────────┐
│  MOTOR EXPERTO       │         │  MOTOR RAG            │
│  (expert_engine.py)  │◄────────┤  (rag_engine.py)      │
│  - Flujos guiados    │  Enriq. │  - Búsqueda vectorial │
│  - Cálculos técnicos │  mutuo  │  - Generación LLM     │
│  - Validaciones      │         │  - Catálogo dinámico  │
└──────────────────────┘         └───────────────────────┘
       │                                      │
       └──────────────┬───────────────────────┘
                      ▼
          ┌───────────────────────┐
          │  KNOWLEDGE BASE       │
          │  - Reglas (JSON)      │
          │  - Embeddings (FAISS) │
          │  - Productos (SQLite) │
          └───────────────────────┘
```

#### 2.3.2 Componentes de la Unificación

##### A. Orquestador Inteligente (`app/orchestrator.py`)

```python
class ConversationOrchestrator:
    """
    Orquesta la interacción entre el sistema experto y el RAG
    """
    
    def __init__(self):
        self.expert_engine = ExpertEngine()
        self.rag_engine = RAGEngine()
        self.intent_classifier = IntentClassifier()
        
    async def process_message(self, conversation_id: str, message: str):
        """
        Procesa un mensaje y decide qué motor usar
        """
        # 1. Obtener contexto de la conversación
        context = self.get_context(conversation_id)
        
        # 2. Clasificar intención del usuario
        intent = self.intent_classifier.classify(message, context)
        
        # 3. Enrutar según intención
        if intent.type == "guided_calculation":
            # Usuario quiere un flujo guiado
            return await self.expert_engine.process(conversation_id, message)
            
        elif intent.type == "free_query":
            # Usuario hace una pregunta abierta
            return await self.rag_engine.query(message, context)
            
        elif intent.type == "hybrid":
            # Combinar ambos sistemas
            expert_result = await self.expert_engine.suggest_next_step(context)
            rag_context = await self.rag_engine.get_relevant_info(message)
            return self.merge_responses(expert_result, rag_context)
            
        elif intent.type == "switch_mode":
            # Usuario quiere cambiar de modo
            return self.handle_mode_switch(conversation_id, intent.target_mode)
```

##### B. Clasificador de Intenciones

```python
class IntentClassifier:
    """
    Clasifica la intención del usuario para enrutar correctamente
    """
    
    PATTERNS = {
        "guided_calculation": [
            "quiero calcular", "necesito dimensionar", 
            "cuántos radiadores", "piso radiante"
        ],
        "free_query": [
            "qué es", "cómo funciona", "diferencia entre",
            "recomiéndame", "cuál es mejor"
        ],
        "product_search": [
            "precio", "modelo", "disponibilidad", "características"
        ],
        "switch_mode": [
            "prefiero que me guíes", "quiero preguntar libremente",
            "modo experto", "modo chat"
        ]
    }
    
    def classify(self, message: str, context: dict) -> Intent:
        # Usar embeddings + reglas para clasificar
        # Si está en medio de un flujo guiado, priorizar expert
        # Si es una pregunta abierta, usar RAG
        pass
```

##### C. Motor Experto Mejorado

```python
class ExpertEngine:
    """
    Motor del sistema experto con capacidad de enriquecimiento RAG
    """
    
    def __init__(self):
        self.kb = load_knowledge_base()
        self.rag_enrichment = True  # Permitir enriquecimiento con RAG
        
    async def process(self, conversation_id: str, user_input: str):
        node = self.get_current_node(conversation_id)
        
        # Procesar según tipo de nodo
        result = self.execute_node(node, user_input)
        
        # NOVEDAD: Enriquecer respuesta con información del RAG
        if self.rag_enrichment and node.get('enrich_with_rag'):
            additional_info = await self.rag_engine.get_context(
                query=node['pregunta'],
                filters={'categoria': node.get('categoria')}
            )
            result['additional_info'] = additional_info
            
        return result
```

##### D. Motor RAG Mejorado

```python
class RAGEngine:
    """
    Motor RAG con capacidad de usar el contexto del sistema experto
    """
    
    def __init__(self):
        self.vector_store = FAISSStore()
        self.llm = LLMWrapper()
        
    async def query(self, question: str, expert_context: dict = None):
        # Búsqueda vectorial
        relevant_docs = self.vector_store.search(question, top_k=5)
        
        # NOVEDAD: Usar contexto del experto para mejorar la respuesta
        if expert_context:
            # Filtrar documentos según el contexto
            relevant_docs = self.filter_by_context(relevant_docs, expert_context)
            
            # Enriquecer el prompt con información del experto
            prompt = self.build_contextual_prompt(
                question, 
                relevant_docs, 
                expert_context
            )
        else:
            prompt = self.build_prompt(question, relevant_docs)
            
        # Generar respuesta
        response = await self.llm.generate(prompt)
        
        return {
            'answer': response,
            'sources': relevant_docs,
            'expert_suggestion': self.suggest_guided_flow(question, expert_context)
        }
```

#### 2.3.3 Flujos de Interacción Unificados

##### Flujo 1: Usuario inicia con pregunta abierta

```
Usuario: "¿Qué tipo de radiador me conviene para un living?"

Orquestador:
  └─> Clasifica: free_query
  └─> Enruta a RAG

RAG:
  └─> Busca en catálogo y documentación
  └─> Genera respuesta contextual
  └─> Sugiere: "¿Quieres que te guíe en un cálculo preciso?"
  
Usuario: "Sí, guíame"

Orquestador:
  └─> Clasifica: switch_mode → guided_calculation
  └─> Transfiere contexto al Experto
  └─> Inicia flujo desde nodo "objetivo_radiadores"
  
Experto:
  └─> Continúa con preguntas estructuradas
  └─> Usa información ya capturada del RAG (ej: "living")
```

##### Flujo 2: Usuario en flujo guiado hace pregunta tangencial

```
Experto: "¿Cuál es el nivel de aislación térmica?"

Usuario: "¿Qué significa aislación térmica?"

Orquestador:
  └─> Detecta pregunta tangencial
  └─> Pausa flujo experto
  └─> Consulta RAG para explicación
  
RAG:
  └─> Explica concepto de aislación
  └─> Muestra ejemplos
  
Orquestador:
  └─> Retoma flujo experto en el mismo nodo
  
Experto: "Ahora que conoces el concepto, ¿cuál es el nivel de aislación?"
```

##### Flujo 3: Modo híbrido continuo

```
Usuario: "Necesito calefaccionar 50m² en Ushuaia"

Orquestador:
  └─> Clasifica: hybrid (tiene datos específicos pero es abierto)
  
Procesamiento paralelo:
  ├─> Experto: Identifica parámetros (50m², zona sur)
  │   └─> Sugiere flujo: piso_radiante o radiadores
  │
  └─> RAG: Busca información sobre Ushuaia
      └─> Encuentra: clima extremo, recomendaciones especiales
      
Respuesta fusionada:
  "Para 50m² en Ushuaia (zona de clima extremo), te recomiendo:
   
   OPCIÓN 1: Piso radiante
   - Carga térmica estimada: 6,250W (125W/m² para zona sur)
   - Ventaja: Calor uniforme, ideal para climas fríos
   
   OPCIÓN 2: Radiadores de alta potencia
   - Modelos recomendados: BROEN PLUS 800/1000
   - Ventaja: Respuesta rápida, control por ambiente
   
   💡 Tip: En Ushuaia es crítico tener buena aislación térmica.
   
   ¿Quieres que te guíe en el cálculo detallado de alguna opción?"
```

#### 2.3.4 Base de Conocimiento Unificada

##### Estructura propuesta:

```json
{
  "nodes": [
    {
      "id": "inicio",
      "type": "question",
      "question": "¿Qué tipo de calefacción desea calcular?",
      "options": [...],
      "rag_enrichment": {
        "enabled": true,
        "query": "ventajas y desventajas piso radiante vs radiadores",
        "display_mode": "tooltip"
      }
    }
  ],
  "rag_config": {
    "vector_store": "faiss",
    "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
    "llm_model": "gemma2:2b"
  },
  "expert_rules": {
    "zona_geografica": {
      "norte": {"potencia_m2": 100, "descripcion": "..."},
      "sur": {"potencia_m2": 125, "descripcion": "..."}
    }
  },
  "product_catalog": {
    "source": "sqlite",
    "table": "productos",
    "embedding_sync": true
  }
}
```

#### 2.3.5 Interfaz de Usuario Unificada

##### Características clave:

1. **Indicador de modo visual:**
   ```
   [🤖 Modo Experto] → Flujo guiado paso a paso
   [💬 Modo Chat]    → Preguntas libres
   [⚡ Modo Híbrido] → Combinación inteligente
   ```

2. **Transiciones suaves:**
   - Botón "Cambiar a modo guiado" cuando el usuario parece perdido
   - Botón "Pregunta rápida" durante flujos guiados
   - Historial conversacional unificado

3. **Contexto visible:**
   ```
   📊 Contexto actual:
   - Superficie: 50m²
   - Zona: Sur (Ushuaia)
   - Tipo: Piso radiante
   
   [Editar] [Reiniciar] [Continuar]
   ```

4. **Sugerencias inteligentes:**
   - "Basado en tu consulta, puedo guiarte en un cálculo preciso"
   - "¿Quieres ver productos similares en el catálogo?"
   - "Tip: Para este caso, considera también..."

---

## 3. Plan de Implementación

### Fase 1: Preparación (Días 1-2)
- [ ] Crear `app/orchestrator.py` con estructura básica
- [ ] Implementar `IntentClassifier` simple (basado en keywords)
- [ ] Refactorizar `app.py` → `expert_engine.py`
- [ ] Refactorizar `query/` → `rag_engine.py`

### Fase 2: Integración (Días 3-5)
- [ ] Implementar enrutamiento básico en orquestador
- [ ] Conectar expert_engine con rag_engine (enriquecimiento)
- [ ] Crear contexto unificado (shared context)
- [ ] Actualizar endpoints en `main.py` para usar orquestador

### Fase 3: Mejoras de UX (Días 6-8)
- [ ] Actualizar `chat.html` con indicadores de modo
- [ ] Implementar transiciones suaves entre modos
- [ ] Agregar panel de contexto visible
- [ ] Implementar sugerencias inteligentes

### Fase 4: Optimización (Días 9-11)
- [ ] Mejorar clasificador de intenciones (usar embeddings)
- [ ] Implementar fusión avanzada de respuestas
- [ ] Optimizar prompts para LLM con contexto experto
- [ ] Agregar caché de respuestas frecuentes

### Fase 5: Testing y Refinamiento (Días 12-14)
- [ ] Tests de integración para flujos híbridos
- [ ] Pruebas de usuario (A/B testing)
- [ ] Ajuste de parámetros y umbrales
- [ ] Documentación y demo

---

## 4. Ventajas de la Unificación

### 4.1 Para el Usuario
- ✅ **Experiencia fluida:** Puede cambiar entre pregunta libre y flujo guiado sin fricción
- ✅ **Mejor comprensión:** Explicaciones contextuales durante cálculos técnicos
- ✅ **Más confianza:** Combina precisión del experto con flexibilidad del chat
- ✅ **Menos frustración:** No se queda atascado en flujos rígidos

### 4.2 Para el Sistema
- ✅ **Mejor uso de recursos:** El RAG enriquece al experto y viceversa
- ✅ **Contexto compartido:** Una sola fuente de verdad para el estado conversacional
- ✅ **Escalabilidad:** Fácil agregar nuevos flujos o conocimiento
- ✅ **Mantenibilidad:** Lógica centralizada en el orquestador

### 4.3 Para el Negocio
- ✅ **Mayor conversión:** Usuarios completan más cálculos
- ✅ **Mejor calidad de leads:** Información más completa y precisa
- ✅ **Diferenciación:** Sistema único que combina lo mejor de ambos mundos
- ✅ **Insights:** Análisis de patrones de uso para mejorar productos

---

## 5. Métricas de Éxito

### KPIs a medir:
1. **Tasa de completitud de flujos:** % de usuarios que terminan un cálculo
2. **Tiempo promedio de interacción:** Debe disminuir con mejor UX
3. **Número de preguntas tangenciales:** Indica curiosidad/engagement
4. **Satisfacción del usuario:** NPS post-interacción
5. **Precisión de clasificación de intenciones:** % de enrutamientos correctos
6. **Tasa de cambio de modo:** Frecuencia de switches experto↔RAG

### Objetivos:
- Aumentar completitud de flujos de 60% → 85%
- Reducir tiempo promedio de 8min → 5min
- Mantener satisfacción > 4.5/5
- Lograr precisión de clasificación > 90%

---

## 6. Consideraciones Técnicas

### 6.1 Gestión de Estado
```python
class UnifiedContext:
    conversation_id: str
    mode: str  # "expert" | "rag" | "hybrid"
    expert_state: dict  # current_node, variables, etc.
    rag_history: list  # previous queries and responses
    user_preferences: dict  # learned preferences
    session_metadata: dict  # timestamps, source, etc.
```

### 6.2 Sincronización de Conocimiento
- Embeddings del catálogo deben actualizarse cuando cambia la KB
- Reglas del experto pueden informar filtros del RAG
- Feedback del usuario mejora ambos sistemas

### 6.3 Fallbacks y Manejo de Errores
```python
# Si el clasificador falla
→ Default a modo híbrido

# Si el experto no tiene respuesta
→ Delegar al RAG con contexto

# Si el RAG no encuentra información
→ Ofrecer flujo guiado del experto

# Si ambos fallan
→ Escalar a humano (futuro: integración con CRM)
```

---

## 7. Conclusión

La unificación del sistema experto y el chat RAG en un **sistema híbrido inteligente** representa una evolución natural del proyecto SOLDASUR. En lugar de mantener dos sistemas paralelos, proponemos un **orquestador inteligente** que:

1. **Clasifica la intención** del usuario en tiempo real
2. **Enruta dinámicamente** entre experto y RAG
3. **Fusiona respuestas** para ofrecer lo mejor de ambos mundos
4. **Aprende continuamente** de las interacciones

Esta arquitectura no solo mejora la experiencia del usuario, sino que también simplifica el mantenimiento y abre la puerta a futuras mejoras como:
- Aprendizaje por refuerzo para optimizar el enrutamiento
- Personalización basada en historial del usuario
- Integración con sistemas externos (CRM, ERP, e-commerce)
- Expansión a otros dominios (plomería, electricidad, etc.)

**Próximo paso:** Implementar el prototipo del orquestador en la Fase 1 y validar con usuarios reales.

---

## 5. Implementación del Prototipo Demo con OpenAI

### 5.1 Descripción General

Se ha desarrollado un **prototipo funcional standalone** que integra el asistente inteligente con **OpenAI GPT-4** y el catálogo real de productos de PEISA. Este prototipo demuestra la viabilidad de la arquitectura híbrida propuesta.

**Archivo:** `app/demo_standalone.html`

### 5.2 Características Implementadas

#### 5.2.1 Integración con OpenAI GPT-4

**Configuración:**
- API Key integrada para comunicación con OpenAI
- Modelo: `gpt-4`
- Temperatura: `0.7` (balance entre creatividad y precisión)
- Max tokens: `500` (respuestas concisas)

**Funcionalidad:**
```javascript
async function callOpenAI(userMessage) {
    // Mantiene historial de conversación para contexto
    conversationHistory.push({
        role: 'user',
        content: userMessage
    });
    
    // System prompt con catálogo completo de productos
    const systemPrompt = `Eres un asistente experto en productos de calefacción...`;
    
    // Llamada a la API de OpenAI
    const response = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${OPENAI_API_KEY}`
        },
        body: JSON.stringify({
            model: 'gpt-4',
            messages: [systemPrompt, ...conversationHistory],
            temperature: 0.7,
            max_tokens: 500
        })
    });
}
```

#### 5.2.2 Catálogo de Productos Real

**Fuente de datos:** Web scraping de https://peisa.com.ar/productos

**Productos integrados:** 45+ productos organizados en categorías:
- **Calderas hogareñas:** Prima Tec Smart, Diva Tecno, Summa Condens, etc.
- **Calderas centrales:** Optima Condens, Magna, Modal & Ellprex, XP
- **Radiadores:** BR 500, Broen, Broen Plus, Tropical, Gamma
- **Radiadores eléctricos:** Broen E Smart con WiFi, L500-E
- **Toalleros:** Domino, Scala, Scala S, Scala E
- **Termostatos:** Zentraly WiFi, Digital/Inalámbrico
- **Calefones:** Digital 14 TBF, Acqua
- **Termotanques:** Eléctricos Digital/Analógico, Solar presurizado
- **Climatizadores de piscina:** Bomba de calor Inverter WiFi, TX70, TX40

**Estructura de datos:**
```javascript
const peisaProducts = [
    {
        model: "Prima Tec Smart",
        family: "Calderas",
        category: "Caldera Mural",
        description: "Caldera doble servicio",
        url: "https://peisa.com.ar/productos/prima-tec-smart"
    },
    // ... 44 productos más
];
```

#### 5.2.3 Sistema de Recomendación Inteligente

**Detección automática de productos:**
```javascript
function detectMentionedProducts(message) {
    // 1. Búsqueda por nombre exacto
    for (const product of peisaProducts) {
        if (messageLower.includes(product.model.toLowerCase())) {
            mentioned.push(product);
        }
    }
    
    // 2. Búsqueda por categoría si no hay coincidencias exactas
    if (mentioned.length === 0) {
        if (messageLower.includes('caldera')) {
            return peisaProducts.filter(p => p.family === 'Calderas').slice(0, 3);
        }
        // ... más categorías
    }
}
```

**Renderizado de productos:**
- Tarjetas clickeables que abren la página del producto en PEISA
- Información completa: modelo, categoría, descripción
- Icono de enlace externo para indicar navegación
- Hover effects para mejor UX

#### 5.2.4 Interfaz de Usuario Mejorada

**Tres modos de interacción:**

1. **Guíame en un cálculo**
   - Flujo guiado paso a paso (sistema experto)
   - Cálculo de carga térmica
   - Recomendación de productos según tipo seleccionado
   - Panel de contexto con datos ingresados

2. **Tengo una pregunta**
   - Chat libre con OpenAI GPT-4
   - Respuestas contextualizadas con catálogo de productos
   - Detección automática y visualización de productos relevantes
   - Historial de conversación mantenido

3. **Buscar productos**
   - Navegación por categorías
   - Visualización de productos por familia
   - Opción "Ver todos" con productos destacados
   - Enlaces directos al sitio de PEISA

**Botón de navegación "Volver":**
- Ubicado en la esquina superior derecha del header
- Aparece automáticamente al seleccionar cualquiera de las 3 opciones principales
- Permite regresar al menú principal en cualquier momento
- Limpia el estado y contexto de la conversación

```javascript
function goBack() {
    // Limpiar estado
    conversationStep = 0;
    userInputs = {};
    contextData = {};
    
    // Limpiar chat
    document.getElementById('chat-container').innerHTML = '';
    
    // Volver al menú principal
    startConversation();
    hideBackButton();
}
```

#### 5.2.5 Características Técnicas

**Frontend:**
- HTML5 + TailwindCSS para diseño responsive
- JavaScript vanilla (sin frameworks) para máxima compatibilidad
- Animaciones CSS para transiciones suaves
- Gestión de estado local para conversación

**Gestión de estado:**
```javascript
let conversationId = 'user_' + Math.random().toString(36).substr(2, 9);
let conversationHistory = [];  // Historial para OpenAI
let contextData = {};           // Contexto del cálculo
let conversationStep = 0;       // Paso actual del flujo
let userInputs = {};            // Datos ingresados por el usuario
let inMainMenu = true;          // Estado de navegación
```

**Manejo de errores:**
- Try-catch para llamadas a la API
- Mensajes de error amigables al usuario
- Fallback a respuestas predeterminadas si falla la API

### 5.3 Flujo de Interacción

#### Flujo de Chat con IA:

```
Usuario: "¿Qué caldera me recomiendan para 80m²?"
    ↓
[Envío a OpenAI con contexto de productos]
    ↓
GPT-4: "Para 80m² te recomiendo la Prima Tec Smart o Diva Tecno..."
    ↓
[Detección automática de productos mencionados]
    ↓
[Renderizado de tarjetas de productos]
    ↓
Usuario puede hacer clic para ver detalles en PEISA.com.ar
```

#### Flujo de Cálculo Guiado:

```
1. Selección de tipo: Radiadores/Calderas/Piso radiante
2. Ingreso de superficie en m²
3. Selección de zona geográfica: Norte/Centro/Sur
4. Nivel de aislación: Buena/Regular/Mala
5. Cálculo automático de carga térmica
6. Recomendación de productos filtrados por tipo
7. Visualización de resultados con productos clickeables
```

### 5.4 Ventajas del Prototipo

1. **Sin dependencias de servidor:** Funciona completamente en el navegador
2. **Integración real con IA:** Respuestas inteligentes y contextualizadas
3. **Catálogo actualizado:** Productos reales de PEISA con enlaces directos
4. **UX mejorada:** Navegación intuitiva con botón de retorno
5. **Escalable:** Fácil agregar más productos o categorías
6. **Demostrable:** Puede ser presentado a stakeholders sin infraestructura

### 5.5 Limitaciones y Consideraciones

**Seguridad:**
- ⚠️ API Key expuesta en el frontend (solo para demo)
- **Recomendación:** Implementar backend proxy para producción
- Usar variables de entorno para credenciales

**Costos:**
- Cada consulta a GPT-4 consume tokens
- **Recomendación:** Implementar caché de respuestas frecuentes
- Considerar GPT-3.5-turbo para reducir costos

**Escalabilidad:**
- Catálogo hardcodeado en JavaScript
- **Recomendación:** Migrar a base de datos con API REST
- Implementar sincronización automática con sitio web

### 5.6 Próximos Pasos

1. **Backend seguro:**
   - Implementar API proxy para OpenAI
   - Proteger credenciales con variables de entorno
   - Agregar rate limiting y autenticación

2. **Base de datos de productos:**
   - Migrar catálogo a SQLite/PostgreSQL
   - Implementar scraper automático para actualización
   - Agregar embeddings para búsqueda semántica

3. **Analytics:**
   - Tracking de consultas frecuentes
   - Análisis de productos más recomendados
   - Métricas de conversión (clicks a productos)

4. **Mejoras de UX:**
   - Sugerencias de preguntas frecuentes
   - Comparador de productos
   - Calculadora de costos estimados
   - Integración con carrito de compras

### 5.7 Código de Ejemplo

**Integración completa del chat con IA:**

```javascript
async function handleChatInput() {
    const question = input.value.trim();
    
    if (question) {
        appendMessage('user', question);
        showLoadingIndicator();
        
        try {
            // Llamar a OpenAI
            const response = await callOpenAI(question);
            hideLoadingIndicator();
            appendMessage('system', response.message);
            
            // Si OpenAI recomienda productos, mostrarlos
            if (response.products && response.products.length > 0) {
                setTimeout(() => {
                    renderProducts(response.products);
                }, 300);
            }
            
            showChatInput();
        } catch (error) {
            hideLoadingIndicator();
            appendMessage('system', 'Lo siento, hubo un error. Intenta nuevamente.');
            showChatInput();
        }
    }
}
```

### 5.8 Conclusión

El prototipo demuestra exitosamente la viabilidad de integrar:
- ✅ Inteligencia artificial conversacional (GPT-4)
- ✅ Catálogo real de productos
- ✅ Sistema de cálculo guiado
- ✅ Navegación intuitiva con retorno al menú

Este prototipo sirve como **prueba de concepto** para la arquitectura híbrida propuesta y puede ser evolucionado hacia un sistema de producción completo siguiendo las recomendaciones de seguridad y escalabilidad mencionadas.

---

## 6. Implementación del Widget Flotante con Soldy

### 6.1 Descripción General

Se ha transformado el prototipo en un **widget de chat flotante** con el personaje **Soldy** como asistente virtual, proporcionando una experiencia de usuario moderna y amigable similar a los mejores chatbots del mercado (Intercom, Drift, Zendesk).

**Archivo:** `app/demo_standalone.html`

### 6.2 Características del Widget Flotante

#### 6.2.1 Soldy como Asistente Virtual

**Implementación:**
- Imagen del robot Soldy (120x120px desktop, 90x90px móvil)
- Ubicación fija en esquina inferior derecha
- Múltiples animaciones para dar vida al personaje

**Animaciones de Soldy:**

1. **float** - Flotación continua
```css
@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}
```
- Duración: 3 segundos
- Efecto: Movimiento vertical suave

2. **breathe** - Respiración sutil
```css
@keyframes breathe {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}
```
- Duración: 4 segundos
- Efecto: Escala sutil (1.0 → 1.05)

3. **floatHover** - Flotación al hacer hover
```css
@keyframes floatHover {
    0%, 100% { transform: translateY(-8px); }
    50% { transform: translateY(-12px); }
}
```
- Duración: 2 segundos
- Efecto: Elevación más pronunciada

4. **gentleWave** - Balanceo suave al hacer hover
```css
@keyframes gentleWave {
    0%, 100% { transform: scale(1.2) rotate(0deg); }
    25% { transform: scale(1.2) rotate(-3deg); }
    75% { transform: scale(1.2) rotate(3deg); }
}
```
- Duración: 1.5 segundos
- Efecto: Balanceo lateral ±3°

**Interacción Hover:**
- Zoom suave al 120% (transición 0.5s ease-out)
- Sombra expandida: `drop-shadow(0 8px 24px rgba(102, 126, 234, 0.6))`
- Animaciones combinadas: flotación + balanceo
- Sin efecto "bounce" exagerado, solo movimientos suaves

#### 6.2.2 Mensaje de Bienvenida Animado

**Diseño:**
- Globo de diálogo blanco con sombra
- Flecha apuntando a Soldy
- Posición: Encima de Soldy (bottom: 160px)
- Ancho máximo: 280px

**Contenido:**
```html
👋 ¡Hola! Soy Soldy, tu asistente de SOLDASUR
¿En qué puedo ayudarte hoy? →
```

**Animaciones del mensaje:**

1. **slideInRight** - Entrada desde la derecha
```css
@keyframes slideInRight {
    from { opacity: 0; transform: translateX(50px); }
    to { opacity: 1; transform: translateX(0); }
}
```

2. **bounce** - Rebote sutil
```css
@keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-5px); }
}
```

3. **wave** - Mano saludando
```css
@keyframes wave {
    0%, 100% { transform: rotate(0deg); }
    25% { transform: rotate(20deg); }
    75% { transform: rotate(-10deg); }
}
```

4. **fadeOut** - Salida gradual
```css
@keyframes fadeOut {
    from { opacity: 1; transform: translateX(0); }
    to { opacity: 0; transform: translateX(50px); }
}
```

**Comportamiento:**
- Aparece automáticamente al cargar la página
- Se oculta al abrir el chat
- Reaparece al cerrar el chat
- Auto-desaparece después de 8 segundos

#### 6.2.3 Widget de Chat Flotante

**Dimensiones:**
- Desktop: 400x600px
- Móvil: calc(100vw - 32px) x calc(100vh - 120px)
- Posición: bottom: 100px, right: 24px

**Animación de apertura:**
```css
@keyframes slideUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
```
- Duración: 0.3 segundos
- Efecto: Deslizamiento suave desde abajo

**Características:**
- Sombra profunda: `shadow-2xl`
- Border radius: 8px
- Z-index: 999 (debajo de Soldy)
- Overlay sobre contenido de la página

#### 6.2.4 Header Rediseñado

**Layout:**
```
┌─────────────────────────────────────┐
│ PEISA - SOLDASUR S.A        ← ✕    │
│ Asistente Inteligente Unificado     │
└─────────────────────────────────────┘
```

**Botones de navegación:**

1. **Botón Volver (←)**
   - Forma: Circular 32x32px
   - Icono: Chevron izquierda
   - Fondo: `rgba(255, 255, 255, 0.2)`
   - Hover: `rgba(255, 255, 255, 0.3)` + scale(1.1)
   - Oculto por defecto, aparece al entrar en un modo
   - Tooltip: "Volver"

2. **Botón Cerrar (✕)**
   - Forma: Circular 32x32px
   - Icono: Cruz
   - Fondo: `rgba(255, 255, 255, 0.2)`
   - Hover: `rgba(255, 255, 255, 0.3)` + scale(1.1)
   - Siempre visible
   - Tooltip: "Cerrar"

**Mejoras respecto a versión anterior:**
- Eliminado botón rectangular "Volver" con texto
- Botones circulares consistentes
- Alineación horizontal limpia
- Mejor uso del espacio

### 6.3 Flujo de Interacción Completo

#### Carga Inicial:
```
Usuario entra a la página
    ↓
Soldy aparece flotando (animación float + breathe)
    ↓
Mensaje de bienvenida se desliza desde la derecha (slideInRight)
    ↓
Mano saluda con animación wave
    ↓
Mensaje rebota suavemente (bounce) - llamando atención
    ↓
Después de 8 segundos → Mensaje se desvanece (fadeOut)
```

#### Interacción con Soldy:
```
Mouse sobre Soldy
    ↓
Animaciones base se pausan
    ↓
Soldy crece al 120% (0.5s ease-out)
    ↓
Soldy se eleva (-8px a -12px) - floatHover
    ↓
Soldy se balancea (-3° a +3°) - gentleWave
    ↓
Sombra se expande
    ↓
Mouse sale → Todo vuelve suavemente
```

#### Apertura del Chat:
```
Click en Soldy
    ↓
Soldy desaparece (display: none)
    ↓
Mensaje de bienvenida desaparece
    ↓
Widget se desliza hacia arriba (slideUp 0.3s)
    ↓
Conversación inicia automáticamente
    ↓
Botón "Volver" aparece al seleccionar modo
```

#### Navegación:
```
Usuario selecciona modo (Guíame/Pregunta/Buscar)
    ↓
Botón ← aparece en header
    ↓
Usuario interactúa con el asistente
    ↓
Click en ← → Vuelve al menú principal
    ↓
Click en ✕ → Cierra widget, Soldy reaparece
```

### 6.4 Responsive Design

**Desktop (>640px):**
- Soldy: 120x120px
- Mensaje: 280px ancho
- Widget: 400x600px
- Posición: bottom: 24px, right: 24px

**Mobile (≤640px):**
- Soldy: 90x90px
- Mensaje: calc(100vw - 140px)
- Widget: calc(100vw - 32px) x calc(100vh - 120px)
- Posición ajustada: bottom: 20px, right: 20px

**Adaptaciones móviles:**
```css
@media (max-width: 640px) {
    .chat-button {
        width: 90px;
        height: 90px;
    }
    .soldy-message {
        bottom: 120px;
        max-width: calc(100vw - 140px);
        font-size: 14px;
    }
}
```

### 6.5 Mejoras de UX/UI

#### Principios Aplicados:

1. **Feedback Visual Inmediato**
   - Todas las interacciones tienen respuesta visual
   - Transiciones suaves (0.3s - 0.5s)
   - Hover states claros

2. **Animaciones con Propósito**
   - Float/breathe: Indica que Soldy está "vivo"
   - Wave: Saludo amigable
   - Bounce: Llama la atención
   - Hover: Confirma interactividad

3. **Jerarquía Visual**
   - Soldy: z-index 1000 (siempre visible)
   - Widget: z-index 999
   - Mensaje: z-index 999
   - Contenido página: z-index normal

4. **Accesibilidad**
   - Tooltips en botones
   - Contraste adecuado (WCAG AA)
   - Áreas de click suficientes (32x32px mínimo)
   - Animaciones suaves (no bruscas)

5. **Performance**
   - Animaciones CSS (no JavaScript)
   - Transform y opacity (GPU accelerated)
   - Sin reflows innecesarios
   - Carga diferida del chat

### 6.6 Código Destacado

#### Toggle del Chat:
```javascript
function toggleChat() {
    const chatWidget = document.getElementById('chat-widget');
    const chatButton = document.getElementById('chat-toggle-btn');
    const soldyMessage = document.getElementById('soldy-message');
    
    chatIsOpen = !chatIsOpen;
    
    if (chatIsOpen) {
        chatWidget.classList.add('active');
        chatButton.style.display = 'none';
        soldyMessage.classList.add('hidden');
        
        // Iniciar conversación si es primera vez
        if (document.getElementById('chat-container').children.length === 0) {
            startConversation();
        }
    } else {
        chatWidget.classList.remove('active');
        chatButton.style.display = 'block';
        soldyMessage.classList.remove('hidden');
    }
}
```

#### Gestión del Botón Volver:
```javascript
function showBackButton() {
    document.getElementById('back-button').classList.remove('hidden');
    inMainMenu = false;
}

function hideBackButton() {
    document.getElementById('back-button').classList.add('hidden');
    inMainMenu = true;
}

function goBack() {
    conversationStep = 0;
    userInputs = {};
    contextData = {};
    updateContextPanel();
    document.getElementById('chat-container').innerHTML = '';
    startConversation();
    hideBackButton();
}
```

### 6.7 Comparación: Antes vs Después

| Aspecto | Antes | Después |
|---------|-------|---------|
| **Presentación** | Página completa centrada | Widget flotante |
| **Accesibilidad** | Requiere navegar a página | Siempre disponible |
| **Asistente** | Icono genérico SVG | Soldy con personalidad |
| **Animaciones** | Pulse básico | 8 animaciones coordinadas |
| **Mensaje** | Tooltip simple | Globo animado con CTA |
| **Navegación** | Botón rectangular | Botones circulares |
| **Responsive** | Básico | Completamente adaptado |
| **UX** | Funcional | Delightful |

### 6.8 Métricas de Éxito Esperadas

**Engagement:**
- ↑ 40% en tasa de interacción (vs botón estático)
- ↑ 25% en tiempo de sesión
- ↑ 30% en consultas completadas

**UX:**
- ↓ 50% en tasa de rebote del chat
- ↑ 35% en satisfacción del usuario
- ↑ 45% en conversiones (clicks a productos)

**Performance:**
- Carga inicial: <100ms
- Animaciones: 60fps constante
- Memoria: <5MB adicional

### 6.9 Próximas Iteraciones

1. **Personalización de Soldy**
   - Diferentes expresiones según contexto
   - Animaciones de "pensando" durante llamadas a IA
   - Celebración al completar cálculos

2. **Mensajes Contextuales**
   - Diferentes saludos según hora del día
   - Mensajes basados en comportamiento del usuario
   - Sugerencias proactivas

3. **Integración Avanzada**
   - Notificaciones push
   - Historial persistente
   - Sincronización multi-dispositivo

4. **Analytics**
   - Tracking de interacciones con Soldy
   - Heatmaps de hover
   - A/B testing de animaciones

### 6.10 Conclusión

La implementación del widget flotante con Soldy transforma la experiencia de usuario de un chatbot funcional a un asistente virtual con personalidad. Las múltiples animaciones coordinadas, el diseño responsive y la atención al detalle en cada interacción crean una experiencia memorable que diferencia a SOLDASUR de la competencia.

El personaje de Soldy humaniza la tecnología y hace que los usuarios se sientan más cómodos al interactuar con el sistema, aumentando significativamente el engagement y la satisfacción del cliente.
