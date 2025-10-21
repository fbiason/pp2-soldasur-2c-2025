# Changelog - SOLDASUR 2025

Todos los cambios notables del proyecto serán documentados en este archivo.

---

## [2.0.0] - 2025-10-15

### 🚀 Versión Standalone con Ollama

#### ✨ Agregado
- **Integración completa con Ollama** para procesamiento de lenguaje natural local
- **Modelo Llama 3.2 (3B)** como motor de IA principal
- **Versión standalone** que funciona sin backend Python
- **Catálogo de productos PEISA** integrado en el prompt del sistema
- **Detección inteligente de productos** mencionados en respuestas de IA
- **Sistema de historial de conversación** para mantener contexto
- **Documentación completa** en `docs/README_STANDALONE_OLLAMA.md`

#### 🔄 Cambiado
- **Migración de Gemini a Ollama:**
  - De: `https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash`
  - A: `http://localhost:11434/api/chat`
- **Formato de API:**
  - De: Formato Gemini con `contents` y `parts`
  - A: Formato Ollama con `messages` estándar
- **Banner de la aplicación:**
  - De: "Integrado con Google Gemini"
  - A: "Integrado con Ollama (Llama 3.2)"
- **Configuración:**
  - Eliminada: `GEMINI_API_KEY`
  - Agregadas: `OLLAMA_URL` y `OLLAMA_MODEL`

#### 🗑️ Eliminado
- Dependencia de API key de Google Gemini
- Dependencia de conexión a internet para IA
- Costos por uso de APIs externas

#### 🐛 Corregido
- Error 404 con modelo `gemini-1.5-flash` en versión v1beta
- Problemas de CORS con APIs externas

#### 📝 Archivos Modificados
- `app/soldasur.js` - Implementación completa de Ollama
- `app/soldasur2025.html` - Actualización del banner
- `README.md` - Agregada sección de versiones y guía rápida
- `docs/README_STANDALONE_OLLAMA.md` - Nueva documentación completa

#### 🎯 Beneficios
- ✅ **100% Local** - Sin dependencias externas
- ✅ **Privacidad total** - Datos no salen de la máquina
- ✅ **Costo cero** - Sin gastos por uso
- ✅ **Offline** - Funciona sin internet (después de descargar modelo)
- ✅ **Rápido** - Respuestas en 1-5 segundos con hardware moderno

---

## [1.0.0] - 2025-10-11

### 🎉 Sistema Híbrido Unificado

#### ✨ Agregado
- **Orquestador inteligente** (`app/orchestrator.py`)
- **Motor experto refactorizado** (`app/expert_engine.py`)
- **Motor RAG refactorizado** (`app/rag_engine.py`)
- **Interfaz unificada** (`app/chat_unified.html`)
- **Clasificador de intenciones** con 6 tipos:
  - GUIDED_CALCULATION
  - FREE_QUERY
  - PRODUCT_SEARCH
  - HYBRID
  - SWITCH_MODE
  - CLARIFICATION
- **Contexto unificado** compartido entre motores
- **Enriquecimiento mutuo** entre sistema experto y RAG
- **Panel de contexto** visual en la interfaz
- **Indicadores de modo** (Experto / Chat / Híbrido)
- **Selector de modo** con 3 botones
- **Sugerencias inteligentes** de cambio de modo

#### 🔄 Cambiado
- **Arquitectura:**
  - De: Frontend → API → Sistema Experto ⟷ Sistema RAG
  - A: Frontend → API → Orquestador → Motores
- **API principal** (`app/main.py`) con nuevos endpoints
- **Modelos de datos** actualizados con campos adicionales
- **Flujo de conversación** más fluido y natural

#### 📝 Archivos Creados
1. `app/orchestrator.py` (473 líneas)
2. `app/expert_engine.py` (448 líneas)
3. `app/rag_engine.py` (345 líneas)
4. `app/chat_unified.html` (498 líneas)
5. `docs/PASOS.md` - Documentación completa del proceso

#### 🎯 Características
- ✅ Clasificación de intenciones en tiempo real
- ✅ Enrutamiento dinámico entre motores
- ✅ Fusión inteligente de respuestas
- ✅ Contexto compartido y persistente
- ✅ Experiencia de usuario fluida
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
