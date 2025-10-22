# 🎯 Cómo Evaluar el Desempeño del Chatbot Soldy

## 📋 Métodos de Evaluación

### Método 1: Script Automatizado - Demo (Recomendado para empezar)

**Sin necesidad de Ollama corriendo:**

```bash
cd tests
python test_chatbot_evaluation_demo.py
```

✅ Usa respuestas simuladas ideales  
✅ Ejecución instantánea  
✅ Perfecto para entender el sistema  

### Método 2: Script Automatizado - Real

**Requisitos previos:**
1. Ollama instalado y corriendo
2. Módulo ollama instalado: `pip install ollama`
3. Modelo descargado: `ollama pull llama3.2:3b`

```bash
cd tests
python test_chatbot_evaluation.py
```

✅ Evalúa respuestas reales del chatbot  
✅ Detecta problemas reales  
✅ Resultados más precisos  

**El script evalúa:**
- ✅ Consultas sobre productos específicos
- ✅ Consultas de precios
- ✅ Consultas técnicas simples y complejas
- ✅ Consultas fuera de tema
- ✅ Comparaciones de productos
- ✅ Consultas sobre dónde comprar
- ✅ Consultas sobre instalación

**Resultado:**
- Puntaje 1-5 por cada métrica
- Justificación de cada puntaje
- Aspectos positivos y a mejorar
- Respuesta ideal sugerida
- Promedio general del chatbot

---

### Método 2: Evaluación Manual

Usá la plantilla en `docs/evaluacion_chatbot.md` para evaluar conversaciones reales:

1. **Copiá la conversación**
2. **Completá la tabla de métricas**
3. **Anotá aspectos positivos y a mejorar**
4. **Sugerí una respuesta mejorada si es necesario**

---

## 📊 Métricas Explicadas

### 1. Detección de Intención (1-5)
**¿El chatbot entiende lo que el usuario necesita?**

| Puntaje | Descripción | Ejemplo |
|---------|-------------|---------|
| 5 | Identifica perfectamente | Usuario pregunta por precio → Chatbot pregunta ciudad |
| 4 | Identifica bien con pequeñas imprecisiones | Identifica pero da info extra innecesaria |
| 3 | Identifica parcialmente | Entiende que pregunta por producto pero no específica bien |
| 2 | Identifica mal o confuso | Responde algo relacionado pero no lo que se pidió |
| 1 | No identifica | Respuesta totalmente fuera de contexto |

**Ejemplo Bueno (5/5):**
- Usuario: "¿Cuánto sale?"
- Soldy: "Para precios, ¿estás en Río Grande o Ushuaia?"
- ✅ Detecta que pregunta precio y actúa correctamente

**Ejemplo Malo (2/5):**
- Usuario: "¿Cuánto sale?"
- Soldy: "Tenemos varios modelos de calderas disponibles."
- ❌ No detecta que pregunta por precio

---

### 2. Relevancia (1-5)
**¿La respuesta es útil y pertinente?**

| Puntaje | Descripción | Ejemplo |
|---------|-------------|---------|
| 5 | Totalmente relevante y útil | Responde exactamente lo que se preguntó + recomienda producto |
| 4 | Muy relevante con detalles menores | Responde bien pero agrega info no pedida |
| 3 | Parcialmente relevante | Responde algo relacionado pero no específico |
| 2 | Poco relevante | Respuesta genérica o vaga |
| 1 | Irrelevante | No tiene nada que ver con la pregunta |

**Ejemplo Bueno (5/5):**
- Usuario: "¿Qué caldera para 80m²?"
- Soldy: "Para 80m² te recomiendo la Prima Tec Smart, es eficiente y perfecta para ese tamaño."
- ✅ Responde específicamente y recomienda producto

**Ejemplo Malo (2/5):**
- Usuario: "¿Qué caldera para 80m²?"
- Soldy: "Tenemos muchas calderas buenas en nuestro catálogo."
- ❌ Respuesta genérica sin especificar

---

### 3. Claridad (1-5)
**¿La respuesta es clara, concisa y fácil de entender?**

| Puntaje | Descripción | Longitud Ideal |
|---------|-------------|----------------|
| 5 | Perfectamente clara y concisa | 20-30 palabras, 2-3 frases |
| 4 | Clara con alguna redundancia | 15-40 palabras |
| 3 | Comprensible pero confusa en partes | 10-60 palabras |
| 2 | Confusa o ambigua | Muy corta (<10) o muy larga (>60) |
| 1 | Incomprensible | Incoherente o cortada |

**Ejemplo Bueno (5/5):**
- "Los radiadores Broen son excelentes, eficientes y duraderos. Ideales para tu hogar."
- ✅ 13 palabras, 2 frases, mensaje completo

**Ejemplo Malo (2/5):**
- "Los radiadores Broen son productos de alta calidad fabricados con materiales resistentes que garantizan una larga vida útil y un rendimiento óptimo en condiciones de uso continuo..."
- ❌ 28 palabras en 1 frase, muy técnico y largo

---

### 4. Tono (1-5)
**¿El tono es cálido, empático y profesional?**

| Puntaje | Descripción | Características |
|---------|-------------|-----------------|
| 5 | Tono perfecto | Usa vos/podés, cálido, empático |
| 4 | Buen tono con pequeñas fallas | Usa vos/podés pero falta calidez |
| 3 | Tono aceptable pero frío | Correcto pero muy formal |
| 2 | Tono inadecuado | Muy técnico o impersonal |
| 1 | Tono inapropiado | Grosero o completamente formal |

**Ejemplo Bueno (5/5):**
- "¡Perfecto! Te recomiendo la Prima Tec Smart, es ideal para tu espacio. ¿Querés saber más?"
- ✅ Usa vos/podés, entusiasta, empático

**Ejemplo Malo (2/5):**
- "Le recomiendo la Prima Tec Smart. Es un producto de alta calidad."
- ❌ Usa "le" (formal), frío, sin empatía

---

## 🎯 Interpretación de Resultados

### Promedio General

| Rango | Clasificación | Acción |
|-------|---------------|--------|
| 4.5-5.0 | 🏆 EXCELENTE | Mantener y documentar buenas prácticas |
| 3.5-4.4 | ✅ BUENO | Pequeños ajustes en áreas específicas |
| 2.5-3.4 | ⚠️ ACEPTABLE | Requiere mejoras significativas |
| <2.5 | ❌ DEFICIENTE | Revisión completa del sistema |

---

## 🔧 Acciones Correctivas

### Si Detección de Intención < 4.0
```python
# En chatbot.js o llm_wrapper.py
# Agregar más keywords de detección
keywords_precio = ["precio", "cuánto", "sale", "cuesta", "vale", "comprar", "presupuesto"]
```

### Si Relevancia < 4.0
```python
# En system prompt
"✅ SIEMPRE recomienda 1 producto específico por nombre
✅ Responde la pregunta ANTES de recomendar
✅ Usa el catálogo proporcionado"
```

### Si Claridad < 4.0
```python
# Ajustar límites
max_tokens = 80  # Si muy largo
max_words = 30   # Si muy largo

# O aumentar si se corta
max_tokens = 100
```

### Si Tono < 4.0
```python
# En system prompt
"✅ Español argentino: Usá vos/podés, tono cercano
✅ Tono CÁLIDO y HUMANO: Como un asesor real
✅ Evitar formalidades: No uses 'usted', 'le recomiendo'"
```

---

## 📝 Ejemplo de Evaluación Completa

### Conversación:
**Usuario:** "¿Cuánto sale la Prima Tec Smart?"  
**Soldy:** "Para precios y compras, ¿estás en Río Grande o Ushuaia? Te paso el contacto de la sucursal."

### Evaluación:

| Métrica | Puntaje | Justificación |
|---------|---------|---------------|
| **Detección de Intención** | 5/5 | Identifica perfectamente que pregunta por precio |
| **Relevancia** | 5/5 | Respuesta totalmente relevante, no menciona precio y ofrece contacto |
| **Claridad** | 5/5 | 16 palabras, 2 frases, mensaje completo y claro |
| **Tono** | 4/5 | Usa vos/podés pero podría ser más cálido |
| **PROMEDIO** | 4.75/5 | 🏆 EXCELENTE |

### ✅ Aspectos Positivos:
- Maneja correctamente consulta de precio
- No menciona montos
- Pregunta por ciudad para dar contacto
- Usa español argentino (vos/podés)
- Respuesta breve y clara

### ⚠️ Aspectos a Mejorar:
- Podría agregar más calidez: "¡Perfecto!" o "¡Dale!"

### 💡 Respuesta Mejorada:
"¡Dale! Para precios y compras, ¿estás en Río Grande o Ushuaia? Te paso el contacto de la sucursal más cercana."

---

## 📊 Registro de Evaluaciones

Mantené un registro de evaluaciones en `docs/evaluacion_chatbot.md`:

```markdown
### Evaluación del 22/10/2025

| Caso | Intención | Relevancia | Claridad | Tono | Promedio |
|------|-----------|------------|----------|------|----------|
| 1    | 5/5       | 5/5        | 4/5      | 5/5  | 4.75/5   |
| 2    | 4/5       | 5/5        | 5/5      | 4/5  | 4.5/5    |
| ...  | ...       | ...        | ...      | ...  | ...      |

**Promedio General:** 4.6/5 ✅ BUENO

**Observaciones:**
- Excelente manejo de precios
- Tono podría ser más cálido en algunos casos
- Claridad consistente en todas las respuestas
```

---

## 🚀 Próximos Pasos

1. **Ejecutar evaluación inicial** con el script
2. **Identificar áreas débiles** (métricas < 4.0)
3. **Implementar mejoras** según las recomendaciones
4. **Re-evaluar** después de cada cambio
5. **Documentar resultados** para seguimiento

---

## 💡 Tips para Mejores Resultados

✅ **Evaluá con casos reales** de usuarios cuando sea posible  
✅ **Evaluá regularmente** (semanal o después de cambios)  
✅ **Documentá patrones** de fallas recurrentes  
✅ **Compará resultados** antes y después de mejoras  
✅ **Involucrar al equipo** en la evaluación  

---

## 🔧 Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'ollama'"

**Solución:**
```bash
pip install ollama
```

### Error: "Connection refused" o "Ollama not running"

**Solución:**
1. Verificar que Ollama esté corriendo:
   ```bash
   ollama list
   ```

2. Si no está corriendo, iniciarlo:
   ```bash
   ollama serve
   ```

3. Verificar que el modelo esté descargado:
   ```bash
   ollama pull llama3.2:3b
   ```

### El test es muy lento

**Solución:**
- Usar la versión demo: `python test_chatbot_evaluation_demo.py`
- La versión demo es instantánea y usa respuestas simuladas

### Quiero evaluar con respuestas reales pero no tengo Ollama

**Solución:**
1. Instalar Ollama desde: https://ollama.ai
2. Instalar el módulo Python: `pip install ollama`
3. Descargar el modelo: `ollama pull llama3.2:3b`
4. Ejecutar el test real: `python test_chatbot_evaluation.py`

---

## 📞 Soporte

Si encontrás problemas o necesitás ayuda con la evaluación, documentá los casos problemáticos en `docs/evaluacion_chatbot.md` para análisis posterior.
