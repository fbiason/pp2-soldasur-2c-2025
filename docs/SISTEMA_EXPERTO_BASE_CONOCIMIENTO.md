# Sistema Experto - Base de Conocimiento Dinámica

## 📋 Descripción

El sistema experto de PEISA Advisor ahora carga **dinámicamente** su base de conocimiento de productos desde el archivo Excel **`data/raw/Products_db.xlsx`**, en lugar de tener los datos hardcodeados en el código.

## 🎯 Ventajas

### ✅ Antes (Hardcoded)
- Productos definidos manualmente en código
- Difícil de actualizar
- Requiere modificar código para agregar productos
- Propenso a errores de sincronización

### ✅ Ahora (Dinámico desde Excel)
- **Productos cargados automáticamente desde Excel**
- Fácil de actualizar (solo editar Excel)
- No requiere modificar código
- Única fuente de verdad

## 🏗️ Arquitectura

```
Products_db.xlsx (Excel)
        ↓
ProductLoader (product_loader.py)
        ↓
    ┌───────────────────────┐
    │  Procesamiento        │
    │  - Radiadores         │
    │  - Calderas           │
    │  - Piso Radiante      │
    └───────────────────────┘
        ↓
    ┌───────────────────────┐
    │  RADIATOR_MODELS      │
    │  (models.py)          │
    └───────────────────────┘
        ↓
    ExpertEngine
        ↓
    Recomendaciones
```

## 📁 Archivos Creados/Modificados

### Nuevos Archivos

1. **`app/modules/expertSystem/product_loader.py`**
   - Carga productos desde Excel
   - Procesa y categoriza productos
   - Filtra radiadores por criterios
   - Recomienda calderas por potencia
   - Exporta catálogo a JSON

2. **`app/modules/expertSystem/models.py`**
   - Define `RADIATOR_MODELS` dinámicamente
   - Función `reload_models()` para recargar

3. **`tests/test_product_loader.py`**
   - Tests de carga de productos
   - Tests de filtrado
   - Tests de recomendaciones
   - Tests de exportación

4. **`docs/SISTEMA_EXPERTO_BASE_CONOCIMIENTO.md`** (este archivo)
   - Documentación completa del sistema

### Archivos Modificados

1. **`app/modules/expertSystem/expert_engine.py`**
   - Integración con `ProductLoader`
   - Funciones actualizadas para usar carga dinámica

## 🔧 Uso

### Cargar Productos

```python
from app.modules.expertSystem.product_loader import get_product_loader

# Obtener instancia del cargador
loader = get_product_loader()

# Obtener radiadores
radiators = loader.get_radiators_dict()

# Obtener calderas
boilers = loader.get_boilers_list()

# Obtener todos los productos
all_products = loader.get_all_products()
```

### Filtrar Radiadores

```python
# Filtrar radiadores por criterios
results = loader.filter_radiators_by_criteria(
    radiator_type='principal',
    installation='cualquiera',
    style='moderno',
    color='blanco',
    heat_load=2000  # kcal/h
)
```

### Recomendar Calderas

```python
# Encontrar caldera adecuada
boiler = loader.find_boiler_by_power(
    power_required_kcal=25000,
    boiler_type='mural'  # opcional
)
```

### Exportar Catálogo

```python
# Exportar a JSON para respaldo o análisis
loader.export_to_json("data/processed/products_catalog.json")
```

## 📊 Estructura del Excel

El archivo `Products_db.xlsx` debe tener las siguientes columnas:

| Columna | Descripción | Ejemplo |
|---------|-------------|---------|
| `type` | Tipo de producto | Radiador, Caldera, Piso Radiante |
| `family` | Familia del producto | Broen, Diva Tecno, PEISA |
| `model` | Modelo específico | 350 Inyectado, 24 DS F |
| `description` | Descripción detallada | Diseño minimalista... |
| `dimentions` | Dimensiones | 425mm x 80mm x 80mm |
| `power_w` | Potencia en Watts | 110, 20724.66 |
| `liters` | Capacidad en litros | 0.295, 8 |
| `max_pressure_bar` | Presión máxima | 6, 3 |

## 🧪 Testing

### Ejecutar Tests

```bash
# Desde el directorio raíz del proyecto
cd tests
python test_product_loader.py
```

### Tests Incluidos

1. ✅ **Carga de productos**: Verifica que se cargan correctamente
2. ✅ **Filtrado de radiadores**: Prueba criterios de búsqueda
3. ✅ **Recomendación de calderas**: Valida selección por potencia
4. ✅ **Exportación de catálogo**: Confirma generación de JSON

### Salida Esperada

```
============================================================
SISTEMA EXPERTO - TEST DE BASE DE CONOCIMIENTO DINÁMICA
============================================================

✓ Radiadores cargados: 10
✓ Calderas cargadas: 3
✓ Sistemas de piso radiante: 0
✓ TOTAL DE PRODUCTOS: 13

============================================================
RESUMEN DE TESTS
============================================================
✓ PASS - Carga de productos
✓ PASS - Filtrado de radiadores
✓ PASS - Recomendación de calderas
✓ PASS - Exportación de catálogo

Resultado: 4/4 tests pasados

🎉 ¡Todos los tests pasaron!
```

## 🔄 Actualizar Productos

### Proceso Simple

1. **Editar Excel**: Abre `data/raw/Products_db.xlsx`
2. **Agregar/Modificar**: Edita productos según necesites
3. **Guardar**: Guarda el archivo Excel
4. **Reiniciar**: Reinicia la aplicación (los productos se cargan automáticamente)

### Sin Reiniciar (Opcional)

```python
from app.modules.expertSystem.models import reload_models

# Recargar modelos sin reiniciar
reload_models()
```

## 📝 Procesamiento Automático

El `ProductLoader` realiza automáticamente:

### Para Radiadores
- ✅ Determina tipo de instalación (empotrada/superficie)
- ✅ Identifica estilo (moderno/clásico)
- ✅ Extrae colores disponibles
- ✅ Calcula coeficientes por tamaño
- ✅ Convierte potencia W → kcal/h

### Para Calderas
- ✅ Identifica tipo (mural/piso)
- ✅ Convierte potencia W → kcal/h
- ✅ Extrae capacidad y presión

### Para Piso Radiante
- ✅ Extrae superficie en m²
- ✅ Identifica kits completos

## 🚨 Fallback Automático

Si el Excel no está disponible, el sistema automáticamente:

1. Intenta cargar desde `data/processed/products_mock.csv`
2. Muestra advertencia en consola
3. Continúa funcionando con datos disponibles

## 🔍 Debugging

### Ver Productos Cargados

```python
loader = get_product_loader()

# Ver radiadores
for name, model in loader.radiators.items():
    print(f"{name}: {model['potencia']:.2f} kcal/h")

# Ver calderas
for boiler in loader.boilers.values():
    print(f"{boiler['name']}: {boiler['potencia_kcal']:.2f} kcal/h")
```

### Verificar Carga

```python
# Verificar si hay productos cargados
if loader.products_df is not None:
    print(f"✓ {len(loader.products_df)} productos cargados")
else:
    print("✗ No se cargaron productos")
```

## 🎓 Ejemplo Completo

```python
from app.modules.expertSystem.product_loader import get_product_loader

# 1. Obtener loader
loader = get_product_loader()

# 2. Buscar radiadores para un ambiente de 20m² con techo de 3m
volumen = 20 * 3  # 60 m³
carga_termica = volumen * 40  # 2400 kcal/h (aislación media)

radiators = loader.filter_radiators_by_criteria(
    radiator_type='principal',
    installation='cualquiera',
    style='moderno',
    color='blanco',
    heat_load=carga_termica
)

# 3. Mostrar recomendaciones
print(f"Para {carga_termica} kcal/h recomendamos:")
for i, rad in enumerate(radiators[:3], 1):
    potencia = rad['potencia'] * rad['coeficiente']
    print(f"{i}. {rad['name']} - {potencia:.0f} kcal/h")

# 4. Buscar caldera para toda la casa (80m²)
carga_total = 80 * 100  # 8000 W
carga_kcal = carga_total * 0.859845  # 6878 kcal/h

boiler = loader.find_boiler_by_power(carga_kcal, boiler_type='mural')
print(f"\nCaldera recomendada: {boiler['name']}")
print(f"Potencia: {boiler['potencia_kcal']:.0f} kcal/h")
```

## 📚 Referencias

- **Excel fuente**: `data/raw/Products_db.xlsx`
- **CSV fallback**: `data/processed/products_mock.csv`
- **Código principal**: `app/modules/expertSystem/product_loader.py`
- **Tests**: `tests/test_product_loader.py`

## ✅ Checklist de Implementación

- [x] Crear `product_loader.py`
- [x] Crear `models.py` dinámico
- [x] Actualizar `expert_engine.py`
- [x] Crear tests automatizados
- [x] Documentar sistema
- [x] Implementar fallback a CSV
- [x] Agregar funciones de filtrado
- [x] Agregar exportación a JSON

---

**Última actualización**: Octubre 2025  
**Proyecto**: Soldasur - Sistema Experto PEISA Advisor  
**Estado**: ✅ Implementado y Testeado
