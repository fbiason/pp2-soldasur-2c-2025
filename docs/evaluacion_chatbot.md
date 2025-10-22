# 📊 Evaluación de Desempeño del Chatbot Soldy

## Métricas de Evaluación (Escala 1-5)

### 1. **Detección de Intención** 
¿El chatbot identifica correctamente lo que el usuario necesita?
- 5: Identifica perfectamente la intención
- 4: Identifica bien con pequeñas imprecisiones
- 3: Identifica parcialmente
- 2: Identifica mal o de forma confusa
- 1: No identifica la intención

### 2. **Relevancia**
¿La respuesta es pertinente y útil para la consulta?
- 5: Totalmente relevante y útil
- 4: Muy relevante con detalles menores irrelevantes
- 3: Parcialmente relevante
- 2: Poco relevante
- 1: Irrelevante

### 3. **Claridad**
¿La respuesta es clara, concisa y fácil de entender?
- 5: Perfectamente clara y concisa
- 4: Clara con alguna redundancia menor
- 3: Comprensible pero confusa en partes
- 2: Confusa o ambigua
- 1: Incomprensible

### 4. **Tono**
¿El tono es cálido, empático y profesional?
- 5: Tono perfecto, cálido y profesional
- 4: Buen tono con pequeñas fallas
- 3: Tono aceptable pero frío o muy formal
- 2: Tono inadecuado (muy técnico o impersonal)
- 1: Tono inapropiado

---

## 📝 Plantilla de Evaluación

### Ejemplo de Conversación:
**Usuario:** [Pregunta del usuario]  
**Soldy:** [Respuesta del chatbot]

### Evaluación:

| Métrica | Puntaje | Justificación |
|---------|---------|---------------|
| **Detección de Intención** | X/5 | [Explicación] |
| **Relevancia** | X/5 | [Explicación] |
| **Claridad** | X/5 | [Explicación] |
| **Tono** | X/5 | [Explicación] |
| **PROMEDIO** | X/5 | |

### ✅ Aspectos Positivos:
- [Punto 1]
- [Punto 2]

### ⚠️ Aspectos a Mejorar:
- [Punto 1]
- [Punto 2]

### 💡 Respuesta Mejorada Sugerida:
```
[Versión mejorada de la respuesta]
```

---

## 🎯 Casos de Uso Comunes

### Caso 1: Consulta sobre Producto Específico
**Usuario:** "¿Qué caldera me recomendás para 80m²?"

**Respuesta Esperada:**
- ✅ Recomienda producto específico (ej: Prima Tec Smart)
- ✅ Menciona beneficio clave
- ✅ Tono cercano (vos/podés)
- ✅ 2-3 frases máximo

**Ejemplo Ideal:**
"Para 80m² te recomiendo la Prima Tec Smart, es eficiente y perfecta para ese tamaño. ¿Querés saber más sobre instalación o precios?"

---

### Caso 2: Consulta sobre Precios
**Usuario:** "¿Cuánto sale la Prima Tec Smart?"

**Respuesta Esperada:**
- ✅ NO menciona precios
- ✅ Pregunta por ciudad (Río Grande o Ushuaia)
- ✅ Tono empático

**Ejemplo Ideal:**
"Para precios y compras, ¿estás en Río Grande o Ushuaia? Te paso el contacto de la sucursal más cercana."

---

### Caso 3: Consulta Técnica
**Usuario:** "¿Cómo funciona el sistema de condensación?"

**Respuesta Esperada:**
- ✅ Explicación simple (sin tecnicismos)
- ✅ Recomienda producto con esa tecnología
- ✅ Ofrece asistencia técnica si es muy complejo

**Ejemplo Ideal:**
"El sistema de condensación aprovecha mejor el calor, ahorrando gas. La Summa Condens usa esta tecnología. Si necesitás más detalles técnicos, te paso contacto con nuestros especialistas."

---

### Caso 4: Consulta Fuera de Tema
**Usuario:** "¿Cuál es el mejor restaurante de Ushuaia?"

**Respuesta Esperada:**
- ✅ Responde amablemente
- ✅ Redirige a productos de calefacción
- ✅ Tono empático

**Ejemplo Ideal:**
"Jaja, no soy experto en restaurantes, pero sí en calefacción. ¿Necesitás algo para tu hogar o negocio?"

---

## 📈 Criterios de Éxito

### Respuesta EXCELENTE (4.5-5.0):
- Identifica perfectamente la intención
- Respuesta relevante y útil
- Clara y concisa (20-30 palabras)
- Tono cálido y profesional
- Recomienda producto específico cuando corresponde
- Maneja precios correctamente

### Respuesta BUENA (3.5-4.4):
- Identifica bien la intención
- Respuesta relevante con detalles menores
- Clara pero puede ser más concisa
- Buen tono con pequeñas fallas
- Recomienda productos pero puede ser más específico

### Respuesta ACEPTABLE (2.5-3.4):
- Identifica parcialmente la intención
- Respuesta parcialmente relevante
- Comprensible pero confusa en partes
- Tono aceptable pero frío
- Falta especificidad en recomendaciones

### Respuesta DEFICIENTE (<2.5):
- No identifica la intención
- Respuesta irrelevante
- Confusa o ambigua
- Tono inadecuado
- No recomienda productos o lo hace mal

---

## 🔧 Acciones Correctivas por Métrica

### Si falla **Detección de Intención**:
1. Revisar keywords en detección de precios
2. Mejorar contexto conversacional
3. Ajustar system prompt con más ejemplos

### Si falla **Relevancia**:
1. Verificar que recomiende productos del catálogo
2. Asegurar que responda la pregunta antes de recomendar
3. Evitar información genérica

### Si falla **Claridad**:
1. Reducir max_tokens si es muy largo
2. Aumentar max_tokens si se corta
3. Ajustar truncamiento en _truncate_to_brief()

### Si falla **Tono**:
1. Revisar system prompt (énfasis en vos/podés)
2. Agregar más ejemplos de tono cálido
3. Ajustar temperature si es muy robótico

---

## 📊 Registro de Evaluaciones

### Fecha: [DD/MM/YYYY]
**Evaluador:** [Nombre]

| # | Intención | Relevancia | Claridad | Tono | Promedio | Estado |
|---|-----------|------------|----------|------|----------|--------|
| 1 | X/5 | X/5 | X/5 | X/5 | X/5 | ✅/⚠️/❌ |
| 2 | X/5 | X/5 | X/5 | X/5 | X/5 | ✅/⚠️/❌ |
| 3 | X/5 | X/5 | X/5 | X/5 | X/5 | ✅/⚠️/❌ |

**Promedio General:** X/5

**Observaciones:**
[Comentarios generales sobre el desempeño]

---

## 🎯 Próximos Pasos

1. **Recolectar conversaciones reales** con usuarios
2. **Evaluar al menos 10 interacciones** usando esta plantilla
3. **Identificar patrones** de fallas recurrentes
4. **Implementar mejoras** según las métricas más bajas
5. **Re-evaluar** después de cada cambio

---

## 📞 Contacto para Feedback

Si encontrás problemas recurrentes o tenés sugerencias, documentalos aquí para análisis posterior.
