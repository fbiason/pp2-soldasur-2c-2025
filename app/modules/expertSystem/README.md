# Sistema Experto - PEISA Advisor

## 📋 Descripción

Motor de sistema experto basado en reglas que recomienda productos de calefacción (radiadores, calderas, piso radiante) según las necesidades del usuario.

## 🎯 Características

- ✅ **Base de conocimiento dinámica**: Carga productos desde `data/raw/Products_db.xlsx`
- ✅ **Árbol de decisión**: Flujo guiado definido en `peisa_advisor_knowledge_base.json`
- ✅ **Filtrado inteligente**: Recomienda productos según criterios específicos
- ✅ **Cálculos automáticos**: Potencia, módulos, circuitos, etc.
- ✅ **Fallback automático**: Usa CSV si Excel no está disponible

## 📁 Estructura

```
expertSystem/
├── expert_engine.py       # Motor principal del sistema experto
├── product_loader.py      # Cargador dinámico desde Excel
├── models.py              # Modelos de productos (RADIATOR_MODELS)
└── README.md              # Este archivo
```

## 🚀 Uso Rápido

```python
from app.modules.expertSystem.expert_engine import ExpertEngine

# Inicializar motor
engine = ExpertEngine()

# Procesar interacción
result = await engine.process(
    conversation_id="user123",
    expert_state={'current_node': 'inicio', 'variables': {}},
    option_index=0  # Usuario selecciona primera opción
)

print(result['text'])  # Mostrar pregunta/respuesta
```

## 📊 Base de Conocimiento

### Fuente de Datos
- **Principal**: `data/raw/Products_db.xlsx` (Excel)
- **Fallback**: `data/processed/products_mock.csv` (CSV)

### Árbol de Decisión
- **Archivo**: `app/peisa_advisor_knowledge_base.json`
- **Nodos**: 234 líneas con preguntas, cálculos y respuestas

## 🧪 Testing

```bash
# Ejecutar tests
cd tests
python test_product_loader.py
```

## 📚 Documentación Completa

Ver: [`docs/SISTEMA_EXPERTO_BASE_CONOCIMIENTO.md`](../../../docs/SISTEMA_EXPERTO_BASE_CONOCIMIENTO.md)

## 🔄 Actualizar Productos

1. Editar `data/raw/Products_db.xlsx`
2. Guardar cambios
3. Reiniciar aplicación (carga automática)

O sin reiniciar:
```python
from app.modules.expertSystem.models import reload_models
reload_models()
```

## ✅ Estado

- ✅ Implementado
- ✅ Testeado (4/4 tests pasados)
- ✅ Documentado
- ✅ Producción ready
