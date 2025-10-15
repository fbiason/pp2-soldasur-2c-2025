# Widget Flotante de Chat - PEISA SOLDASUR

## Descripción

Widget de chat flotante estilo chatbot moderno con integración de OpenAI GPT-4 y catálogo real de productos PEISA.

## Características del Widget

### 🎨 Diseño UX/UI

1. **Botón Flotante**
   - Ubicación: Esquina inferior derecha
   - Diseño: Circular con gradiente púrpura-azul
   - Animación: Efecto pulse continuo
   - Badge: Notificación roja con número
   - Tooltip: Mensaje de bienvenida al hacer hover

2. **Ventana de Chat**
   - Tamaño: 400x600px (responsive)
   - Posición: Flotante sobre el contenido
   - Animación: Slide-up suave al abrir
   - Sombra: Shadow-2xl para profundidad
   - Cierre: Botón X con rotación al hover

3. **Responsive**
   - Mobile: Ocupa casi toda la pantalla
   - Desktop: Widget de tamaño fijo
   - Adaptación automática según viewport

### ⚡ Funcionalidades

1. **Abrir/Cerrar Chat**
   - Click en botón flotante: Abre el chat
   - Click en X: Cierra el chat
   - Primera apertura: Inicia conversación automáticamente

2. **Tres Modos de Interacción**
   - 🤖 Guíame en un cálculo: Flujo paso a paso
   - 💬 Tengo una pregunta: Chat libre con IA
   - 📦 Buscar productos: Navegación por categorías

3. **Navegación**
   - Botón "Volver": Regresa al menú principal
   - Aparece automáticamente al entrar en un modo
   - Limpia el estado al volver

### 🔧 Implementación Técnica

#### HTML
```html
<!-- Botón flotante -->
<div class="chat-button" onclick="toggleChat()">
    <svg>...</svg>
    <span class="chat-badge">1</span>
</div>

<!-- Widget de chat -->
<div class="chat-container-wrapper" id="chat-widget">
    <!-- Contenido del chat -->
</div>
```

#### CSS
- Animaciones suaves con keyframes
- Transiciones de 0.3s para interacciones
- Z-index: 999-1000 para superposición
- Media queries para responsive

#### JavaScript
```javascript
function toggleChat() {
    chatIsOpen = !chatIsOpen;
    if (chatIsOpen) {
        // Mostrar widget
        chatWidget.classList.add('active');
        chatButton.style.display = 'none';
        // Iniciar conversación si es primera vez
        if (chatContainer.children.length === 0) {
            startConversation();
        }
    } else {
        // Ocultar widget
        chatWidget.classList.remove('active');
        chatButton.style.display = 'flex';
    }
}
```

## Uso

### Para el Usuario Final

1. **Abrir el chat**: Hacer clic en el botón flotante morado en la esquina inferior derecha
2. **Seleccionar opción**: Elegir entre cálculo guiado, pregunta libre o búsqueda de productos
3. **Interactuar**: Seguir las instrucciones del asistente
4. **Volver**: Usar el botón "Volver" para regresar al menú principal
5. **Cerrar**: Hacer clic en la X para cerrar el widget

### Para Desarrolladores

#### Integrar en tu sitio web

1. **Copiar el archivo**: `demo_standalone.html`

2. **Configurar API Key**: Reemplazar la API Key de OpenAI
```javascript
const OPENAI_API_KEY = 'tu-api-key-aqui';
```

3. **Personalizar colores**: Modificar el gradiente del botón
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

4. **Ajustar posición**: Cambiar bottom/right del botón
```css
.chat-button {
    bottom: 24px;
    right: 24px;
}
```

5. **Modificar productos**: Actualizar el array `peisaProducts`

## Características Avanzadas

### Badge de Notificación
- Muestra "1" por defecto
- Se oculta al abrir el chat
- Útil para indicar mensajes nuevos

### Tooltip Interactivo
- Aparece al hacer hover sobre el botón
- Mensaje personalizable
- Flecha apuntando al botón

### Animaciones
- **Pulse**: Latido continuo del botón
- **Slide-up**: Aparición suave del widget
- **Fade-in**: Mensajes del chat
- **Rotate**: Botón de cerrar al hover

### Gestión de Estado
```javascript
let chatIsOpen = false;           // Estado del widget
let conversationHistory = [];     // Historial con OpenAI
let conversationStep = 0;         // Paso actual del flujo
let inMainMenu = true;            // Estado de navegación
```

## Mejores Prácticas

### UX
- ✅ Botón siempre visible y accesible
- ✅ Animaciones suaves (no bruscas)
- ✅ Feedback visual en todas las interacciones
- ✅ Cierre fácil e intuitivo
- ✅ Responsive en todos los dispositivos

### Performance
- ✅ Carga diferida del chat (solo al abrir)
- ✅ Animaciones con CSS (no JS)
- ✅ Gestión eficiente del DOM
- ✅ Caché de respuestas frecuentes

### Accesibilidad
- ✅ Contraste adecuado de colores
- ✅ Tamaños de fuente legibles
- ✅ Áreas de click suficientemente grandes
- ✅ Navegación por teclado (mejora futura)

## Próximas Mejoras

1. **Persistencia**: Guardar conversación en localStorage
2. **Notificaciones**: Sistema de notificaciones push
3. **Multimedia**: Soporte para imágenes y videos
4. **Voz**: Integración con Web Speech API
5. **Analytics**: Tracking de interacciones
6. **A/B Testing**: Diferentes variantes del widget
7. **Personalización**: Temas y colores configurables
8. **Offline**: Modo offline con respuestas predefinidas

## Soporte

Para preguntas o problemas, contactar al equipo de desarrollo.

## Licencia

Uso interno - PEISA SOLDASUR 2025
