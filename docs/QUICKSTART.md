# 🚀 Guía de Inicio Rápido - SOLDASUR 2025

## ⚡ En 5 minutos

### Paso 1: Instalar Ollama (2 minutos)

#### Windows
1. Descargar desde: https://ollama.ai/download/windows
2. Ejecutar el instalador
3. Ollama se iniciará automáticamente

#### macOS
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

#### Linux
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### Paso 2: Descargar el modelo (1 minuto)

```bash
ollama pull llama3.2:3b
```

**Nota:** El modelo pesa ~2GB. La descarga puede tardar según tu conexión.

### Paso 3: Configurar Ollama (30 segundos)

1. Abrir la aplicación Ollama
2. Ir a **Settings** (⚙️)
3. Activar: **"Expose Ollama to the network"** ✅

### Paso 4: Verificar instalación (30 segundos)

```bash
ollama list
```

Deberías ver:
```
NAME              ID              SIZE      MODIFIED
llama3.2:3b       a80c4f17acd5    2.0 GB    X days ago
```

### Paso 5: Ejecutar la aplicación (1 minuto)

#### Opción A: Abrir directamente
1. Navegar a la carpeta `app/`
2. Hacer doble clic en `soldasur2025.html`
3. ¡Listo! 🎉

#### Opción B: Con servidor local (recomendado)
```bash
cd app
python -m http.server 8000
```

Abrir en el navegador: http://localhost:8000/soldasur2025.html

---

## 🎮 Cómo usar

### 1. Abrir el chat
- Buscar el botón flotante de **Soldy** en la esquina inferior derecha
- Hacer clic para abrir el chat

### 2. Elegir modo de interacción

#### 🤖 Guíame en un cálculo
**Cuándo usar:** Necesitas calcular la calefacción para un espacio

**Flujo:**
1. Tipo de calefacción → Piso radiante / Radiadores / Calderas
2. Superficie → Ingresa los m²
3. Zona geográfica → Norte / Centro / Sur
4. Aislación → Buena / Regular / Mala
5. **Resultado:** Carga térmica + Productos recomendados

**Ejemplo:**
```
Usuario: [Selecciona "Guíame en un cálculo"]
Soldy: ¿Qué tipo de calefacción deseas calcular?
Usuario: [Selecciona "Radiadores"]
Soldy: ¿Cuál es la superficie a calefaccionar?
Usuario: 50 m²
...
```

#### 💬 Tengo una pregunta
**Cuándo usar:** Tienes una consulta específica o abierta

**Ejemplos de preguntas:**
- "¿Qué diferencia hay entre una caldera mural y una de potencia?"
- "¿Cuál es el mejor radiador para un baño?"
- "¿Cómo funciona un termotanque solar?"
- "Necesito climatizar una piscina de 40m³"
- "¿Qué mantenimiento requiere una caldera?"

**Ventaja:** Ollama procesa tu pregunta con contexto del catálogo completo

#### 📦 Buscar productos
**Cuándo usar:** Quieres explorar el catálogo

**Categorías disponibles:**
- **Calderas** (11 productos)
- **Radiadores** (8 productos)
- **Termotanques** (3 productos)
- **Calefones** (2 productos)
- **Toalleros** (6 productos)
- **Climatizadores** (3 productos)
- **Termostatos** (2 productos)

**Acción:** Haz clic en cualquier producto para ver detalles en la web de PEISA

---

## 🔧 Solución de Problemas

### ❌ "Error en la API de Ollama"

**Problema:** Ollama no está corriendo o no está expuesto

**Solución:**
1. Verificar que Ollama está activo:
   ```bash
   ollama list
   ```
2. Abrir Ollama → Settings → Activar "Expose Ollama to the network"
3. Reiniciar Ollama

### ❌ El chat no responde

**Verificar:**
1. Consola del navegador (F12) para ver errores
2. Ollama está corriendo: `ollama list`
3. El modelo está descargado: debe aparecer `llama3.2:3b`
4. Puerto correcto: `http://localhost:11434`

### ❌ Respuestas muy lentas

**Causa:** Hardware limitado o modelo muy grande

**Solución:**
- El modelo `llama3.2:3b` es el más rápido (2GB)
- Si tienes problemas, verifica:
  - RAM disponible (mínimo 4GB libres)
  - Cierra otras aplicaciones pesadas

### ❌ Error de CORS

**Causa:** Restricciones del navegador

**Solución:**
- No abrir el HTML directamente
- Usar un servidor local:
  ```bash
  python -m http.server 8000
  ```

---

## 💡 Tips y Trucos

### Para mejores respuestas:
1. **Sé específico:** "Necesito radiadores para 50m² en zona fría" es mejor que "¿Qué radiador me conviene?"
2. **Menciona detalles:** Superficie, zona, tipo de instalación, presupuesto
3. **Pregunta paso a paso:** Si tienes varias dudas, hazlas una por una

### Para cálculos precisos:
1. Usa el modo **"Guíame en un cálculo"**
2. Proporciona datos exactos de superficie
3. Considera el nivel de aislación real de tu vivienda

### Para explorar productos:
1. Usa **"Buscar productos"** para ver el catálogo completo
2. Haz clic en los productos para ver especificaciones técnicas
3. Pregunta en el chat sobre comparaciones entre modelos

---

## 📊 Rendimiento Esperado

### Tiempos de respuesta (Llama 3.2 3B)

| Hardware | Primera respuesta | Respuestas siguientes |
|----------|-------------------|----------------------|
| CPU moderna (i5/Ryzen 5+) | 3-5 seg | 2-3 seg |
| GPU integrada | 2-3 seg | 1-2 seg |
| GPU dedicada (GTX 1060+) | 1-2 seg | 0.5-1 seg |

### Consumo de recursos

- **RAM:** 4-6 GB (modelo + overhead)
- **Disco:** 2 GB (modelo)
- **CPU:** Variable (20-80% durante generación)

---

## 🎯 Casos de Uso Comunes

### Caso 1: Cliente nuevo
```
Usuario: Hola, necesito calefaccionar mi casa
Soldy: ¡Hola! Puedo ayudarte. ¿Prefieres que te guíe paso a paso 
       en un cálculo o tienes una pregunta específica?
Usuario: [Selecciona "Guíame en un cálculo"]
→ Flujo estructurado con resultado preciso
```

### Caso 2: Consulta técnica
```
Usuario: [Selecciona "Tengo una pregunta"]
Usuario: ¿Qué diferencia hay entre Prima Tec y Diva Tecno?
Soldy: [Ollama procesa y responde con detalles técnicos]
→ Respuesta contextualizada del catálogo
```

### Caso 3: Exploración de productos
```
Usuario: [Selecciona "Buscar productos"]
Usuario: [Selecciona "Radiadores"]
Soldy: Aquí están nuestros 8 productos de Radiadores
→ Muestra tarjetas con todos los radiadores
```

---

## 📱 Compatibilidad

### Navegadores soportados:
- ✅ Chrome/Edge (Recomendado)
- ✅ Firefox
- ✅ Safari
- ⚠️ Internet Explorer (No soportado)

### Sistemas operativos:
- ✅ Windows 10/11
- ✅ macOS 11+
- ✅ Linux (Ubuntu, Fedora, etc.)

---

## 🆘 Soporte

### Recursos útiles:
- 📖 [Documentación completa](docs/README_STANDALONE_OLLAMA.md)
- 📝 [Changelog](CHANGELOG.md)
- 🔧 [Documentación Ollama](https://ollama.ai/docs)

### Contacto:
- **Proyecto:** SOLDASUR 2025
- **Email:** franco.biason@gmail.com

---

## ✅ Checklist de Verificación

Antes de reportar un problema, verifica:

- [ ] Ollama está instalado y corriendo
- [ ] Modelo `llama3.2:3b` está descargado
- [ ] "Expose Ollama to the network" está activado
- [ ] El navegador puede acceder a `http://localhost:11434`
- [ ] No hay errores en la consola del navegador (F12)
- [ ] Tienes al menos 4GB de RAM libre

---

**¡Listo para empezar! 🚀**

Si todo está configurado correctamente, deberías poder chatear con Soldy en menos de 5 minutos.

**¿Problemas?** Revisa la sección de [Solución de Problemas](#-solución-de-problemas) o consulta la [documentación completa](docs/README_STANDALONE_OLLAMA.md).
