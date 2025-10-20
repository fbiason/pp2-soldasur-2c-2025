# SoldaSur IA Chatbot  

**Chatbot inteligente para asesoramiento en sistemas de calefacción**  

Proyecto desarrollado en el marco de **Prácticas Profesionalizantes II – 2° Cuatrimestre 2025**, orientado al diseño de un asistente conversacional capaz de brindar soporte técnico y asesoramiento automatizado a clientes y operarios del sector calefacción.

## 🚀 Versiones Disponibles

### 🌐 Versión Standalone con Ollama (v2.0) - **RECOMENDADA**
- ✅ **100% Local** - Sin dependencias de APIs externas
- ✅ **Privacidad total** - Procesamiento en tu máquina
- ✅ **Costo cero** - Sin gastos por uso
- ✅ **Modelo:** Llama 3.2 (3B)
- 📄 [Ver documentación completa](docs/README_STANDALONE_OLLAMA.md)

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

## 🏃 Inicio Rápido (Versión Standalone)

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

---

## Estructura del proyecto  



    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
