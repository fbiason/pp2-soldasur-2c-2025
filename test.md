# Testing - SoldaSur IA Chatbot

**Proyecto:** PP2 SOLDASUR 2C 2025

## Resumen

El chatbot SoldaSur es un asistente inteligente standalone que integra Ollama (Llama 3.2 3B) para procesamiento local de lenguaje natural. Cuenta con tres módulos principales: un sistema experto para cálculos de calefacción guiados, un chatbot conversacional con IA, y un catálogo de productos PEISA cargado dinámicamente desde JSON. La aplicación es 100% local, construida con HTML/JavaScript/Tailwind CSS, y se ejecuta en `http://localhost:8000` sin dependencias de backend activo.

Los cambios recientes incluyen la migración completa a Ollama eliminando la necesidad de APIs externas, modularización del código JavaScript en `app/modules/` (chatbot, expertSystem, scraping), implementación de catálogo dinámico desde `data/products_catalog.json`, y mejoras en la UI con panel de contexto, maximización de chat, y flujos de navegación optimizados. El sistema mantiene historial de conversación (máximo 10 mensajes) y permite transiciones fluidas entre los tres modos de operación.

## Checklist de Testing

**Pre-requisitos:**
- [ ] Ollama instalado y corriendo (`ollama list` debe mostrar `llama3.2:3b`)
- [ ] Archivo `data/products_catalog.json` presente
- [ ] Servidor local levantado: `cd app && python -m http.server 8000`

**Tests funcionales básicos:**
- [ ] Abrir/cerrar chatbot funciona correctamente
- [ ] Sistema experto calcula carga térmica (ej: 50m² × 120 (Sur) × 1.15 = 6,900W)
- [ ] Chatbot IA responde en <5 segundos con contexto coherente
- [ ] Catálogo carga productos (verificar en Console: "✅ Catálogo cargado")
- [ ] Navegación entre módulos mantiene contexto
- [ ] UI responsive en mobile (375px) y desktop

**Issues conocidos:**
- Chatbot puede responder preguntas fuera del dominio de calefacción
- Filtrado por categoría en catálogo pendiente de implementación
