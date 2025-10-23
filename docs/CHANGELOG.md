# Changelog - SOLDASUR 2025

Todos los cambios notables del proyecto serán documentados en este archivo.

---

## [2.0.0] - 2025-10-15

### 🚀 Versión Standalone con Ollama

#### ✨ Agregado

#### 🔄 Cambiado
  - De: `https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash`
  - A: `http://localhost:11434/api/chat`
  - De: Formato Gemini con `contents` y `parts`
  - A: Formato Ollama con `messages` estándar
  - De: "Integrado con Google Gemini"
  - A: "Integrado con Ollama (Llama 3.2)"
  - Eliminada: `GEMINI_API_KEY`
  - Agregadas: `OLLAMA_URL` y `OLLAMA_MODEL`

#### 🗑️ Eliminado

#### 🐛 Corregido

#### 📝 Archivos Modificados

#### 🎯 Beneficios

---

## [1.0.0] - 2025-10-11


#### ✨ Agregado
- **Orquestador inteligente** (`app/orchestrator.py`)
- **Motor experto refactorizado** (`app/expert_engine.py`)
- **Interfaz unificada** (`app/chat_unified.html`)
- **Clasificador de intenciones** con 6 tipos:
  - GUIDED_CALCULATION
  - FREE_QUERY
  - PRODUCT_SEARCH
  - HYBRID
  - CLARIFICATION
- **Contexto unificado** compartido entre motores
- **Enriquecimiento mutuo** entre sistema experto y RAG
- **Indicadores de modo** (Experto / Chat / Híbrido)
- **Selector de modo** con 3 botones
- **Sugerencias inteligentes** de cambio de modo

#### 🔄 Cambiado
- **Arquitectura:**
  - A: Frontend → API → Orquestador → Motores
- **API principal** (`app/main.py`) con nuevos endpoints
- **Modelos de datos** actualizados con campos adicionales
- **Flujo de conversación** más fluido y natural
#### 📝 Archivos Creados
1. `app/orchestrator.py` (473 líneas)
2. `app/expert_engine.py` (448 líneas)

#### 🎯 Características
- ✅ Contexto compartido y persistente
- ✅ Arquitectura modular y escalable

---

## [0.9.0] - 2025-09-XX

### 🔧 Versión Beta Inicial

#### ✨ Agregado
- Sistema experto básico con flujo guiado
- Sistema RAG con búsqueda vectorial (FAISS)
- Integración con OpenAI GPT-4
- Base de conocimiento de productos PEISA
- Interfaz de chat básica
- API REST con FastAPI
- Cálculo de carga térmica

#### 📝 Archivos Base
- `app/app.py` - Sistema experto original
- `query/query.py` - Sistema RAG original
- `app/chat.html` - Interfaz básica
- `app/peisa_advisor_knowledge_base.json` - Base de conocimiento

---

## Formato

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

### Tipos de cambios
- **✨ Agregado** - Para nuevas funcionalidades
- **🔄 Cambiado** - Para cambios en funcionalidades existentes
- **🗑️ Eliminado** - Para funcionalidades eliminadas
- **🐛 Corregido** - Para corrección de bugs
- **🔒 Seguridad** - Para vulnerabilidades de seguridad

---

**Proyecto:** SOLDASUR 2025 - Asistente Inteligente Soldy  
**Equipo:** Cussi Nicolás, Biason Franco, Bolaña Silvia, Luna Luciano  
**Institución:** Prácticas Profesionalizantes II – 2° Cuatrimestre 2025
