# SoldaSur IA Chatbot  

**Chatbot inteligente para asesoramiento en sistemas de calefacción**  

Proyecto desarrollado en el marco de **Prácticas Profesionalizantes II – 2° Cuatrimestre 2025**, orientado al diseño de un asistente conversacional capaz de brindar soporte técnico y asesoramiento automatizado a clientes y operarios del sector calefacción.

## 🚀 Versiones Disponibles

### 🌐 Versión Standalone con Ollama (v2.0) - **RECOMENDADA**
- ✅ **100% Local** - Sin dependencias de APIs externas
- ✅ **Privacidad total** - Procesamiento en tu máquina
- ✅ **Costo cero** - Sin gastos por uso
- ✅ **Modelo:** Llama 3.2 (3B)
- 📄 **[Ver documentación completa del chatbot](docs/CHATBOT_SOLDY.md)** ⭐
- 📄 [Ver documentación técnica](docs/README_STANDALONE_OLLAMA.md)

### 🔧 Versión Backend Python (v1.0)
- Sistema híbrido con backend FastAPI
- RAG + Sistema Experto
- Requiere servidor Python + entorno virtual
- 📄 [Ver documentación](docs/PASOS.md)

**Instalación rápida:**
```bash
# 1. Crear entorno virtual
python -m venv venv

# 2. Activar (Windows)
venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Iniciar servidor
python -m uvicorn app.main:app --reload
```

---

## Equipo 2 – PP2 SOLDASUR 2C 2025  

**Integrantes:**

Cussi Nicolás  Biason Franco  
Bolaña Silvia  Luna Luciano

---

### Metodología de Trabajo
El equipo trabajará bajo una metodología **Àgil (Scrum)**, organizando el desarrollo en **3 sprints** principales.  
Cada sprint incluirá:
- **Planificación:** definición de tareas y objetivos.  
- **Desarrollo:** ejecución y revisión del avance en Trello y GitHub.  
- **Cierre:** retrospectiva y entrega de los resultados parciales.
  
---

**Links del proyecto:**  
- 📁 [Google Drive](https://drive.google.com/drive/u/0/folders/1pU7Th3OKQLMJ6IEezuRPtt7Ufv3Yb6Xe)  
- 📋 [Tablero de Trello](https://trello.com/b/MdxyBFuU/equipo-2-pp2-soldasur-2c-2025)  

---

## 🏃 Inicio Rápido

### Requisitos
1. **Instalar Ollama:** https://ollama.ai
2. **Descargar modelo:**
   ```bash
   ollama pull llama3.2:3b
   ```
3. **Activar en Ollama Settings:** "Expose Ollama to the network"

### Ejecutar
```bash
# Opción 1: Abrir directamente
# Navegar a app/ y abrir soldasur2025.html

# Opción 2: Con servidor local
cd app
python -m http.server 8000
# Abrir: http://localhost:8000/soldasur2025.html
```

### Probar
1. Hacer clic en el botón flotante de Soldy (esquina inferior derecha)
2. Elegir una opción:
   -  **Guíame en un cálculo** - Flujo estructurado
   -  **Tengo una pregunta** - Chat libre con IA
   -  **Buscar productos** - Catálogo PEISA

---

## Objetivo del proyecto  

Desarrollar un **chatbot basado en IA** que pueda:  
- Responder consultas frecuentes sobre sistemas de calefacción.  
- Brindar asistencia técnica personalizada.  
- Sugerir soluciones o recomendaciones según el tipo de instalación o problema reportado. 
- Integrarse con bases de conocimiento y flujos conversacionales adaptativos.  

--

## Estructura del proyecto  


```
├── LICENSE
├── Makefile
├── README.md
├── requirements.txt
├── app/
│   ├── app.py
│   ├── main.py
│   ├── models.py
│   ├── orchestrator.py
│   ├── soldasur2025.html
│   ├── soldasur.js
│   ├── soldasur.css
│   ├── peisa_advisor_knowledge_base.json
│   ├── img/
│   ├── modules/
│   │   ├── chatbot/
│   │   │   ├── llm_wrapper.py
│   │   │   ├── rag_engine_v2.py
│   │   │   └── models/
│   │   ├── expert_system/
│   │   ├── expertSystem/
│   │   │   ├── expert_engine.py
│   │   │   ├── expertSystem.js
│   │   │   ├── models.py
│   │   │   └── product_loader.py
│   │   └── scraping/
│   │       ├── inspect_peisa.py
│   │       └── product_scraper.py
├── configs/
│   └── params.yaml
├── data/
│   └── products_catalog.json
├── docs/
├── embeddings/
│   └── products.faiss
├── images/
├── ingest/
│   └── ingest.py
├── models/
├── notebooks/
│   └── exploration.ipynb
├── query/
│   └── query.py
├── scripts/
│   └── test_embeddings.py
├── tests/
```

## Propuestas de Escalabilidad

Para potenciar el crecimiento y la robustez del sistema SoldaSur, se proponen las siguientes estrategias de escalabilidad y optimización:

- **Velocidad de respuesdtas:** Optimizar la velocidad de respuestas del Chatbot. 
- **Almacenamiento y análisis de datos de consultas:** Registrar las interacciones y consultas de los usuarios para su posterior análisis, permitiendo la implementación de campañas de email marketing, remarketing y segmentación avanzada de clientes.
- **Autenticación y personalización:** Incorporar mecanismos de inicio de sesión para personalizar la experiencia de compra, ofrecer recomendaciones basadas en el historial y facilitar la gestión de usuarios.
- **Asistente en el proceso de compra:** Integrar el chatbot con el flujo de checkout, guiando al usuario y mostrando imágenes, videos o tutoriales sobre el uso e instalación de productos.
- **Base de datos dinámica de productos consultados:** Desarrollar una base de datos que registre los productos más consultados (inicialmente calderas y radiadores), sirviendo como fuente para optimizaciones, análisis de demanda y gestión de inventario.
- **Sistema de feedback automático:** Permitir que los usuarios califiquen las respuestas del chatbot y del sistema experto, utilizando estos datos para mejorar los modelos y la base de conocimiento.
- **Motor de recomendaciones avanzado:** Implementar algoritmos de machine learning para sugerir productos complementarios, promociones personalizadas y anticipar necesidades del cliente.


---