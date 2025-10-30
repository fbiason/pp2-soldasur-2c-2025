/* ========== ESTADO GLOBAL ========== */
let conversationId = 'user_' + Math.random().toString(36).substr(2, 9);
let lastUserResponse = null;
let isLoading = false;
let currentMode = 'hybrid';
let inMainMenu = true;

/* ========== TOGGLE DEL CHAT FLOTANTE ========== */
let chatIsOpen = false;
let isMaximized = false;

function toggleMaximize() {
    const chatWidget = document.getElementById('chat-widget');
    const maximizeIcon = document.getElementById('maximize-icon');
    const minimizeIcon = document.getElementById('minimize-icon');
    const maximizeButton = document.getElementById('maximize-button');
    
    isMaximized = !isMaximized;
    
    if (isMaximized) {
        chatWidget.classList.add('maximized');
        maximizeIcon.classList.add('hidden');
        minimizeIcon.classList.remove('hidden');
        maximizeButton.title = 'Restaurar';
    } else {
        chatWidget.classList.remove('maximized');
        maximizeIcon.classList.remove('hidden');
        minimizeIcon.classList.add('hidden');
        maximizeButton.title = 'Maximizar';
    }
}

function toggleChat() {
    const chatWidget = document.getElementById('chat-widget');
    const chatButton = document.getElementById('chat-toggle-btn');
    const soldyMessage = document.getElementById('soldy-message');
    const soldyChatImage = document.getElementById('soldy-chat-image');
    
    chatIsOpen = !chatIsOpen;
    
    if (chatIsOpen) {
        chatWidget.classList.add('active');
        chatButton.style.display = 'none';
        if (soldyChatImage) {
            soldyChatImage.style.display = 'block';
        }
        if (soldyMessage) {
            soldyMessage.classList.add('hidden');
        }
        if (document.getElementById('chat-container').children.length === 0) {
            startConversation();
        }
    } else {
        chatWidget.classList.remove('active');
        chatButton.style.display = 'block';
        if (soldyChatImage) {
            soldyChatImage.style.display = 'none';
        }
        if (soldyMessage) {
            soldyMessage.classList.remove('hidden');
        }
    }
}

/* ========== INICIALIZACIÓN ========== */
document.addEventListener('DOMContentLoaded', () => {
    // Ocultar mensaje de bienvenida después de 8 segundos
    setTimeout(() => {
        const soldyMessage = document.getElementById('soldy-message');
        if (soldyMessage && !chatIsOpen) {
            soldyMessage.style.animation = 'fadeOut 0.5s ease-out forwards';
            setTimeout(() => {
                soldyMessage.style.display = 'none';
            }, 500);
        }
    }, 8000);
    
    // Login (mantenido por compatibilidad)
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const username = document.getElementById('login-username').value.trim();
            const password = document.getElementById('login-password').value.trim();
            const errorLabel = document.getElementById('login-error');

            if (username === 'admin' && password === 'admin') {
                document.getElementById('login-overlay').classList.add('hidden');
                startConversation();
            } else {
                errorLabel.textContent = 'Usuario o contraseña incorrectos';
            }
        });
    }
});

/* ========== NAVEGACIÓN ========== */
function showBackButton() {
    document.getElementById('back-button').classList.remove('hidden');
    inMainMenu = false;
}

function hideBackButton() {
    document.getElementById('back-button').classList.add('hidden');
    inMainMenu = true;
}

function goBack() {
    resetExpertSystem();
    // NO resetear el historial del chatbot para mantener contexto
    document.getElementById('chat-container').innerHTML = '';
    startConversation();
    hideBackButton();
}

function switchMode(mode) {
    currentMode = mode;
    conversationId = 'user_' + Math.random().toString(36).substr(2, 9);
    document.getElementById('chat-container').innerHTML = '';
    lastUserResponse = null;
    resetExpertSystem();
    // Resetear historial del chatbot solo si se cambia explícitamente de modo
    if (typeof resetChatHistory === 'function') {
        resetChatHistory();
    }
    startConversation();
    hideBackButton();
}

/* ========== INICIO DE CONVERSACIÓN ========== */
function startConversation() {
    resetExpertSystem();
    appendMessage('system', '¡Hola! Soy <strong>Soldy</strong> tu asistente inteligente de SOLDASUR. Puedo ayudarte de diferentes formas. ¿Qué necesitas?');
    renderOptions(['Guíame en un cálculo', 'Tengo una pregunta', 'Buscar productos'], false);
}

/* ========== MANEJO DE OPCIONES ========== */
function handleOptionClick(option) {
    appendMessage('user', option);
    
    // Categorías de productos
    const productCategories = ['Calderas', 'Radiadores', 'Termotanques', 'Calefones', 'Toalleros', 'Climatizadores', 'Termostatos'];
    
    if (conversationStep === 0 && productCategories.includes(option)) {
        showProductsByCategory(option);
        return;
    }
    
    // Navegación de catálogo
    if (option === 'Ver todos') {
        showAllProducts();
        return;
    } else if (option === '📦 Ver otras categorías' || option === '📦 Ver por categoría') {
        showCategoryMenu();
        return;
    }
    
    // Opciones iniciales del menú principal
    if (conversationStep === 0) {
        if (option.includes('Guíame') || option.includes('cálculo')) {
            showBackButton();
            startExpertSystem();
        } else if (option.includes('pregunta')) {
            showBackButton();
            startChatbot();
        } else if (option.includes('Buscar') || option.includes('productos')) {
            showBackButton();
            showCategoryMenu();
        }
        return;
    }
    
    // Respuestas del sistema experto
    if (conversationStep >= 1 && conversationStep <= 4) {
        handleExpertSystemResponse(option);
        return;
    }
    
    // Opciones post-cálculo
    if (option === 'Nuevo cálculo' || option.includes('Hacer un cálculo')) {
        resetExpertSystem();
        appendMessage('system', '¡Perfecto! Iniciemos un nuevo cálculo.');
        startExpertSystem();
    } else if (option === 'Hacer una pregunta' || option.includes('pregunta')) {
        startChatbot();
    }
}

/* ========== RENDERIZADO DE UI ========== */
function renderOptions(options, isResponse = false) {
    const inputArea = document.getElementById('input-area');
    inputArea.innerHTML = '';
    const container = document.createElement('div');
    container.className = 'space-y-2';
    
    options.forEach((option, idx) => {
        const btn = document.createElement('button');
        btn.className = `option-btn w-full ${isResponse ? 'bg-green-100 hover:bg-green-200 text-green-800' : 'bg-blue-100 hover:bg-blue-200 text-blue-800'} py-2 px-4 rounded`;
        btn.textContent = option;
        btn.onclick = () => handleOptionClick(option);
        container.appendChild(btn);
    });
    
    inputArea.appendChild(container);
}

function renderSuggestion(suggestion) {
    const box = document.createElement('div');
    box.className = 'suggestion-box fade-in';
    box.innerHTML = `
        <div class="font-medium mb-2">${suggestion.message || suggestion}</div>
        ${suggestion.options ? `
            <div class="flex gap-2 mt-2">
                ${suggestion.options.map((opt, idx) => `
                    <button onclick="handleSuggestionOption(${idx})" 
                        class="text-xs px-3 py-1 bg-blue-100 hover:bg-blue-200 text-blue-800 rounded transition">
                        ${opt}
                    </button>
                `).join('')}
            </div>
        ` : ''}
    `;
    document.getElementById('chat-container').appendChild(box);
}

function createMultipleInputs(inputs) {
    const inputArea = document.getElementById('input-area');
    const form = document.createElement('form');
    form.onsubmit = (e) => {
        e.preventDefault();
        if (isLoading) return;
        const values = {};
        inputs.forEach(inp => {
            values[inp.name] = document.getElementById(`input-${inp.name}`).value;
        });
        lastUserResponse = `Valores ingresados: ${Object.entries(values).map(([k,v]) => `${k}=${v}`).join(', ')}`;
    };
    
    const fieldsHTML = inputs.map(inp => `
        <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">${inp.label}</label>
            <input type="${inp.type || 'text'}" inputmode="decimal" id="input-${inp.name}" required 
                class="w-full border border-gray-300 rounded px-3 py-2" placeholder="Ej: 4.5">
        </div>
    `).join('');
    
    form.innerHTML = `
        <div class="space-y-4">
            ${fieldsHTML}
            <button type="submit" class="w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 transition">
                Calcular
            </button>
        </div>
    `;
    inputArea.appendChild(form);
}

function createRestartButton() {
    const inputArea = document.getElementById('input-area');
    const btn = document.createElement('button');
    btn.className = 'w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 transition';
    btn.textContent = 'Iniciar nuevo cálculo';
    btn.onclick = () => {
        if (isLoading) return;
        switchMode(currentMode);
    };
    inputArea.appendChild(btn);
}

/* ========== HELPERS ========== */
function appendMessage(sender, text) {
    const chatContainer = document.getElementById('chat-container');
    const div = document.createElement('div');
    div.className = `chat-message rounded-lg p-3 ${sender === 'system' ? 'system-message' : 'user-message'} fade-in`;
    div.innerHTML = text;
    chatContainer.appendChild(div);
    scrollToBottom();
}

function formatResponseText(text) {
    return text ? text.replace(/\n/g, '<br>').replace(/<br>- /g, '<br>• ') : '';
}

function scrollToBottom() {
    const container = document.getElementById('chat-container');
    container.scrollTop = container.scrollHeight;
}

function updateModeIndicator(mode, label) {
    const indicator = document.getElementById('mode-indicator');
    if (indicator) {
        indicator.textContent = label;
        indicator.className = 'mode-indicator';
        
        if (mode === 'expert') {
            indicator.classList.add('mode-expert');
        } else if (mode === 'rag') {
            indicator.classList.add('mode-rag');
        } else {
            indicator.classList.add('mode-hybrid');
        }
    }
}

/* ========== CONSULTA SUCURSAL (RIO GRANDE / USHUAIA) ========== */
function consultSucursal(city = null, showOnPage = true) {
    const sel = document.getElementById('city-select');
    const res = document.getElementById('sucursal-result');
    // determine city: priority param -> selector -> default
    const selectedCity = city || (sel ? sel.value : null);
    // info map
    const info = {
        rio_grande: {
            name: 'Sucursal Río Grande - Soldasur',
            address: 'Av. San Martín 1234, Río Grande, Tierra del Fuego',
            phone: '+54 2964 123456',
            email: 'riogrande@soldasur.com'
        },
        ushuaia: {
            name: 'Sucursal Ushuaia - Soldasur',
            address: 'Calle 9 de Julio 210, Ushuaia, Tierra del Fuego',
            phone: '+54 2901 654321',
            email: 'ushuaia@soldasur.com'
        }
    };

    const c = info[selectedCity];
    if (!c) {
        if (res) res.innerHTML = '';
        return;
    }

    // Mostrar en el widget (solo si showOnPage)
    if (showOnPage && res) {
        res.innerHTML = `
            <div class="p-3 bg-blue-50 rounded">
                <div class="font-semibold">${c.name}</div>
                <div class="text-sm text-gray-700">${c.address}</div>
                <div class="text-sm">Tel: <a href="tel:${c.phone.replace(/\s+/g,'')}" class="text-blue-600">${c.phone}</a></div>
                <div class="text-sm">Email: <a href="mailto:${c.email}" class="text-blue-600">${c.email}</a></div>
            </div>
        `;
    }

    // Añadir también un mensaje al chat para que quede en el historial
    if (typeof appendMessage === 'function') {
        // Si no se pasó ciudad y la llamada viene desde el chat (showOnPage=false),
        // presentar opciones interactivas para elegir sucursal dentro del chat.
        if (!selectedCity && !showOnPage) {
            const optionsHtml = `
                <div class="sucursal-options" style="display:flex;gap:8px;margin-top:8px;">
                    <button class="inline-block bg-blue-600 text-white px-3 py-1 rounded text-sm" onclick="consultSucursalFromChat('rio_grande')">Río Grande</button>
                    <button class="inline-block bg-blue-600 text-white px-3 py-1 rounded text-sm" onclick="consultSucursalFromChat('ushuaia')">Ushuaia</button>
                </div>
            `;
            appendMessage('system', `Seleccioná la sucursal:${optionsHtml}`);
        } else {
            // Añadir mensaje al chat con botones junto a la tarjeta de contacto
            const chatHtml = `
                <div class="sucursal-card">
                    <strong>${c.name}</strong><br>
                    ${c.address}<br>
                    Tel: <a href="tel:${c.phone.replace(/\s+/g,'')}" class="text-blue-600">${c.phone}</a><br>
                    Email: <a href="mailto:${c.email}" class="text-blue-600">${c.email}</a>
                    <div style="margin-top:8px; display:flex; gap:8px;">
                        <a href="tel:${c.phone.replace(/\s+/g,'')}" class="inline-block bg-blue-600 text-white px-3 py-1 rounded text-sm">Llamar</a>
                        <a href="mailto:${c.email}" class="inline-block bg-gray-200 text-gray-800 px-3 py-1 rounded text-sm">Email</a>
                        <button onclick="scrollToSucursal('${selectedCity}')" class="inline-block bg-green-600 text-white px-3 py-1 rounded text-sm">Ver sucursal</button>
                    </div>
                </div>
            `;
            appendMessage('system', chatHtml);
        }
    }
    // Asegurar scroll al final
    scrollToBottom();
}

// Desplazar a la tarjeta de sucursal en la página y aplicar un breve highlight
function scrollToSucursal(city) {
    const el = document.getElementById('sucursal-result');
    if (!el) return;
    el.scrollIntoView({ behavior: 'smooth', block: 'center' });
    // efecto highlight
    el.style.transition = 'box-shadow 0.3s ease, transform 0.15s ease';
    el.style.boxShadow = '0 6px 18px rgba(59,130,246,0.25)';
    el.style.transform = 'translateY(-2px)';
    setTimeout(() => {
        el.style.boxShadow = '';
        el.style.transform = '';
    }, 1200);
}

/* ========== CONSULTAR DESDE PRODUCTO ========== */
function consultFromProduct(productModel) {
    // Abrir chat si está cerrado
    if (!chatIsOpen) toggleChat();
    // Añadir mensaje de usuario indicando interés en el producto
    appendMessage('user', `Estoy interesado en: <strong>${productModel}</strong>`);
    // Mostrar la sección de consulta si existe
    const sel = document.getElementById('city-select');
    // Iniciar flujo de consulta dentro del chat: mostrar opciones de sucursal
    consultSucursal(null, false);
}

// Función llamada desde los botones de opciones dentro del chat
function consultSucursalFromChat(city) {
    // Añadir un mensaje de confirmación de selección en el chat
    appendMessage('user', `Seleccioné: <strong>${city === 'rio_grande' ? 'Río Grande' : 'Ushuaia'}</strong>`);
    // Mostrar la tarjeta correspondiente en el chat (sin actualizar la página)
    consultSucursal(city, false);
}
