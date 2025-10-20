# SOLDASUR 2025 - Versión Standalone con Ollama

## 📋 Resumen Ejecutivo

Versión **standalone** del asistente inteligente Soldy para SOLDASUR S.A., completamente funcional en el navegador con integración local de **Ollama** para procesamiento de lenguaje natural.

**Fecha de actualización:** 15 de Octubre, 2025  
**Versión:** SOLDASUR 2025 v2.0 - Standalone  
**Estado:** ✅ Operativo con Ollama

---

## 🎯 Características Principales

### ✨ Funcionalidades
- **Sistema Experto Guiado**: Flujo paso a paso para cálculo de calefacción
- **Chat Libre con IA**: Consultas abiertas procesadas por Ollama (Llama 3.2)
- **Catálogo de Productos**: Navegación por categorías de productos PEISA
- **100% Local**: Sin dependencias de APIs externas o servicios en la nube
- **Sin Backend**: Funciona directamente desde archivos HTML/JS

### 🤖 Integración con Ollama
- **Modelo:** Llama 3.2 (3B parámetros)
- **Endpoint:** `http://localhost:11434/api/chat`
- **Características:**
  - Procesamiento local y privado
  - Sin costos por uso
  - Respuestas rápidas
  - Contexto de conversación mantenido
  - Catálogo de productos integrado en el prompt

---

## 📁 Estructura de Archivos

```
app/
├── soldasur2025.html          # Página principal standalone
├── soldasur.js                # Lógica del chatbot con Ollama
├── soldasur.css               # Estilos del chatbot
└── img/
    ├── soldy.png              # Avatar del chatbot (botón flotante)
    └── soldy_head.png         # Imagen del chatbot (header)
```

---

## 🚀 Instalación y Configuración

### Requisitos Previos

1. **Ollama instalado**
   ```bash
   # Descargar desde: https://ollama.ai
   # O instalar con:
   curl -fsSL https://ollama.ai/install.sh | sh
   ```

2. **Modelo Llama 3.2 descargado**
   ```bash
   ollama pull llama3.2:3b
   ```

3. **Ollama expuesto a la red**
   - Abrir Ollama
   - Ir a Settings
   - Activar "Expose Ollama to the network"

### Verificar Instalación

```bash
# Verificar que Ollama está corriendo
ollama list

# Debería mostrar:
# NAME              ID              SIZE      MODIFIED
# llama3.2:3b       a80c4f17acd5    2.0 GB    X days ago
```

---

## 💻 Uso

### Opción 1: Abrir directamente
1. Navegar a la carpeta `app/`
2. Abrir `soldasur2025.html` en el navegador
3. El chatbot estará disponible en la esquina inferior derecha

### Opción 2: Servidor local (recomendado)
```bash
# Con Python
cd app
python -m http.server 8000

# Con Node.js
npx http-server app -p 8000

# Acceder a:
http://localhost:8000/soldasur2025.html
```

---

## 🎨 Modos de Interacción

### 1.  Guíame en un cálculo
Flujo estructurado paso a paso:
1. Tipo de calefacción (Piso radiante / Radiadores / Calderas)
2. Superficie en m²
3. Zona geográfica (Norte / Centro / Sur)
4. Nivel de aislación (Buena / Regular / Mala)
5. **Resultado:** Carga térmica + Productos recomendados

### 2. 💬 Tengo una pregunta
Chat libre con Ollama:
- Consultas sobre productos
- Información técnica
- Comparaciones
- Recomendaciones personalizadas
- **Ollama procesa** con contexto del catálogo PEISA

### 3. 📦 Buscar productos
Navegación por categorías:
- Calderas (11 productos)
- Radiadores (8 productos)
- Termotanques (3 productos)
- Calefones (2 productos)
- Toalleros (6 productos)
- Climatizadores (3 productos)
- Termostatos (2 productos)

---

## ⚙️ Configuración Técnica

### Variables en `soldasur.js`

```javascript
/* Configuración Ollama */
const OLLAMA_URL = 'http://localhost:11434/api/chat';
const OLLAMA_MODEL = 'llama3.2:3b';
```

### Personalizar Modelo

Para usar otro modelo de Ollama:

```javascript
// Opciones disponibles:
const OLLAMA_MODEL = 'llama3.2:3b';     // Rápido, 2GB
const OLLAMA_MODEL = 'llama3.1:8b';     // Balanceado, 4.7GB
const OLLAMA_MODEL = 'mistral:7b';      // Alternativa, 4.1GB
const OLLAMA_MODEL = 'gemma2:9b';       // Google, 5.4GB
```

### Ajustar Parámetros de IA

```javascript
options: {
    temperature: 0.7,        // Creatividad (0.0-1.0)
    num_predict: 500        // Máximo de tokens
}
```

---

## 🔧 Personalización

### Cambiar Productos

Editar el array `peisaProducts` en `soldasur.js`:

```javascript
const peisaProducts = [
    {
        model: "Nombre del Producto",
        family: "Categoría",
        category: "Subcategoría",
        description: "Descripción breve",
        url: "https://url-del-producto.com"
    },
    // ... más productos
];
```

### Modificar System Prompt

En la función `callOllama()`, editar:

```javascript
const systemPrompt = `Eres un asistente experto en productos de calefacción...
// Personalizar instrucciones aquí
`;
```

### Cambiar Estilos

Editar `soldasur.css` para personalizar:
- Colores del chatbot
- Tamaño de la ventana
- Animaciones
- Tipografía

---

## 🐛 Solución de Problemas

### Error: "Error en la API de Ollama"

**Causa:** Ollama no está corriendo o no está expuesto a la red

**Solución:**
1. Verificar que Ollama está activo:
   ```bash
   ollama list
   ```
2. Verificar configuración en Ollama Settings:
   - ✅ "Expose Ollama to the network" debe estar activado
3. Reiniciar Ollama

### Error: CORS

**Causa:** Restricciones de seguridad del navegador

**Solución:**
- Usar un servidor local (no abrir el HTML directamente)
- Ollama debe estar expuesto a la red

### Respuestas lentas

**Causa:** Modelo muy grande o hardware limitado

**Solución:**
1. Usar modelo más pequeño:
   ```bash
   ollama pull llama3.2:3b
   ```
2. Reducir `num_predict` en la configuración

### El chatbot no responde

**Verificar:**
1. Console del navegador (F12) para errores
2. Ollama está corriendo: `ollama list`
3. Puerto correcto: `http://localhost:11434`
4. Modelo descargado: `ollama list`

---

## 📊 Arquitectura Técnica

### Flujo de Datos

```
Usuario → Frontend (HTML/JS)
           ↓
    Clasificación de Intención
           ↓
    ┌──────┴──────┐
    ↓             ↓
Sistema Experto   Ollama (Chat Libre)
    ↓             ↓
Cálculos +    Respuestas IA
Productos     + Productos
    ↓             ↓
    └──────┬──────┘
           ↓
    Renderizado UI
```

### Componentes JavaScript

```javascript
// Gestión de estado
conversationHistory = []  // Historial para Ollama
conversationStep = 0      // Paso actual del flujo experto
userInputs = {}          // Variables capturadas
contextData = {}         // Contexto visible al usuario

// Funciones principales
startConversation()      // Inicia el chat
handleOptionClick()      // Procesa selecciones
handleChatInput()        // Procesa texto libre
callOllama()            // Llama a la API de Ollama
detectMentionedProducts() // Extrae productos mencionados
renderProducts()         // Muestra tarjetas de productos
```

---

## 🔐 Privacidad y Seguridad

### Ventajas de Ollama Local

✅ **100% Privado:** Los datos nunca salen de tu máquina  
✅ **Sin API Keys:** No se requieren credenciales externas  
✅ **Offline:** Funciona sin conexión a internet (después de descargar el modelo)  
✅ **Sin Límites:** No hay restricciones de uso o cuotas  
✅ **Cumplimiento:** Ideal para datos sensibles o regulaciones estrictas  

---

## 📈 Rendimiento

### Tiempos de Respuesta (Llama 3.2 3B)

| Hardware | Tiempo promedio |
|----------|----------------|
| CPU moderna | 2-5 segundos |
| GPU integrada | 1-3 segundos |
| GPU dedicada | 0.5-1 segundo |

### Consumo de Recursos

- **RAM:** ~4-6 GB (modelo + overhead)
- **Disco:** 2 GB (modelo)
- **CPU/GPU:** Variable según hardware

---

## 🚀 Mejoras Futuras

### Corto Plazo
- [ ] Streaming de respuestas (mostrar texto progresivamente)
- [ ] Historial de conversaciones persistente
- [ ] Exportar conversación a PDF
- [ ] Modo oscuro

### Medio Plazo
- [ ] Soporte para múltiples modelos
- [ ] Análisis de sentimiento
- [ ] Recomendaciones personalizadas basadas en historial
- [ ] Integración con sistema de cotizaciones

### Largo Plazo
- [ ] Fine-tuning del modelo con datos de SOLDASUR
- [ ] Multilenguaje (inglés, portugués)
- [ ] Integración con CRM
- [ ] Analytics de conversaciones

---

## 📞 Soporte

### Recursos
- **Documentación Ollama:** https://ollama.ai/docs
- **Modelos disponibles:** https://ollama.ai/library
- **Comunidad Ollama:** https://discord.gg/ollama

### Contacto
- **Proyecto:** SOLDASUR 2025
- **Desarrollador:** Franco Biason
- **Email:** franco.biason@gmail.com

---

## 📝 Changelog

### v2.0 - Standalone con Ollama (15/10/2025)
- ✅ Migración completa a Ollama local
- ✅ Eliminación de dependencias de APIs externas
- ✅ Optimización de prompts para Llama 3.2
- ✅ Mejora en detección de productos mencionados
- ✅ Actualización de documentación

### v1.0 - Sistema Híbrido (11/10/2025)
- ✅ Unificación de sistema experto y RAG
- ✅ Orquestador inteligente
- ✅ Interfaz unificada
- ✅ Integración con backend Python

---

## 📄 Licencia

Este proyecto es propiedad de **SOLDASUR S.A.** y está desarrollado para uso interno y demostración.

---

## 🎉 Conclusión

El asistente Soldy ahora funciona completamente con **Ollama**, proporcionando:

✅ **Autonomía total** - Sin dependencias externas  
✅ **Privacidad garantizada** - Procesamiento 100% local  
✅ **Costo cero** - Sin gastos por uso de APIs  
✅ **Rendimiento óptimo** - Respuestas rápidas con Llama 3.2 3B  
✅ **Escalabilidad** - Fácil cambio de modelos según necesidades  

**¡Listo para producción!** 🚀
