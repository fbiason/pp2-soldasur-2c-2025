/* ============================================
   SISTEMA EXPERTO - CÁLCULO DE CALEFACCIÓN
   ============================================ */

/* Variables del sistema experto */
let conversationStep = 0;
let userInputs = {};
let contextData = {};

/* Iniciar flujo del sistema experto */
function startExpertSystem() {
    conversationStep = 0;
    userInputs = {};
    contextData = {};
    updateContextPanel();
    
    appendMessage('system', '¡Perfecto! Te guiaré paso a paso para calcular tu sistema de calefacción.');
    setTimeout(() => askQuestion(), 500);
}

/* Preguntar siguiente paso del flujo */
function askQuestion() {
    conversationStep++;
    
    if (conversationStep === 1) {
        appendMessage('system', '¿Qué tipo de calefacción deseas calcular?');
        renderOptions(['Piso radiante', 'Radiadores', 'Calderas'], false);
    } else if (conversationStep === 2) {
        appendMessage('system', '¿Cuál es la superficie a calefaccionar?');
        createNumberInput({ input_label: 'Superficie en m²' });
    } else if (conversationStep === 3) {
        const superficie = userInputs.superficie;
        contextData.superficie = superficie + ' m²';
        updateContextPanel();
        appendMessage('system', `Perfecto, ${superficie}m². ¿En qué zona geográfica se encuentra?`);
        renderOptions(['Norte', 'Centro', 'Sur'], false);
    } else if (conversationStep === 4) {
        const zona = userInputs.zona;
        contextData.zona = zona;
        updateContextPanel();
        appendMessage('system', '¿Cuál es el nivel de aislación térmica de la vivienda?');
        renderOptions(['Buena', 'Regular', 'Mala'], false);
    } else if (conversationStep === 5) {
        calculateHeatingLoad();
    }
}

/* Calcular carga térmica */
function calculateHeatingLoad() {
    const superficie = parseFloat(userInputs.superficie);
    const zona = userInputs.zona;
    const aislacion = userInputs.aislacion;
    const tipo = userInputs.tipo;
    
    let factor = zona === 'Norte' ? 80 : zona === 'Centro' ? 100 : 125;
    if (aislacion === 'Mala') factor *= 1.2;
    if (aislacion === 'Buena') factor *= 0.9;
    
    const cargaTermica = Math.round(superficie * factor);
    contextData['Carga térmica'] = cargaTermica + ' W';
    updateContextPanel();
    
    appendMessage('system', `🎉 ¡Cálculo completado!<br><br>📊 Resultados:<br>- Superficie: ${superficie}m²<br>- Zona: ${zona}<br>- Aislación: ${aislacion}<br>- Carga térmica: ${cargaTermica} W<br><br>💡 Productos recomendados:`);
    
    setTimeout(() => {
        showRecommendedProducts(tipo);
        renderOptions(['Nuevo cálculo', 'Hacer una pregunta'], false);
    }, 500);
}

/* Mostrar productos recomendados según el tipo */
function showRecommendedProducts(tipo) {
    let recommendedProducts = [];
    if (tipo.toLowerCase().includes('radiador')) {
        recommendedProducts = peisaProducts.filter(p => p.family === 'Radiadores');
    } else if (tipo.toLowerCase().includes('caldera')) {
        recommendedProducts = peisaProducts.filter(p => p.family === 'Calderas');
    } else if (tipo.toLowerCase().includes('piso')) {
        recommendedProducts = peisaProducts.filter(p => 
            p.family === 'Calderas' || p.model.toLowerCase().includes('piso')
        );
    }
    
    if (recommendedProducts.length === 0) {
        recommendedProducts = [...peisaProducts.filter(p => p.family === 'Calderas').slice(0, 2),
                              ...peisaProducts.filter(p => p.family === 'Radiadores').slice(0, 2)];
    }
    
    renderProducts(recommendedProducts.slice(0, 5));
}

/* Manejar respuestas del sistema experto */
function handleExpertSystemResponse(option) {
    if (conversationStep === 1) {
        userInputs.tipo = option;
        contextData.tipo = option;
    } else if (conversationStep === 3) {
        userInputs.zona = option;
    } else if (conversationStep === 4) {
        userInputs.aislacion = option;
    }
    
    setTimeout(() => askQuestion(), 500);
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
            userInputs.superficie = value;
            appendMessage('user', value + ' m²');
            setTimeout(() => askQuestion(), 500);
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
    conversationStep = 0;
    userInputs = {};
    contextData = {};
    updateContextPanel();
}

/* Actualizar panel de contexto */
function updateContextPanel() {
    const panel = document.getElementById('context-panel');
    const itemsContainer = document.getElementById('context-items');
    
    if (Object.keys(contextData).length === 0) {
        panel.classList.add('hidden');
        return;
    }

    panel.classList.remove('hidden');
    itemsContainer.innerHTML = '';

    for (const [key, value] of Object.entries(contextData)) {
        if (!key.includes('_texto') && typeof value !== 'object') {
            const item = document.createElement('div');
            item.className = 'context-item';
            item.innerHTML = `<span class="font-medium">${key}:</span><span>${value}</span>`;
            itemsContainer.appendChild(item);
        }
    }
}
