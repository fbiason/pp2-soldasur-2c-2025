# Estructura Modular de SOLDASUR

## 📁 Estructura de Carpetas

```
app/
├── modules/
│   ├── chatbot/           # Módulo de Chatbot con IA
│   │   ├── chatbot.js
│   │   ├── llm_wrapper.py
│   │   └── rag_engine_v2.py
│   │
│   ├── expertSystem/      # Sistema Experto de Cálculos
│   │   ├── expertSystem.js
│   │   └── expert_engine.py
│   │
│   └── scraping/          # Catálogo y Scraping de Productos
│       ├── productCatalog.js
│       └── product_scraper.py
│
├── soldasur.js            # Orquestador principal
├── soldasur2025.html      # Interfaz web
├── soldasur.css           # Estilos
└── README_MODULOS.md      # Esta documentación
```

## 📦 Módulos del Sistema

El sistema ha sido separado en **3 módulos independientes** + 1 orquestador principal:

### 1. **modules/scraping/** - Catálogo y Scraping
📁 **Ubicación**: `app/modules/scraping/`

**productCatalog.js** (~11.6 KB)
- Array `peisaProducts` con todos los productos
- Función `renderProducts()` - Renderiza tarjetas de productos
- Función `showProductsByCategory()` - Filtra por categoría
- Función `showAllProducts()` - Muestra productos destacados
- Función `showCategoryMenu()` - Menú de categorías

**product_scraper.py**
- Script Python para scraping de productos PEISA
- Actualización automática del catálogo

### 2. **modules/expertSystem/** - Sistema Experto
📁 **Ubicación**: `app/modules/expertSystem/`

**expertSystem.js** (~6 KB)
- Variables: `conversationStep`, `userInputs`, `contextData`
- Función `startExpertSystem()` - Inicia el flujo guiado
- Función `askQuestion()` - Maneja el flujo paso a paso
- Función `calculateHeatingLoad()` - Calcula carga térmica
- Función `handleExpertSystemResponse()` - Procesa respuestas
- Función `createNumberInput()` - Input numérico para superficie
- Función `updateContextPanel()` - Actualiza panel de contexto

**expert_engine.py**
- Motor de reglas del sistema experto
- Lógica de cálculo de carga térmica en Python

### 3. **modules/chatbot/** - Chatbot con IA
📁 **Ubicación**: `app/modules/chatbot/`

**chatbot.js** (~7.3 KB)
- Configuración: `OLLAMA_URL`, `OLLAMA_MODEL`
- Array `conversationHistory` - Historial de conversación
- Función `startChatbot()` - Inicia modo chat
- Función `handleChatInput()` - Procesa input del usuario
- Función `callOllama()` - Llamada a API de Ollama
- Función `detectMentionedProducts()` - Detecta productos en respuestas
- Funciones `showLoadingIndicator()` / `hideLoadingIndicator()`
- **Configuración LLM**: Model `llama3.2:3b`, Temperature `0.7`, Max tokens `80`

**llm_wrapper.py**
- Wrapper Python para integración con LLM
- Gestión de prompts y respuestas

**rag_engine_v2.py**
- Motor RAG (Retrieval-Augmented Generation)
- Búsqueda semántica en base de conocimiento

### 4. **soldasur.js** - Orquestador Principal
📁 **Ubicación**: `app/soldasur.js` (~10.8 KB)

- Estado global de la aplicación
- Funciones de navegación (`toggleChat`, `goBack`, etc.)
- Función `startConversation()` - Menú principal
- Función `handleOptionClick()` - Router de opciones
- Funciones de renderizado UI (`renderOptions`, `appendMessage`, etc.)
- Helpers generales

## 🔗 Orden de Carga

Los scripts deben cargarse en este orden en `soldasur2025.html`:

```html
<script src="modules/scraping/productCatalog.js"></script>       <!-- 1º: Catálogo -->
<script src="modules/expertSystem/expertSystem.js"></script>     <!-- 2º: Sistema Experto -->
<script src="modules/chatbot/chatbot.js"></script>               <!-- 3º: Chatbot -->
<script src="soldasur.js"></script>                              <!-- 4º: Orquestador -->
```

## 🎯 Ventajas de la Modularización

✅ **Legibilidad**: Cada archivo tiene una responsabilidad clara  
✅ **Mantenibilidad**: Más fácil encontrar y modificar código específico  
✅ **Escalabilidad**: Se pueden agregar nuevos módulos sin afectar los existentes  
✅ **Debugging**: Errores más fáciles de localizar  
✅ **Colaboración**: Múltiples desarrolladores pueden trabajar en paralelo  
✅ **Organización**: Archivos agrupados por funcionalidad en carpetas dedicadas

## 📊 Comparación

| Antes | Después |
|-------|---------|
| 1 archivo de ~792 líneas | 4 archivos modulares |
| Todo mezclado en `/app` | Organizado en carpetas `/modules` |
| Difícil de navegar | Estructura clara por funcionalidad |
| Archivos JS y Python mezclados | Cada módulo con sus archivos relacionados |

## 🔧 Mantenimiento

- **Para modificar el catálogo**: `modules/scraping/productCatalog.js` o `product_scraper.py`
- **Para ajustar el sistema experto**: `modules/expertSystem/expertSystem.js` o `expert_engine.py`
- **Para cambiar el chatbot/LLM**: `modules/chatbot/chatbot.js`, `llm_wrapper.py` o `rag_engine_v2.py`
- **Para modificar la UI/navegación**: `soldasur.js` (raíz de app)

## 📝 Notas

- El archivo `soldasur.js.backup` contiene el código original por seguridad
- Todos los módulos comparten el DOM y pueden acceder a funciones globales
- Las variables de estado se mantienen en el orquestador principal
