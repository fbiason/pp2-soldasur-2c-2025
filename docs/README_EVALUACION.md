# 📊 Sistema de Evaluación del Chatbot Soldy

## 🚀 Inicio Rápido

### Opción 1: Demo con Respuestas Simuladas (Recomendado para empezar)

```bash
cd tests
python test_chatbot_evaluation_demo.py
```

✅ **Ventajas:**
- No requiere Ollama corriendo
- Ejecución instantánea
- Muestra cómo funciona el sistema de evaluación
- Usa respuestas ideales para demostración

### Opción 2: Evaluación Real con Ollama

**Requisitos previos:**
1. Ollama instalado y corriendo
2. Modelo llama3.2:3b descargado

```bash
# Instalar dependencias si es necesario
pip install ollama

# Verificar que Ollama está corriendo
ollama list

# Ejecutar evaluación real
cd tests
python test_chatbot_evaluation.py
```

✅ **Ventajas:**
- Evalúa respuestas reales del chatbot
- Detecta problemas reales
- Resultados más precisos

---

## 📊 Qué Evalúa el Sistema

### 4 Métricas Clave (Escala 1-5)

#### 1. **Detección de Intención** ⭐⭐⭐⭐⭐
¿El chatbot entiende lo que el usuario necesita?

**Ejemplo Excelente (5/5):**
- Usuario: "¿Cuánto sale?"
- Soldy: "Para precios, ¿estás en Río Grande o Ushuaia?"

#### 2. **Relevancia** ⭐⭐⭐⭐⭐
¿La respuesta es útil y pertinente?

**Ejemplo Excelente (5/5):**
- Usuario: "¿Qué caldera para 80m²?"
- Soldy: "Para 80m² te recomiendo la Prima Tec Smart, es eficiente."

#### 3. **Claridad** ⭐⭐⭐⭐⭐
¿Es clara y concisa? (Ideal: 20-30 palabras, 2-3 frases)

**Ejemplo Excelente (5/5):**
- "Los Broen son excelentes y duraderos. Ideales para tu hogar."

#### 4. **Tono** ⭐⭐⭐⭐⭐
¿Es cálido y empático? (Usa vos/podés)

**Ejemplo Excelente (5/5):**
- "¡Perfecto! Te recomiendo la Prima Tec Smart. ¿Querés saber más?"

---

## 📈 Interpretación de Resultados

### Clasificación por Promedio

| Puntaje | Clasificación | Significado |
|---------|---------------|-------------|
| **4.5-5.0** | 🏆 **EXCELENTE** | Chatbot funcionando óptimamente |
| **3.5-4.4** | ✅ **BUENO** | Buen desempeño, pequeños ajustes |
| **2.5-3.4** | ⚠️ **ACEPTABLE** | Requiere mejoras significativas |
| **<2.5** | ❌ **DEFICIENTE** | Necesita revisión completa |

---

## 🎯 8 Casos de Prueba

El sistema evalúa automáticamente estos escenarios:

1. **Consulta Producto Específico**
   - "¿Qué caldera me recomendás para 80m²?"

2. **Consulta Precios**
   - "¿Cuánto sale la Prima Tec Smart?"

3. **Consulta Técnica Simple**
   - "¿Los radiadores Broen son buenos?"

4. **Consulta Técnica Compleja**
   - "¿Cómo funciona el sistema de condensación?"

5. **Consulta Fuera de Tema**
   - "¿Cuál es el mejor restaurante de Ushuaia?"

6. **Consulta Comparación**
   - "¿Qué diferencia hay entre Prima Tec y Diva Tecno?"

7. **Consulta Dónde Comprar**
   - "¿Dónde puedo comprar radiadores?"

8. **Consulta Instalación**
   - "¿Es difícil instalar una caldera?"

---

## 📝 Ejemplo de Salida

```
================================================================================
🔍 CASO 1: Consulta Producto Específico
================================================================================

👤 Usuario: ¿Qué caldera me recomendás para 80m²?
🤖 Soldy: Para 80m² te recomiendo la Prima Tec Smart, es eficiente y perfecta.

📈 MÉTRICAS:
  • Detección de Intención: 5/5
    └─ Identifica correctamente la intención
  • Relevancia: 5/5
    └─ Respuesta totalmente relevante y útil
  • Claridad: 4/5
    └─ Respuesta clara y concisa (14 palabras)
  • Tono: 4/5
    └─ Tono cálido, empático con español argentino

  ⭐ PROMEDIO: 4.5/5

✅ Aspectos Positivos:
  • Usa español argentino (vos/podés)
  • Recomienda producto específico
  • Respuesta breve y concisa

⚠️ Aspectos a Mejorar:
  • Ninguno identificado

================================================================================
📊 RESUMEN GENERAL
================================================================================

📈 Promedios por Métrica:
  • Detección de Intención: 4.25/5
  • Relevancia: 4.50/5
  • Claridad: 4.00/5
  • Tono: 4.12/5

  ⭐ PROMEDIO GENERAL: 4.22/5

  ✅ BUENO

💡 Recomendaciones Generales:
  • Reforzar uso de español argentino (vos/podés) en system prompt
```

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
- Usar la versión demo: `test_chatbot_evaluation_demo.py`
- Reducir el número de casos en el script

---

## 📚 Documentación Adicional

- **`docs/evaluacion_chatbot.md`**: Plantilla para evaluación manual
- **`docs/COMO_EVALUAR_CHATBOT.md`**: Guía completa de evaluación
- **`tests/test_chatbot_evaluation.py`**: Script con Ollama real
- **`tests/test_chatbot_evaluation_demo.py`**: Script con respuestas simuladas

---

## 💡 Tips

✅ **Ejecutá la evaluación regularmente** (semanal o después de cambios)  
✅ **Compará resultados** antes y después de mejoras  
✅ **Documentá patrones** de fallas recurrentes  
✅ **Usa la versión demo** para entender el sistema  
✅ **Usa la versión real** para evaluar el chatbot en producción  

---

## 🎯 Próximos Pasos

1. ✅ Ejecutar `test_chatbot_evaluation_demo.py` para ver cómo funciona
2. ✅ Revisar los resultados y entender las métricas
3. ✅ Ejecutar `test_chatbot_evaluation.py` con Ollama para evaluación real
4. ✅ Implementar mejoras según las recomendaciones
5. ✅ Re-evaluar después de cada cambio

---

## 📞 Soporte

Si encontrás problemas, documentalos en `docs/evaluacion_chatbot.md` para análisis posterior.
