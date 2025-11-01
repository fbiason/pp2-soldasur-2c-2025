/* ============================================
   SISTEMA EXPERTO - CÁLCULO DE CALEFACCIÓN
   ============================================ */

/* Variables del sistema experto */
let expertConversationId = null;
let currentNodeData = null;

/* Iniciar flujo del sistema experto */
async function startExpertSystem() {
    console.log('[DEBUG] startExpertSystem() iniciado');
    
    // Generar ID único para la conversación
    expertConversationId = 'conv_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    console.log('[DEBUG] Conversation ID:', expertConversationId);
    
    updateContextPanel();
    
    appendMessage('system', '¡Perfecto! Te guiaré paso a paso para calcular tu sistema de calefacción.');
    console.log('[DEBUG] Mensaje inicial enviado');
    
    try {
        console.log('[DEBUG] Iniciando fetch a /start');
        // Iniciar conversación con el backend
        const response = await fetch('/start', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ conversation_id: expertConversationId })
        });
        
        console.log('[DEBUG] Respuesta recibida:', response.status);
        const data = await response.json();
        console.log('[DEBUG] Datos parseados:', data);
        currentNodeData = data;
        
        // Mostrar la primera pregunta
        console.log('[DEBUG] Llamando a displayNodeMessage');
        displayNodeMessage(data);
        
    } catch (error) {
        console.error('[ERROR] Error iniciando sistema experto:', error);
        appendMessage('system', '❌ Error al iniciar el sistema. Por favor, intenta de nuevo.');
    }
}

/* Mostrar mensaje del nodo actual */
function displayNodeMessage(data) {
    console.log('[DEBUG] displayNodeMessage - data recibida:', data);
    
    if (data.error) {
        appendMessage('system', `❌ Error: ${data.error}`);
        return;
    }
    
    // Mostrar el texto de la pregunta o respuesta
    if (data.text) {
        appendMessage('system', data.text);
    }
    
    // Mostrar opciones si existen
    if (data.options && data.options.length > 0) {
        console.log('[DEBUG] Mostrando opciones:', data.options);
        renderExpertOptions(data.options);
    }
    // Mostrar input numérico si es necesario
    else if (data.input_type === 'number') {
        console.log('[DEBUG] Mostrando input numérico');
        createNumberInput(data);
    }
    // Mostrar inputs múltiples si es necesario
    else if (data.input_type === 'multiple' && data.inputs) {
        console.log('[DEBUG] Mostrando inputs múltiples:', data.inputs);
        createMultipleInputs(data);
    } else {
        console.log('[DEBUG] No se detectó qué mostrar. input_type:', data.input_type);
    }
    
    // Si es final, volver al menú principal
    if (data.is_final) {
        setTimeout(() => {
            // Volver al menú principal
            inMainMenu = true;
            hideBackButton();
            renderOptions(['Guíame en un cálculo', 'Hacer una pregunta', 'Buscar productos'], false);
        }, 500);
    }
}

/* OBSOLETO - Ahora el backend hace los cálculos */

/* OBSOLETO - Ahora el backend maneja las recomendaciones */

/* Enviar respuesta al backend */
async function sendExpertResponse(option_index = null, input_values = null) {
    try {
        const requestBody = {
            conversation_id: expertConversationId,
            option_index: option_index,
            input_values: input_values || {}
        };
        
        const response = await fetch('/reply', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(requestBody)
        });
        
        const data = await response.json();
        currentNodeData = data;
        
        // Mostrar el siguiente mensaje
        displayNodeMessage(data);
        
    } catch (error) {
        console.error('Error enviando respuesta:', error);
        appendMessage('system', '❌ Error al procesar tu respuesta. Por favor, intenta de nuevo.');
    }
}

/* Renderizar opciones del sistema experto */
function renderExpertOptions(options) {
    const inputArea = document.getElementById('input-area');
    inputArea.innerHTML = '';
    const container = document.createElement('div');
    container.className = 'space-y-2';
    
    options.forEach((option, idx) => {
        const btn = document.createElement('button');
        btn.className = 'option-btn w-full bg-blue-100 hover:bg-blue-200 text-blue-800 py-2 px-4 rounded';
        btn.textContent = option;
        btn.onclick = () => {
            appendMessage('user', option);
            inputArea.innerHTML = '';
            sendExpertResponse(idx, null);
        };
        container.appendChild(btn);
    });
    
    inputArea.appendChild(container);
    inputArea.classList.remove('hidden');
}

/* Manejar respuestas del sistema experto (cuando se selecciona una opción) */
function handleExpertSystemResponse(optionText) {
    // Encontrar el índice de la opción seleccionada
    const optionIndex = currentNodeData && currentNodeData.options ? 
        currentNodeData.options.findIndex(opt => opt === optionText) : -1;
    
    if (optionIndex >= 0) {
        sendExpertResponse(optionIndex, null);
    }
}

/* Crear input numérico */
function createNumberInput(response) {
    const inputArea = document.getElementById('input-area');
    inputArea.innerHTML = '';
    const form = document.createElement('form');
    form.onsubmit = (e) => {
        e.preventDefault();
        const value = document.getElementById('input-value').value;
        if (value && parseFloat(value) > 0) {
            appendMessage('user', value);
            inputArea.innerHTML = '';
            // Enviar al backend
            sendExpertResponse(null, { value: value });
        }
    };
    form.innerHTML = `
        <div class="flex flex-col space-y-2">
            <input type="number" id="input-value" required 
                class="border border-gray-300 rounded px-3 py-2" 
                placeholder="${response.input_label || 'Ej: 50'}">
            <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition">
                Enviar
            </button>
        </div>
    `;
    inputArea.appendChild(form);
    document.getElementById('input-value').focus();
}

/* Resetear sistema experto */
function resetExpertSystem() {
    expertConversationId = null;
    currentNodeData = null;
    updateContextPanel();
}

/* Actualizar panel de contexto */
function updateContextPanel() {
    const panel = document.getElementById('context-panel');
    const itemsContainer = document.getElementById('context-items');
    
    // Obtener variables del estado actual si existe
    const variables = currentNodeData?.expert_state?.variables || {};
    
    if (Object.keys(variables).length === 0) {
        panel.classList.add('hidden');
        return;
    }

    panel.classList.remove('hidden');
    itemsContainer.innerHTML = '';

    for (const [key, value] of Object.entries(variables)) {
        if (!key.includes('_texto') && typeof value !== 'object') {
            const item = document.createElement('div');
            item.className = 'context-item';
            item.innerHTML = `<span class="font-medium">${key}:</span><span>${value}</span>`;
            itemsContainer.appendChild(item);
        }
    }
}

/* Crear inputs múltiples */
function createMultipleInputs(response) {
    const inputArea = document.getElementById('input-area');
    inputArea.innerHTML = '';
    
    const form = document.createElement('form');
    form.className = 'space-y-3';
    
    const inputs = response.inputs || [];
    const inputElements = {};
    
    inputs.forEach(inputConfig => {
        const inputGroup = document.createElement('div');
        inputGroup.className = 'flex flex-col';
        
        const label = document.createElement('label');
        label.textContent = inputConfig.label;
        label.className = 'text-sm font-medium mb-1';
        
        const input = document.createElement('input');
        input.type = inputConfig.type || 'number';
        input.name = inputConfig.name;
        input.className = 'px-3 py-2 border rounded-lg';
        input.required = true;
        input.step = '0.01';
        input.min = '0';
        
        inputElements[inputConfig.name] = input;
        
        inputGroup.appendChild(label);
        inputGroup.appendChild(input);
        form.appendChild(inputGroup);
    });
    
    const button = document.createElement('button');
    button.type = 'submit';
    button.textContent = 'Continuar';
    button.className = 'bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 w-full';
    form.appendChild(button);
    
    form.onsubmit = (e) => {
        e.preventDefault();
        const values = {};
        
        // Recoger todos los valores
        for (const [name, inputEl] of Object.entries(inputElements)) {
            values[name] = inputEl.value;
            appendMessage('user', `${name}: ${inputEl.value}`);
        }
        
        inputArea.innerHTML = '';
        // Enviar al backend
        sendExpertResponse(null, values);
    };
    
    inputArea.appendChild(form);
    inputArea.classList.remove('hidden');
}
