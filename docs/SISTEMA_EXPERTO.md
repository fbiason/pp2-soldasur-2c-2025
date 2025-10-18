# Sistema Experto de Calefacción PEISA - SOLDASUR S.A.

## Índice
1. [Arquitectura General](#arquitectura-general)
2. [Cálculo de Piso Radiante](#cálculo-de-piso-radiante)
3. [Cálculo de Radiadores](#cálculo-de-radiadores)
4. [Cálculo de Calderas](#cálculo-de-calderas)
5. [Ubicación de Archivos](#ubicación-de-archivos)

---

## Arquitectura General

El sistema experto funciona mediante un **motor de reglas basado en grafos de decisión** implementado en Python con FastAPI. El flujo de conversación está definido en un archivo JSON que contiene nodos con diferentes tipos de acciones.

### Componentes Principales:
- **Base de conocimiento**: `peisa_advisor_knowledge_base.json`
- **Motor de cálculo**: `app.py`
- **Modelos de productos**: `models.py`
- **API REST**: `main.py`

---

## Cálculo de Piso Radiante

### Ubicación del Código
- **Archivo de configuración**: `app/peisa_advisor_knowledge_base.json` (nodos: `superficie_piso`, `tipo_piso`, `zona_geografica`, `calculo_piso_radiante`)
- **Motor de cálculo**: `app/app.py` (función `perform_calculation()`)

### Flujo de Cálculo

#### 1. Entrada de Datos
El sistema solicita al usuario:
- **Superficie útil** (m²) a calefaccionar
- **Tipo de pavimento**: Cerámica/Mármol, Madera/Parquet, o Alfombra
- **Zona geográfica**: Centro/Norte o Sur

#### 2. Parámetros de Cálculo
```json
"parametros": {
  "potencia_m2": { 
    "norte": 100,  // W/m²
    "sur": 125     // W/m²
  },
  "densidad_caño": 5,              // metros de caño por m²
  "longitud_maxima_circuito": 100  // metros máximos por circuito
}
```

#### 3. Fórmulas Aplicadas

**Carga térmica total:**
```python
carga_termica = superficie * potencia_m2[zona_geografica]
```
- Zona Norte/Centro: 100 W/m²
- Zona Sur: 125 W/m² (mayor demanda por clima más frío)

**Longitud total de caños:**
```python
longitud_total = superficie * densidad_caño
```
- Se utilizan 5 metros de caño por cada m² de superficie

**Número de circuitos:**
```python
circuitos = ceil(longitud_total / longitud_maxima_circuito)
```
- Cada circuito no debe superar los 100 metros para mantener presión adecuada
- Se redondea hacia arriba para asegurar cobertura completa

#### 4. Resultado
El sistema devuelve:
- Superficie total
- Potencia estimada en Watts
- Longitud total de caños necesarios
- Cantidad de circuitos sugeridos

### Ejemplo de Cálculo
Para un ambiente de **50 m²** en **Zona Sur**:
- Carga térmica: 50 × 125 = **6,250 W**
- Longitud de caños: 50 × 5 = **250 m**
- Circuitos: ceil(250 / 100) = **3 circuitos**

---

## Cálculo de Radiadores

### Ubicación del Código
- **Base de conocimiento**: `app/peisa_advisor_knowledge_base.json` (nodos: `objetivo_radiadores`, `dimensiones_radiador`, `nivel_aislacion`, `recomendar_modelos`)
- **Modelos de productos**: `app/models.py` (diccionario `RADIATOR_MODELS`)
- **Funciones de filtrado**: `app/app.py` (funciones `filter_radiators()`, `format_radiator_recommendations()`)

### Flujo de Cálculo

#### 1. Entrada de Datos
El sistema recopila:
- **Dimensiones del ambiente**: largo, ancho y alto (metros)
- **Nivel de aislación térmica**: Alta, Media o Baja
- **Preferencias de diseño**:
  - Tipo de instalación: Empotrada, Superficie o Sin preferencia
  - Estilo: Moderno/Minimalista, Clásico/Tradicional o Sin preferencia
  - Color: Blanco, Negro, Cromo o Sin preferencia
- **Objetivo**: Calefacción principal, complementaria o toallero

#### 2. Cálculo de Carga Térmica

**Volumen del ambiente:**
```python
volumen = largo * ancho * alto  // m³
```

**Carga térmica según aislación:**
```python
if nivel_aislacion == 'baja':
    factor = 50  # kcal/h por m³
elif nivel_aislacion == 'media':
    factor = 40  # kcal/h por m³
else:  # alta
    factor = 30  # kcal/h por m³

carga_termica = volumen * factor
```

Los factores reflejan:
- **Baja aislación (50 kcal/h·m³)**: Sin doble vidrio, paredes sin aislar
- **Media aislación (40 kcal/h·m³)**: Vidrio simple, aislación parcial
- **Alta aislación (30 kcal/h·m³)**: Doble vidrio, paredes aisladas

#### 3. Filtrado de Modelos

El sistema filtra los radiadores según:

```python
def filter_radiators(radiator_type, installation, style, color, heat_load):
    # 1. Filtrar por tipo (principal, complementaria, toallero)
    # 2. Filtrar por instalación (empotrada, superficie)
    # 3. Filtrar por estilo (moderno, clasico)
    # 4. Filtrar por color (blanco, negro, cromo)
    # 5. Ordenar por mejor ajuste a la carga térmica
```

#### 4. Modelos Disponibles

Cada modelo tiene:
- **Coeficiente**: Factor multiplicador de potencia base
- **Potencia base**: 185 kcal/h por módulo (632 kcal/h para toalleros)

**Ejemplos de modelos:**

| Modelo | Coeficiente | Potencia Efectiva | Tipo | Instalación |
|--------|-------------|-------------------|------|-------------|
| TROPICAL 350 | 0.75 | 139 kcal/h | Principal | Superficie |
| TROPICAL 500 | 1.0 | 185 kcal/h | Principal | Superficie |
| TROPICAL 600 | 1.16 | 215 kcal/h | Principal | Superficie |
| BROEN 350 | 0.75 | 139 kcal/h | Principal/Complementaria | Superficie |
| BROEN 500 | 1.0 | 185 kcal/h | Principal/Complementaria | Superficie |
| BROEN 600 | 1.16 | 215 kcal/h | Principal/Complementaria | Superficie |
| BROEN PLUS 700 | 1.27 | 235 kcal/h | Principal/Complementaria | Empotrada/Superficie |
| BROEN PLUS 800 | 1.4 | 259 kcal/h | Principal/Complementaria | Empotrada/Superficie |
| BROEN PLUS 1000 | 1.65 | 305 kcal/h | Principal/Complementaria | Empotrada/Superficie |
| GAMMA 500 | 0.93 | 172 kcal/h | Complementaria | Superficie |
| TOALLERO SCALA | N/A | 632 kcal/h | Toallero | Superficie |

#### 5. Cálculo de Módulos

**Potencia efectiva por módulo:**
```python
potencia_efectiva = potencia_base * coeficiente
```

**Módulos necesarios:**
```python
modulos = ceil(carga_termica / potencia_efectiva)
```

Se redondea hacia arriba para garantizar calefacción suficiente.

#### 6. Recomendación

El sistema presenta los **3 mejores modelos** ordenados por:
1. Cumplimiento de preferencias (tipo, instalación, estilo, color)
2. Mejor ajuste a la carga térmica calculada

Para cada modelo muestra:
- Nombre del modelo
- Potencia efectiva por módulo
- Módulos estimados necesarios
- Descripción del producto
- Colores disponibles

### Ejemplo de Cálculo

Para un ambiente de **4m × 3m × 2.5m** con **aislación media**:

1. **Volumen**: 4 × 3 × 2.5 = **30 m³**
2. **Carga térmica**: 30 × 40 = **1,200 kcal/h**
3. Si se elige **BROEN 500** (185 kcal/h):
   - Módulos: ceil(1,200 / 185) = **7 módulos**

---

## Cálculo de Calderas

### Nota Importante
El sistema actual **no incluye cálculo automático de calderas**. Sin embargo, la lógica sería:

### Criterios de Selección (Propuesta)

**Potencia total requerida:**
```python
potencia_total_caldera = suma_cargas_termicas_todos_ambientes * factor_seguridad
```

Donde:
- `factor_seguridad` = 1.2 (20% adicional para pérdidas y arranque)

**Tipo de caldera según uso:**
- **Solo calefacción**: Caldera estándar
- **Calefacción + ACS (Agua Caliente Sanitaria)**: Caldera mixta o con acumulador

**Ubicación sugerida:**
El cálculo de calderas podría agregarse en:
- **Archivo**: `app/peisa_advisor_knowledge_base.json`
- **Nuevo nodo**: `"id": "calculo_caldera"`
- **Función**: Nueva función en `app/app.py` llamada `calculate_boiler()`

### Implementación Sugerida

```python
def calculate_boiler(total_heat_load, has_hot_water=False):
    """
    Calcula la potencia de caldera necesaria
    
    Args:
        total_heat_load: Carga térmica total en kcal/h
        has_hot_water: Si requiere agua caliente sanitaria
    
    Returns:
        Potencia de caldera recomendada en kcal/h
    """
    safety_factor = 1.2
    hot_water_extra = 5000 if has_hot_water else 0  # kcal/h adicionales para ACS
    
    required_power = (total_heat_load * safety_factor) + hot_water_extra
    
    # Redondear a potencias estándar: 18000, 24000, 30000, 35000 kcal/h
    standard_powers = [18000, 24000, 30000, 35000, 45000]
    
    for power in standard_powers:
        if power >= required_power:
            return power
    
    return standard_powers[-1]  # Máxima potencia si excede
```

---

## Ubicación de Archivos

### Estructura del Proyecto

```
proyecto_pp2/
│
├── app/
│   ├── __init__.py                          # Inicialización del módulo
│   ├── app.py                               # Motor de cálculo y lógica de negocio
│   ├── main.py                              # API REST con FastAPI
│   ├── models.py                            # Base de datos de radiadores
│   ├── llm_wrapper.py                       # Wrapper para LLM (consultas adicionales)
│   ├── chat.html                            # Interfaz web del chatbot
│   └── peisa_advisor_knowledge_base.json    # Base de conocimiento (grafo de decisión)
│
├── query/
│   └── query.py                             # Motor de búsqueda semántica
│
├── ingest/
│   └── ingest.py                            # Ingesta de documentos para RAG
│
├── requirements.txt                          # Dependencias Python
└── EXPLICACION.md                           # Este archivo
```

### Descripción de Archivos Clave

#### `app/peisa_advisor_knowledge_base.json`
- **Propósito**: Define el flujo conversacional completo
- **Contenido**: Nodos con preguntas, opciones, cálculos y respuestas
- **Tipos de nodos**:
  - `pregunta`: Solicita información al usuario
  - `entrada_usuario`: Captura valores numéricos
  - `calculo`: Ejecuta fórmulas matemáticas
  - `respuesta`: Muestra resultados

#### `app/models.py`
- **Propósito**: Base de datos de productos (radiadores)
- **Contenido**: Diccionario `RADIATOR_MODELS` con especificaciones técnicas
- **Campos por modelo**:
  - `type`: Tipo de uso (principal, complementaria, toallero)
  - `installation`: Tipo de instalación (superficie, empotrada)
  - `style`: Estilo de diseño (moderno, clasico)
  - `colors`: Colores disponibles
  - `coeficiente`: Factor multiplicador de potencia
  - `potencia`: Potencia base en kcal/h
  - `description`: Descripción del producto

#### `app/app.py`
- **Propósito**: Motor de cálculo y funciones auxiliares
- **Funciones principales**:
  - `perform_calculation()`: Ejecuta cálculos definidos en nodos
  - `exec_expression()`: Evalúa expresiones matemáticas
  - `filter_radiators()`: Filtra modelos según preferencias
  - `format_radiator_recommendations()`: Formatea recomendaciones
  - `replace_variables()`: Reemplaza variables en textos con Jinja2

#### `app/main.py`
- **Propósito**: API REST y endpoints
- **Endpoints**:
  - `POST /start`: Inicia una conversación
  - `POST /reply`: Procesa respuestas del usuario
  - `GET /health`: Verifica estado del servicio
  - `GET /ask`: Consulta con LLM (búsqueda semántica)
  - `GET /`: Sirve la interfaz web

#### `app/chat.html`
- **Propósito**: Interfaz de usuario web
- **Funcionalidad**: Chatbot interactivo que consume la API REST

---

## Flujo de Ejecución

### 1. Inicio de Conversación
```
Usuario → POST /start → Carga nodo "inicio" → Muestra opciones
```

### 2. Navegación por Nodos
```
Usuario selecciona opción → POST /reply → 
  ├─ Si es entrada_usuario: Guarda valores en contexto
  ├─ Si es pregunta: Muestra siguiente pregunta
  ├─ Si es calculo: Ejecuta fórmulas y avanza
  └─ Si es respuesta: Muestra resultado
```

### 3. Contexto de Conversación
Cada conversación mantiene:
```python
conversations[conversation_id] = {
    'current_node': 'id_del_nodo_actual',
    'context': {
        'superficie': 50,
        'zona_geografica': 'sur',
        'largo': 4,
        'ancho': 3,
        'alto': 2.5,
        'carga_termica': 1200,
        # ... más variables calculadas
    }
}
```

### 4. Ejecución de Cálculos
```python
# En nodo de tipo "calculo"
for action in node["acciones"]:
    exec_expression(action, context)
    
# Ejemplo de acción:
"carga_termica = volumen * (50 if nivel_aislacion == 'baja' else 40 if nivel_aislacion == 'media' else 30)"
```

---

## Ventajas del Sistema

1. **Modular**: Fácil agregar nuevos productos o modificar cálculos
2. **Declarativo**: La lógica está en JSON, no hardcodeada
3. **Extensible**: Se pueden agregar nuevos tipos de nodos
4. **Mantenible**: Separación clara entre datos, lógica y presentación
5. **Interactivo**: Guía al usuario paso a paso

---

## Mejoras Futuras

1. **Cálculo de calderas**: Implementar selección automática de calderas
2. **Validaciones**: Agregar rangos válidos para entradas numéricas
3. **Persistencia**: Guardar conversaciones en base de datos
4. **Exportación**: Generar PDF con presupuesto y especificaciones
5. **Integración**: Conectar con sistema de inventario y precios
6. **Visualización**: Mostrar planos o esquemas de instalación

---

## Contacto y Soporte

**SOLDASUR S.A.**  
Sistema desarrollado para asesoramiento en calefacción PEISA  
Versión: 1.0