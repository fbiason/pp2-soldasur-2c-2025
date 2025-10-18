# Registro de Pruebas (Testing Log)

## 18 de Octubre, 2025

**Funcionalidad Probada:** Flujo completo del Sistema Experto.

**Pasos:**
1.  Iniciar el chat y seleccionar "Guíame en un cálculo".
2.  **Prueba de Piso Radiante:** Completar el flujo (Superficie, Zona, etc.).
3.  **Prueba de Radiadores:** Completar el flujo (Dimensiones, Aislación, etc.).
4.  **Prueba de Calderas:** Completar el flujo (Carga térmica, Tipo de caldera).

📊 Resultados:

✅ ÉXITO: El frontend (soldasur.js) ahora se comunica correctamente con el backend (app.py).

✅ ÉXITO: El flujo de "Piso Radiante" funciona y da un resultado.

✅ ÉXITO: El flujo de "Radiadores" (que antes mostraba productos) ahora hace las preguntas correctas (dimensiones, etc.) y da el cálculo de módulos.

✅ ÉXITO: El flujo de "Calderas" (que antes mostraba productos) ahora hace las preguntas correctas (carga térmica, tipo) y recomienda una caldera.

📈 Estado: El sistema de cálculo guiado está 100% funcional. 
