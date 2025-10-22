# 🤖 Documentación Completa del Chatbot Soldy

## 📋 Índice
1. [Descripción General](#descripción-general)
2. [Arquitectura](#arquitectura)
3. [Características Principales](#características-principales)
4. [Funcionamiento Interno](#funcionamiento-interno)
5. [Configuración Técnica](#configuración-técnica)
6. [Sistema de Memoria](#sistema-de-memoria)
7. [Manejo de Consultas](#manejo-de-consultas)
8. [Evaluación y Métricas](#evaluación-y-métricas)
9. [Archivos del Sistema](#archivos-del-sistema)

---

## 📖 Descripción General

**Soldy** es el chatbot inteligente de PEISA-SOLDASUR, diseñado como un **asesor de ventas virtual** que ayuda a los clientes con consultas sobre sistemas de calefacción, productos y servicios.

### Objetivo Principal
Proporcionar respuestas **breves, empáticas y orientadas a ventas** que:
- Respondan las preguntas del cliente de forma clara
- Recomienden productos específicos del catálogo
- Dirijan a contacto comercial para precios y compras
- Mantengan un tono cálido y profesional

### Características Clave
- ✅ **100% Local** - Funciona con Ollama (sin APIs externas)
- ✅ **Respuestas breves** - 2-3 frases (20-30 palabras)
- ✅ **Memoria conversacional** - Recuerda las últimas 10 interacciones
- ✅ **Manejo inteligente de precios** - Redirige a contactos por ciudad
- ✅ **Tono argentino** - Usa vos/podés, cálido y cercano

---

## 🏗️ Arquitectura

### Componentes del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                    INTERFAZ DE USUARIO                       │
│  (soldasur2025.html + soldasur.js + soldasur.css)          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   MÓDULO CHATBOT                             │
│              (app/modules/chatbot/)                          │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  chatbot.js                                          │  │
│  │  - Gestión de conversación                          │  │
│  │  - Memoria conversacional                           │  │
│  │  - Detección de intenciones                         │  │
│  │  - Manejo de contactos por ciudad                   │  │
│  └──────────────────┬───────────────────────────────────┘  │
│                     │                                        │
│                     ▼                                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  llm_wrapper.py                                      │  │
│  │  - Wrapper de Ollama                                 │  │
│  │  - System prompt optimizado                          │  │
│  │  - Control de longitud de respuestas                 │  │
│  └──────────────────┬───────────────────────────────────┘  │
└────────────────────┼────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    OLLAMA (LLM)                              │
│              Modelo: llama3.2:3b                             │
│              Puerto: 11434                                   │
└─────────────────────────────────────────────────────────────┘
```

### Flujo de Interacción

```
Usuario escribe pregunta
         │
         ▼
chatbot.js detecta intención
         │
         ├─► ¿Es consulta de precio? ──► Pregunta ciudad ──► Muestra contactos
         │
         └─► Pregunta normal
                  │
                  ▼
         Prepara contexto conversacional
                  │
                  ▼
         Llama a Ollama vía API
                  │
                  ▼
         llm_wrapper.py genera respuesta
                  │
                  ▼
         Trunca y valida respuesta
                  │
                  ▼
         Detecta productos mencionados
                  │
                  ▼
         Muestra respuesta + productos
                  │
                  ▼
         Actualiza historial conversacional
```

---

## ⭐ Características Principales

### 1. **Respuestas Breves y Empáticas**

**Configuración:**
- Máximo: 2-3 frases (20-30 palabras)
- `max_tokens`: 80
- `max_words`: 30
- Tono: Cálido, empático, profesional

**Ejemplo:**
```
Usuario: "¿Qué caldera me recomendás para 80m²?"
Soldy: "Para 80m² te recomiendo la Prima Tec Smart, es eficiente 
        y perfecta para ese tamaño. ¿Querés saber más?"
```

### 2. **Memoria Conversacional**

El chatbot mantiene contexto entre preguntas:

**Características:**
- Historial de últimos 10 mensajes
- Resumen automático cuando se alcanza el límite
- Coherencia en respuestas de seguimiento

**Ejemplo:**
```
Usuario: "¿Qué caldera me recomendás?"
Soldy: "Te recomiendo la Prima Tec Smart, es eficiente."

Usuario: "¿Cuánto sale?"  [Recuerda que hablaban de Prima Tec]
Soldy: "Para precios de la Prima Tec Smart, ¿estás en Río Grande o Ushuaia?"
```

### 3. **Manejo Inteligente de Precios**

**Detección automática** de palabras clave:
- precio, cuánto sale, comprar, presupuesto, dónde consigo

**Flujo:**
1. Usuario pregunta por precio
2. Chatbot pregunta: "¿Estás en Río Grande o Ushuaia?"
3. Usuario responde con ciudad
4. Chatbot muestra contactos de la ciudad

**Datos de Contacto:**

**RÍO GRANDE:**
- Islas Malvinas 1950 — Tel. 02964 422350 — ventasrg@soldasur.com.ar
- Av. San Martín 366 — Tel. 02964 422131

**USHUAIA:**
- Héroes de Malvinas 4180 — Tel. 02901 436392 — ventasush@soldasur.com.ar
- Gobernador Paz 665 — Tel. 02901 430886

### 4. **Tono Argentino y Cercano**

**Características:**
- Usa vos/podés (no tú/puedes ni usted)
- Tono cálido y servicial
- Sin tecnicismos excesivos
- Directo al punto

**Ejemplos:**
- ✅ "Te recomiendo..." (no "Le recomiendo...")
- ✅ "¿Querés saber más?" (no "¿Quieres saber más?")
- ✅ "Podés usar..." (no "Puedes usar...")

---

## ⚙️ Funcionamiento Interno

### 1. **Procesamiento de Mensajes**

#### Paso 1: Recepción del mensaje
```javascript
// chatbot.js - handleChatInput()
const question = input.value.trim();
appendMessage('user', question);
```

#### Paso 2: Detección de intención
```javascript
// ¿Es respuesta de ciudad?
if (waitingForCity && question.includes('río grande')) {
    showContactInfo('riogrande');
    return;
}
```

#### Paso 3: Preparación del contexto
```javascript
// Agregar contexto conversacional
if (conversationContext) {
    systemPrompt += `\n\nCONTEXTO DE LA CONVERSACIÓN:\n${conversationContext}`;
}

// Agregar historial de mensajes
conversationHistory.push({
    role: 'user',
    content: userMessage
});
```

#### Paso 4: Llamada a Ollama
```javascript
const response = await fetch('http://localhost:11434/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        model: 'llama3.2:3b',
        messages: conversationHistory,
        stream: false,
        options: {
            temperature: 0.7,
            num_predict: 80  // Límite de tokens
        }
    })
});
```

#### Paso 5: Procesamiento de respuesta
```javascript
const assistantMessage = data.message.content;

// Agregar al historial
conversationHistory.push({
    role: 'assistant',
    content: assistantMessage
});

// Detectar si pregunta por ciudad
if (assistantMessage.includes('Río Grande o Ushuaia')) {
    waitingForCity = true;
}

// Mostrar respuesta
appendMessage('system', assistantMessage);
```

### 2. **Sistema de Memoria**

#### Variables de Estado
```javascript
const conversationHistory = [];           // Últimos 10 mensajes
const MAX_HISTORY_LENGTH = 10;            // Límite de historial
let conversationContext = '';             // Resumen de contexto
let waitingForCity = false;               // Esperando respuesta de ciudad
```

#### Actualización de Contexto
```javascript
function updateConversationContext() {
    // Cuando se alcanza el límite, crear resumen
    if (conversationHistory.length >= MAX_HISTORY_LENGTH) {
        // Extraer temas clave y productos mencionados
        conversationContext = `Temas tratados: ${temas}
                               Productos recomendados: ${productos}`;
        
        // Mantener solo últimos 5 mensajes
        conversationHistory.splice(0, conversationHistory.length - 5);
    }
}
```

#### Reset Manual
```javascript
function resetChatHistory() {
    conversationHistory.length = 0;
    conversationContext = '';
    waitingForCity = false;
}
```

### 3. **Control de Longitud de Respuestas**

#### En el Frontend (chatbot.js)
```javascript
options: {
    temperature: 0.7,
    num_predict: 80  // Máximo 80 tokens
}
```

#### En el Backend (llm_wrapper.py)
```python
def generate(self, question: str, max_tokens: int = 80) -> str:
    response = ollama.generate(
        model=self.model,
        prompt=prompt,
        system=self.system_prompt,
        options={
            'temperature': 0.3,
            'num_predict': max_tokens,  # Límite de tokens
            'stop': ['\n']  # Parar en salto de línea
        }
    )
    
    # Truncar a max_words
    answer = self._truncate_to_brief(response['response'], max_words=30)
    return answer

def _truncate_to_brief(self, text: str, max_words: int = 30) -> str:
    words = text.split()
    if len(words) <= max_words:
        return text
    
    # Buscar primer punto antes de max_words
    for i, char in enumerate(text):
        if char in ['.', '?', '!']:
            sentence = text[:i+1].strip()
            if len(sentence.split()) >= 10:
                return sentence
    
    # Si no hay punto, truncar a max_words
    return ' '.join(words[:max_words]) + '.'
```

---

## 🔧 Configuración Técnica

### System Prompt (chatbot.js)

```javascript
let systemPrompt = `Eres Soldy, asesor de ventas de PEISA-SOLDASUR. 
Tu objetivo es ayudar con calidez y profesionalismo.

REGLAS DE ORO:
1. ✅ Respuestas BREVES: Máximo 2-3 frases cortas (20-30 palabras total)
2. ✅ Tono CÁLIDO y HUMANO: Como un asesor real, empático y servicial
3. ✅ DIRECTO AL PUNTO: Sin rodeos ni explicaciones largas
4. ✅ Recomienda 1 producto específico por nombre cuando sea relevante
5. ✅ COHERENCIA: Recuerda lo que el cliente ya preguntó

🚫 NUNCA MENCIONES PRECIOS, COSTOS O MONTOS
Si preguntan por precio/compra/presupuesto, responde:
"Para precios y compras, ¿estás en Río Grande o Ushuaia?"

EJEMPLOS:
❌ MAL: "Para calentar tu hogar eficientemente, especialmente con un perro 
         como Rufus que necesita un ambiente acogedor, te recomiendo 
         considerar un sistema de calefacción completo..."
✅ BIEN: "Podés usar radiadores Broen, son eficientes y fáciles de mantener. 
          Si querés saber precios, te paso el contacto según tu ciudad."

Español argentino, vos/podés, tono cercano.`;
```

### System Prompt (llm_wrapper.py)

```python
self.system_prompt = """Eres Soldy, asesor de ventas de PEISA-SOLDASUR. 
Tu objetivo es ayudar con calidez y profesionalismo.

REGLAS DE ORO:
✅ Respuestas BREVES: Máximo 2-3 frases cortas (20-30 palabras total)
✅ Tono CÁLIDO y HUMANO: Como un asesor real, empático y servicial
✅ DIRECTO AL PUNTO: Sin rodeos ni explicaciones largas
✅ Recomienda 1 producto específico por nombre cuando sea relevante
✅ COHERENCIA: Recuerda lo que el cliente ya preguntó
✅ Español argentino: Usá vos/podés, tono cercano

🚫 NUNCA MENCIONES PRECIOS, COSTOS O MONTOS
Si preguntan por precio/compra/presupuesto/dónde consigo, responde:
"Para precios y compras, ¿estás en Río Grande o Ushuaia?"

EJEMPLOS:
❌ MAL: "Para calentar tu hogar eficientemente, especialmente con un perro 
         como Rufus que necesita un ambiente acogedor, te recomiendo 
         considerar un sistema de calefacción completo..."
✅ BIEN: "Podés usar radiadores Broen, son eficientes y fáciles de mantener. 
          Si querés saber precios, te paso el contacto según tu ciudad."

✗ No inventes datos técnicos
✗ No recomiendes productos fuera del catálogo
✗ No des explicaciones largas o técnicas
✗ No repitas información
- TERMINA SIEMPRE CON PUNTO FINAL (.)"""
```

### Parámetros de Ollama

```javascript
// chatbot.js
{
    model: 'llama3.2:3b',
    temperature: 0.7,        // Creatividad moderada
    num_predict: 80,         // Máximo 80 tokens
    stream: false            // Respuesta completa, no streaming
}
```

```python
# llm_wrapper.py
{
    'temperature': 0.3,      # Bajo para respuestas determinísticas
    'num_predict': 80,       # Máximo 80 tokens
    'top_p': 0.7,           # Control de diversidad
    'top_k': 20,            # Vocabulario limitado
    'repeat_penalty': 1.3,  # Penaliza repeticiones
    'num_ctx': 1024,        # Contexto limitado
    'stop': ['\n']          # Parar en salto de línea
}
```

---

## 💾 Sistema de Memoria

### Estructura del Historial

```javascript
conversationHistory = [
    {
        role: 'user',
        content: '¿Qué caldera me recomendás?'
    },
    {
        role: 'assistant',
        content: 'Te recomiendo la Prima Tec Smart, es eficiente.'
    },
    {
        role: 'user',
        content: '¿Cuánto sale?'
    },
    {
        role: 'assistant',
        content: 'Para precios de la Prima Tec Smart, ¿estás en Río Grande o Ushuaia?'
    }
    // ... hasta 10 mensajes
];
```

### Gestión del Contexto

```javascript
// Cuando se alcanza el límite
if (conversationHistory.length >= MAX_HISTORY_LENGTH) {
    // Crear resumen
    conversationContext = `
        Temas tratados: calefacción para 80m², calderas
        Productos recomendados: Prima Tec Smart
        Última consulta: precio
    `;
    
    // Mantener solo últimos 5 mensajes
    conversationHistory.splice(0, 5);
}
```

### Persistencia

- **Durante la sesión**: El historial se mantiene en memoria
- **Navegación**: `goBack()` NO resetea el historial
- **Reset manual**: Botón "Nueva conversación" (aparece después de 2 mensajes)

---

## 🎯 Manejo de Consultas

### Tipos de Consultas

#### 1. **Consulta de Producto**
```
Usuario: "¿Qué caldera me recomendás para 80m²?"
Soldy: "Para 80m² te recomiendo la Prima Tec Smart, es eficiente 
        y perfecta para ese tamaño."
```

#### 2. **Consulta de Precio**
```
Usuario: "¿Cuánto sale la Prima Tec Smart?"
Soldy: "Para precios y compras, ¿estás en Río Grande o Ushuaia?"

Usuario: "Río Grande"
Soldy: [Muestra contactos de Río Grande]
```

#### 3. **Consulta Técnica**
```
Usuario: "¿Cómo funciona el sistema de condensación?"
Soldy: "El sistema de condensación aprovecha mejor el calor, 
        ahorrando gas. La Summa Condens usa esta tecnología."
```

#### 4. **Consulta Fuera de Tema**
```
Usuario: "¿Cuál es el mejor restaurante de Ushuaia?"
Soldy: "Jaja, no soy experto en restaurantes, pero sí en calefacción. 
        ¿Necesitás algo para tu hogar?"
```

### Detección de Intenciones

```javascript
// Palabras clave para precios
const keywords_precio = [
    'precio', 'cuánto', 'sale', 'cuesta', 'vale',
    'comprar', 'presupuesto', 'dónde consigo'
];

// Detección en la respuesta del LLM
if (response.includes('Río Grande o Ushuaia')) {
    waitingForCity = true;
}

// Detección de respuesta de ciudad
if (waitingForCity) {
    if (question.includes('río grande') || question.includes('rg')) {
        showContactInfo('riogrande');
    } else if (question.includes('ushuaia') || question.includes('ush')) {
        showContactInfo('ushuaia');
    }
}
```

---

## 📊 Evaluación y Métricas

### Sistema de Evaluación

El chatbot incluye un sistema completo de evaluación con 4 métricas:

#### 1. **Detección de Intención** (1-5)
¿Identifica correctamente lo que el usuario necesita?

#### 2. **Relevancia** (1-5)
¿La respuesta es pertinente y útil?

#### 3. **Claridad** (1-5)
¿Es clara, concisa y fácil de entender?

#### 4. **Tono** (1-5)
¿Es cálido, empático y profesional?

### Ejecución de Evaluación

```bash
cd tests
python test_chatbot_evaluation.py
```

### Resultados Actuales

```
📊 RESUMEN GENERAL
================================================================================

📈 Promedios por Métrica:
  • Detección de Intención: 2.25/5  ⚠️ Necesita mejora
  • Relevancia: 4.00/5               ✅ Bueno
  • Claridad: 4.00/5                 ✅ Bueno
  • Tono: 3.62/5                     ⚠️ Aceptable

  ⭐ PROMEDIO GENERAL: 3.47/5

  ⚠️ ACEPTABLE

💡 Recomendaciones:
  • Mejorar detección de intención con más keywords
  • Reforzar uso de español argentino (vos/podés)
```

📖 **[Ver documentación completa de evaluación](COMO_EVALUAR_CHATBOT.md)**

---

## 📁 Archivos del Sistema

### Estructura de Archivos

```
pp2-soldasur-2c-2025/
├── app/
│   ├── soldasur2025.html          # Interfaz principal
│   ├── soldasur.js                # Orquestador de la aplicación
│   ├── soldasur.css               # Estilos
│   └── modules/
│       └── chatbot/
│           ├── chatbot.js         # Lógica del chatbot
│           └── llm_wrapper.py     # Wrapper de Ollama
├── tests/
│   ├── test_chatbot_evaluation.py # Script de evaluación
│   └── README_EVALUACION.md       # Guía de evaluación
└── docs/
    ├── CHATBOT_SOLDY.md           # Esta documentación
    ├── COMO_EVALUAR_CHATBOT.md    # Guía de evaluación
    └── evaluacion_chatbot.md      # Plantilla de evaluación
```

### Archivos Principales

#### 1. **chatbot.js** (Frontend)
- Gestión de conversación
- Memoria conversacional
- Detección de intenciones
- Manejo de contactos por ciudad
- Integración con Ollama

**Líneas clave:**
- L5-11: Variables de configuración
- L13-21: Función `startChatbot()`
- L30-82: Función `showContactInfo()`
- L84-112: Función `showChatInput()`
- L114-158: Función `handleChatInput()`
- L160-234: Función `callOllama()`

#### 2. **llm_wrapper.py** (Backend)
- Wrapper de Ollama
- System prompt optimizado
- Control de longitud
- Truncamiento inteligente

**Líneas clave:**
- L10-46: Inicialización y system prompt
- L48-108: Función `generate()`
- L110-141: Función `_truncate_to_brief()`

#### 3. **soldasur.js** (Orquestador)
- Navegación entre modos
- Gestión del widget flotante
- Helpers compartidos

**Funciones compartidas:**
- `appendMessage()`: Agregar mensajes al chat
- `scrollToBottom()`: Scroll automático
- `renderOptions()`: Renderizar opciones

---

## 🚀 Inicio Rápido

### Requisitos Previos

1. **Ollama instalado**: https://ollama.ai
2. **Modelo descargado**:
   ```bash
   ollama pull llama3.2:3b
   ```
3. **Ollama corriendo**: Verificar con `ollama list`

### Ejecutar

```bash
# Opción 1: Abrir directamente
# Navegar a app/ y abrir soldasur2025.html en el navegador

# Opción 2: Con servidor local
cd app
python -m http.server 8000
# Abrir: http://localhost:8000/soldasur2025.html
```

### Probar

1. Hacer clic en el botón flotante de Soldy (esquina inferior derecha)
2. Elegir "Tengo una pregunta"
3. Escribir una pregunta
4. Ver la respuesta del chatbot

---

## 🔧 Solución de Problemas

### Error: "Connection refused"

**Causa**: Ollama no está corriendo

**Solución**:
```bash
ollama serve
```

### Respuestas muy largas

**Causa**: `num_predict` muy alto

**Solución**: Ajustar en `chatbot.js`:
```javascript
num_predict: 80  // Reducir si es necesario
```

### Respuestas cortadas

**Causa**: `num_predict` muy bajo

**Solución**: Aumentar en `chatbot.js`:
```javascript
num_predict: 100  // Aumentar si es necesario
```

### No detecta consultas de precio

**Causa**: Falta keyword

**Solución**: Agregar en system prompt o en detección manual

---

## 📚 Referencias

- **[Evaluación del Chatbot](COMO_EVALUAR_CHATBOT.md)** - Sistema de métricas
- **[Plantilla de Evaluación](evaluacion_chatbot.md)** - Evaluación manual
- **[README Principal](../README.md)** - Información general del proyecto
- **[Ollama Documentation](https://ollama.ai/docs)** - Documentación de Ollama

---

## 📝 Changelog

### Versión 2.0 (Actual)
- ✅ Respuestas breves (2-3 frases, 20-30 palabras)
- ✅ Memoria conversacional (últimos 10 mensajes)
- ✅ Manejo inteligente de precios por ciudad
- ✅ Tono argentino (vos/podés)
- ✅ Sistema de evaluación con 4 métricas
- ✅ Documentación completa

### Versión 1.0
- Respuestas largas (30-40 palabras)
- Sin memoria conversacional
- Sin manejo de precios
- Tono formal

---

## 👥 Equipo

**Equipo 2 – PP2 SOLDASUR 2C 2025**

- Cussi Nicolás
- Biason Franco
- Bolaña Silvia
- Luna Luciano

---

## 📄 Licencia

MIT License - Copyright (c) 2025 Equipo Soldasur PP2
