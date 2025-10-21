# GLOSARIO TÉCNICO - Proyecto Soldasur

Este documento contiene los conceptos técnicos clave utilizados en el desarrollo del chatbot Soldy y el sistema de recomendación de productos PEISA-SOLDASUR.

---

## 📚 Conceptos de IA y Machine Learning

### Embeddings
**Definición:** Representaciones vectoriales numéricas de texto que capturan el significado semántico de palabras, frases o documentos en un espacio multidimensional.

**Ejemplo:**
```python
# Texto original
texto = "caldera de gas natural"

# Embedding (vector simplificado de 3 dimensiones)
embedding = [0.82, -0.45, 0.31]

# Textos similares tendrán vectores cercanos
texto2 = "calefactor a gas"
embedding2 = [0.79, -0.42, 0.28]  # Vectores cercanos = significado similar
```

**Uso en Soldasur:** Los embeddings se generan para el catálogo de productos y las consultas de usuarios, permitiendo búsquedas semánticas eficientes.

---

### FAISS (Facebook AI Similarity Search)
**Definición:** Biblioteca de Facebook para búsqueda eficiente de similitud en grandes conjuntos de vectores. Permite encontrar rápidamente los embeddings más cercanos a una consulta.

**Ejemplo:**
```python
import faiss
import numpy as np

# Crear índice FAISS
dimension = 384  # Dimensión de los embeddings
index = faiss.IndexFlatL2(dimension)

# Agregar vectores al índice
vectors = np.random.random((1000, dimension)).astype('float32')
index.add(vectors)

# Buscar los 5 vectores más similares
query = np.random.random((1, dimension)).astype('float32')
distances, indices = index.search(query, k=5)
```

**Uso en Soldasur:** El archivo `embeddings/products.faiss` almacena los embeddings del catálogo para búsquedas rápidas.

---

### LLM (Large Language Model)
**Definición:** Modelo de lenguaje de gran escala entrenado con enormes cantidades de texto para comprender y generar lenguaje natural.

**Ejemplo:**
```python
# Consulta al LLM
prompt = "¿Qué caldera recomiendas para 100m²?"

# Respuesta del LLM
respuesta = "Para 100m² te recomiendo la Prima Tec Smart 24kW, 
             ideal para calefacción eficiente en ese espacio."
```

**Uso en Soldasur:** Ollama con modelos como Llama o Mistral para generar respuestas conversacionales.

---

### RAG (Retrieval-Augmented Generation)
**Definición:** Técnica que combina recuperación de información con generación de texto. Primero busca documentos relevantes y luego genera respuestas basadas en esa información.

**Ejemplo:**
```python
# 1. RETRIEVAL: Buscar productos relevantes
query = "caldera para 80m²"
productos_relevantes = buscar_en_faiss(query)  # [Prima Tec Smart, Roca Victoria]

# 2. AUGMENTATION: Agregar contexto al prompt
contexto = f"Productos disponibles: {productos_relevantes}"

# 3. GENERATION: Generar respuesta con LLM
prompt = f"{contexto}\n\nPregunta: {query}"
respuesta = llm.generate(prompt)
```

**Uso en Soldasur:** El chatbot usa RAG para recomendar productos específicos del catálogo.

---

### Prompt Engineering
**Definición:** Técnica de diseñar y optimizar las instrucciones (prompts) que se dan a un LLM para obtener respuestas más precisas y útiles.

**Ejemplo:**
```javascript
// Prompt básico (menos efectivo)
const promptBasico = "Responde preguntas sobre calderas";

// Prompt optimizado (más efectivo)
const promptOptimizado = `
Eres Soldy, vendedor experto de PEISA-SOLDASUR.
OBJETIVO: VENDER productos en respuestas ULTRA CORTAS (80-120 caracteres).
SIEMPRE recomienda al menos 1 producto específico por nombre.
Formato: [Respuesta] + [Producto] + [Beneficio]
`;
```

**Uso en Soldasur:** El system prompt en `soldasur.js` está optimizado para respuestas de ventas cortas y efectivas.

---

## 🤖 Sistemas Inteligentes

### Sistema Experto
**Definición:** Sistema de IA basado en reglas que emula el razonamiento de un experto humano en un dominio específico. Usa una base de conocimiento y un motor de inferencia.

**Ejemplo:**
```javascript
// Base de conocimiento (reglas)
const reglas = {
  superficie_grande: {
    condicion: (datos) => datos.superficie > 150,
    recomendacion: "Caldera de alta potencia (>30kW)"
  },
  superficie_media: {
    condicion: (datos) => datos.superficie >= 80 && datos.superficie <= 150,
    recomendacion: "Caldera media potencia (20-30kW)"
  }
};

// Motor de inferencia
function recomendar(datos) {
  for (let regla of Object.values(reglas)) {
    if (regla.condicion(datos)) {
      return regla.recomendacion;
    }
  }
}

// Uso
const resultado = recomendar({ superficie: 100 });
// Output: "Caldera media potencia (20-30kW)"
```

**Uso en Soldasur:** El módulo `expertSystem.js` implementa reglas para recomendar calderas según superficie, tipo de gas, etc.

---

### Árbol de Decisión
**Definición:** Estructura de datos en forma de árbol donde cada nodo representa una pregunta o decisión, y las ramas representan las posibles respuestas.

**Ejemplo:**
```javascript
const arbolDecision = {
  pregunta: "¿Cuál es la superficie a calefaccionar?",
  opciones: [
    {
      condicion: "< 80m²",
      siguiente: {
        pregunta: "¿Tipo de gas?",
        opciones: [
          { condicion: "Natural", resultado: "Prima Tec Smart 18kW" },
          { condicion: "Envasado", resultado: "Roca Victoria 20" }
        ]
      }
    },
    {
      condicion: "> 150m²",
      resultado: "Prima Tec Smart 35kW"
    }
  ]
};
```

**Uso en Soldasur:** El sistema experto usa árboles de decisión para guiar las recomendaciones de productos.

---

## 🌐 Tecnologías Web

### Web Scraping
**Definición:** Técnica automatizada para extraer información de sitios web mediante programación.

**Ejemplo:**
```python
from selenium import webdriver
from bs4 import BeautifulSoup

# Inicializar navegador
driver = webdriver.Chrome()
driver.get("https://ejemplo.com/productos")

# Extraer datos
soup = BeautifulSoup(driver.page_source, 'html.parser')
productos = soup.find_all('div', class_='producto')

for producto in productos:
    nombre = producto.find('h2').text
    precio = producto.find('span', class_='precio').text
    print(f"{nombre}: {precio}")
```

**Uso en Soldasur:** El módulo `scraping` extrae información actualizada del catálogo de productos PEISA.

---

### API REST
**Definición:** Interfaz de programación de aplicaciones que usa HTTP para comunicación entre sistemas, siguiendo principios REST.

**Ejemplo:**
```python
from flask import Flask, jsonify, request

app = Flask(__name__)

# Endpoint GET
@app.route('/api/productos', methods=['GET'])
def obtener_productos():
    return jsonify({"productos": ["Prima Tec", "Roca Victoria"]})

# Endpoint POST
@app.route('/api/consulta', methods=['POST'])
def procesar_consulta():
    datos = request.json
    respuesta = chatbot.responder(datos['pregunta'])
    return jsonify({"respuesta": respuesta})
```

**Uso en Soldasur:** Flask expone endpoints para el chatbot y el sistema experto.

---

### WebSocket
**Definición:** Protocolo de comunicación bidireccional en tiempo real entre cliente y servidor sobre una única conexión TCP.

**Ejemplo:**
```javascript
// Cliente
const socket = new WebSocket('ws://localhost:8080');

socket.onmessage = (event) => {
  console.log('Mensaje recibido:', event.data);
};

socket.send('Hola desde el cliente');

// Servidor (Node.js)
const WebSocket = require('ws');
const wss = new WebSocket.Server({ port: 8080 });

wss.on('connection', (ws) => {
  ws.on('message', (message) => {
    ws.send(`Eco: ${message}`);
  });
});
```

**Uso en Soldasur:** Comunicación en tiempo real entre la interfaz del chatbot y el backend.

---

## 📊 Procesamiento de Datos

### CSV (Comma-Separated Values)
**Definición:** Formato de archivo de texto plano para almacenar datos tabulares, donde cada línea es un registro y las columnas se separan por comas.

**Ejemplo:**
```csv
id,nombre,precio,potencia,tipo_gas
1,Prima Tec Smart 24,45000,24kW,Natural
2,Roca Victoria 20,38000,20kW,Envasado
3,Peisa Diva 28,52000,28kW,Natural
```

```python
import pandas as pd

# Leer CSV
df = pd.read_csv('productos.csv')

# Filtrar productos
calderas_gas_natural = df[df['tipo_gas'] == 'Natural']
print(calderas_gas_natural)
```

**Uso en Soldasur:** `data/processed/products_mock.csv` almacena el catálogo procesado.

---

### Vectorización
**Definición:** Proceso de convertir texto u otros datos en vectores numéricos que pueden ser procesados por algoritmos de machine learning.

**Ejemplo:**
```python
from sentence_transformers import SentenceTransformer

# Modelo de vectorización
model = SentenceTransformer('all-MiniLM-L6-v2')

# Textos a vectorizar
textos = [
    "caldera de gas natural",
    "calefactor eléctrico",
    "termotanque solar"
]

# Generar embeddings
embeddings = model.encode(textos)
print(embeddings.shape)  # (3, 384) - 3 textos, 384 dimensiones
```

**Uso en Soldasur:** Se vectorizan descripciones de productos y consultas de usuarios para búsquedas semánticas.

---

## 🛠️ Herramientas y Frameworks

### Gradio
**Definición:** Framework de Python para crear interfaces web interactivas para modelos de machine learning de forma rápida y sencilla.

**Ejemplo:**
```python
import gradio as gr

def saludar(nombre):
    return f"¡Hola {nombre}!"

# Crear interfaz
interfaz = gr.Interface(
    fn=saludar,
    inputs=gr.Textbox(label="Tu nombre"),
    outputs=gr.Textbox(label="Saludo"),
    title="App de Saludos"
)

interfaz.launch()
```

**Uso en Soldasur:** Gradio proporciona la interfaz web del chatbot (aunque el proyecto usa principalmente JavaScript/HTML custom).

---

### Ollama
**Definición:** Herramienta para ejecutar modelos de lenguaje grandes (LLMs) localmente en tu computadora de forma sencilla.

**Ejemplo:**
```bash
# Instalar modelo
ollama pull llama2

# Ejecutar modelo
ollama run llama2

# Usar API
curl http://localhost:11434/api/generate -d '{
  "model": "llama2",
  "prompt": "¿Qué es una caldera?",
  "stream": false
}'
```

**Uso en Soldasur:** Ollama ejecuta el LLM localmente para generar respuestas del chatbot.

---

### LangChain
**Definición:** Framework para desarrollar aplicaciones con LLMs, facilitando la creación de cadenas de procesamiento, RAG, agentes y más.

**Ejemplo:**
```python
from langchain.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS

# Configurar LLM
llm = Ollama(model="llama2")

# Configurar retriever
vectorstore = FAISS.load_local("embeddings/products.faiss")
retriever = vectorstore.as_retriever()

# Crear cadena RAG
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff"
)

# Consultar
respuesta = qa_chain.run("¿Qué caldera recomiendas para 100m²?")
```

**Uso en Soldasur:** Potencial uso para orquestar el flujo RAG del chatbot.

---

## 🔧 Conceptos de Desarrollo

### Virtual Environment (venv)
**Definición:** Entorno aislado de Python que permite instalar paquetes específicos para un proyecto sin afectar el sistema global.

**Ejemplo:**
```bash
# Crear entorno virtual
python -m venv venv

# Activar (Windows)
venv\Scripts\activate

# Activar (Linux/Mac)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Desactivar
deactivate
```

**Uso en Soldasur:** El proyecto usa un venv para aislar las dependencias de Python.

---

### Git & GitHub
**Definición:** Git es un sistema de control de versiones distribuido. GitHub es una plataforma de hosting para repositorios Git.

**Ejemplo:**
```bash
# Inicializar repositorio
git init

# Agregar cambios
git add .
git commit -m "feat: agregar sistema experto"

# Subir a GitHub
git remote add origin https://github.com/usuario/repo.git
git push -u origin main

# Crear rama
git checkout -b feature/nueva-funcionalidad
```

**Uso en Soldasur:** Control de versiones del código y colaboración en equipo.

---

### Makefile
**Definición:** Archivo que define comandos automatizados para compilar, ejecutar y mantener un proyecto.

**Ejemplo:**
```makefile
# Makefile
.PHONY: install run test clean

install:
	pip install -r requirements.txt

run:
	python app/main.py

test:
	pytest tests/

clean:
	rm -rf __pycache__ *.pyc
```

```bash
# Ejecutar comandos
make install
make run
make test
```

**Uso en Soldasur:** Automatiza tareas comunes del proyecto como instalación y ejecución.

---

## 📈 Métricas y Evaluación

### Similitud Coseno
**Definición:** Métrica que mide la similitud entre dos vectores calculando el coseno del ángulo entre ellos. Valores cercanos a 1 indican alta similitud.

**Ejemplo:**
```python
import numpy as np

def similitud_coseno(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    return dot_product / (norm1 * norm2)

# Vectores de ejemplo
v1 = np.array([1, 2, 3])
v2 = np.array([2, 3, 4])

similitud = similitud_coseno(v1, v2)
print(f"Similitud: {similitud:.4f}")  # Output: 0.9926 (muy similares)
```

**Uso en Soldasur:** FAISS usa similitud coseno (o distancia L2) para encontrar productos relevantes.

---

### Token
**Definición:** Unidad básica de texto procesada por un LLM. Puede ser una palabra, parte de una palabra o un carácter.

**Ejemplo:**
```python
# Texto original
texto = "La caldera Prima Tec es excelente"

# Tokenización (ejemplo simplificado)
tokens = ["La", "cal", "dera", "Prima", "Tec", "es", "exc", "elente"]
# Total: 8 tokens

# En LLMs
# "num_predict: 80" = máximo 80 tokens en la respuesta
# Aproximadamente 60-80 palabras o 300-400 caracteres
```

**Uso en Soldasur:** Se limita a 80 tokens (`num_predict: 80`) para respuestas cortas y concisas.

---

## 🎯 Conceptos de Negocio

### Chatbot Orientado a Ventas
**Definición:** Asistente conversacional diseñado específicamente para guiar al cliente hacia la compra, recomendando productos y destacando beneficios.

**Ejemplo:**
```javascript
// Respuesta informativa (NO orientada a ventas)
"Las calderas de gas natural son más eficientes que las de gas envasado."

// Respuesta orientada a ventas (CORRECTA)
"Para tu hogar te recomiendo la Prima Tec Smart 24kW a gas natural. 
 Ahorro del 30% en consumo y calefacción perfecta. ¿Te interesa?"
```

**Uso en Soldasur:** Soldy está configurado para SIEMPRE recomendar productos específicos en cada respuesta.

---

### Sistema de Recomendación
**Definición:** Sistema que sugiere productos o servicios personalizados basándose en las necesidades y preferencias del usuario.

**Ejemplo:**
```python
def recomendar_caldera(superficie, tipo_gas, presupuesto):
    # Filtrar por tipo de gas
    productos = catalogo[catalogo['tipo_gas'] == tipo_gas]
    
    # Filtrar por potencia necesaria (superficie)
    potencia_necesaria = superficie * 0.1  # 100W por m²
    productos = productos[productos['potencia'] >= potencia_necesaria]
    
    # Filtrar por presupuesto
    productos = productos[productos['precio'] <= presupuesto]
    
    # Ordenar por mejor relación calidad-precio
    return productos.sort_values('rating', ascending=False).head(3)
```

**Uso en Soldasur:** Combina sistema experto + RAG para recomendar productos personalizados.

---

## 🔐 Seguridad y Configuración

### Variables de Entorno
**Definición:** Variables externas al código que almacenan configuraciones sensibles como API keys, contraseñas o URLs.

**Ejemplo:**
```bash
# Archivo .env
OLLAMA_URL=http://localhost:11434
MODEL_NAME=llama2
MAX_TOKENS=80
DATABASE_URL=postgresql://user:pass@localhost/db
```

```python
# Leer en Python
import os
from dotenv import load_dotenv

load_dotenv()

ollama_url = os.getenv('OLLAMA_URL')
model_name = os.getenv('MODEL_NAME')
```

**Uso en Soldasur:** Configuración de URLs, modelos y parámetros sin hardcodear en el código.

---

### .gitignore
**Definición:** Archivo que especifica qué archivos o directorios Git debe ignorar y no versionar.

**Ejemplo:**
```gitignore
# Entornos virtuales
venv/
env/

# Archivos de Python
__pycache__/
*.pyc
*.pyo

# Variables de entorno
.env

# Dependencias
node_modules/

# Datos sensibles
data/raw/*.xlsx
*.csv
```

**Uso en Soldasur:** Evita subir archivos grandes, sensibles o generados automáticamente al repositorio.

---

## 📚 Referencias

- **FAISS:** https://github.com/facebookresearch/faiss
- **Ollama:** https://ollama.ai/
- **LangChain:** https://python.langchain.com/
- **Gradio:** https://gradio.app/
- **Sentence Transformers:** https://www.sbert.net/

---

**Última actualización:** Octubre 2025  
**Proyecto:** Soldasur - Sistema de Recomendación de Calderas PEISA
