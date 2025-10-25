# 🌐 Scraper de Productos PEISA

Este módulo realiza **scraping real** del sitio web de PEISA para obtener el catálogo de productos actualizado.

## 📍 Ubicación del Archivo Generado

El scraping guarda los productos en:
```
data/products_catalog.json
```

**NO** en `data/processed/` ni en `data/raw/`, sino directamente en la raíz de `data/`.

## 🚀 Uso

### Opción 1: Scraping Real (Recomendado)

Extrae productos directamente de https://peisa.com.ar/productos:

```bash
python app/modules/scraping/product_scraper.py
```

### Opción 2: Catálogo de Respaldo

Si no tienes conexión o el sitio no está disponible:

```bash
python app/modules/scraping/product_scraper.py --no-scraping
```

## 📊 Resultado del Scraping

El scraper extrae aproximadamente **50-70 productos** con la siguiente información:

```json
{
  "model": "Prima Tec Smart",
  "description": "Caldera doble servicio",
  "family": "Calderas",
  "type": "Producto de calefacción",
  "power_w": 0,
  "features": [],
  "applications": [],
  "liters": 0,
  "max_pressure_bar": 10,
  "dimensions": "N/A",
  "url": "https://peisa.com.ar/productos/prima-tec-smart"
}
```

### Familias de Productos Extraídas

- **Calderas**: Prima Tec Smart, Diva Tecno, Summa Condens, etc.
- **Radiadores**: Broen, Broen Plus, Tropical, Gamma, etc.
- **Termotanques**: Eléctricos, solares, etc.
- **Climatización Piscinas**: Bombas de calor, TX70, TX40, etc.
- **Otros**: Termostatos, sistemas, accesorios, etc.

## 🔄 Flujo de Datos

```
PEISA Website (https://peisa.com.ar/productos)
    ↓
product_scraper.py (scraping)
    ↓
data/products_catalog.json
    ↓
rag_engine_v2.py (RAG/Chatbot)
```

## 🛠️ Dependencias

El scraper requiere:

```
beautifulsoup4==4.13.3
requests==2.32.3
lxml==6.0.2
```

Ya están incluidas en `requirements.txt`.

## 📝 Estructura HTML de PEISA

El scraper está optimizado para la estructura actual de PEISA:

```html
<a href="/productos/[nombre]">
  <article>
    <div class="text-peisared-600">CATEGORÍA</div>
    <h4>NOMBRE PRODUCTO</h4>
    <p>Descripción del producto</p>
  </article>
</a>
```

## ⚙️ Configuración

### Límite de Productos

Por defecto extrae hasta 50 productos. Para cambiar:

```python
# En product_scraper.py, línea ~46
for idx, card in enumerate(product_cards[:50], 1):  # Cambiar 50
```

### Timeout de Conexión

```python
# En product_scraper.py, línea ~31
response = requests.get(products_url, headers=headers, timeout=10)  # Cambiar 10
```

## 🔍 Verificación

Para verificar que el scraping funcionó correctamente:

```bash
# Ver contenido del archivo
cat data/products_catalog.json

# Contar productos
python -c "import json; print(len(json.load(open('data/products_catalog.json'))))"
```

## 🐛 Solución de Problemas

### Error: "No se encontraron productos"

- Verificar conexión a internet
- El sitio de PEISA puede haber cambiado su estructura HTML
- Usar modo `--no-scraping` como respaldo

### Error: "Connection timeout"

- Aumentar el timeout en la línea 31
- Verificar firewall/proxy
- Usar modo `--no-scraping`

### Error: "ModuleNotFoundError: beautifulsoup4"

```bash
pip install beautifulsoup4 requests lxml
```

## 📌 Notas Importantes

1. **Respeto al servidor**: El scraper incluye pausas de 0.1s entre productos para no sobrecargar el servidor de PEISA.

2. **Catálogo de respaldo**: Si el scraping falla, automáticamente usa un catálogo curado de 14 productos.

3. **Actualización**: Ejecuta el scraper periódicamente para mantener el catálogo actualizado.

4. **Ubicación correcta**: El archivo DEBE estar en `data/products_catalog.json` (no en subdirectorios) para que el RAG Engine lo encuentre.

## 🔗 Integración con el Sistema

El catálogo generado es usado por:

- **RAG Engine V2** (`app/modules/chatbot/rag_engine_v2.py`)
- **Chatbot Soldy** (para recomendaciones de productos)
- **Sistema de búsqueda vectorial** (FAISS)

## 📚 Más Información

- Documentación del chatbot: `docs/CHATBOT_SOLDY.md`
- Estructura del proyecto: `docs/README_MODULOS.md`
- Guía rápida: `docs/QUICKSTART.md`
