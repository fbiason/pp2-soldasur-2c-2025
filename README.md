# SoldaSur IA Chatbot  

**Chatbot inteligente para asesoramiento en sistemas de calefacción**  

Proyecto desarrollado en el marco de **Prácticas Profesionalizantes II – 2° Cuatrimestre 2025**, orientado al diseño de un asistente conversacional capaz de brindar soporte técnico y asesoramiento automatizado a clientes y operarios del sector calefacción.

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
