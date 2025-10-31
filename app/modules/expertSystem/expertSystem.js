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
    
    appendMessage('system', `🎉 ¡Cálculo completado!<br><br>📊 Resultados:<br>- Superficie: ${superficie}m²<br>- Zona: ${zona}<br>- Aislación: ${aislacion}<br>- Carga térmica: ${cargaTermica} W<br><br>💡 Producto recomendado:`);
    
    setTimeout(() => {
        showRecommendedProducts(tipo);
        renderOptions(['Nuevo cálculo', 'Hacer una pregunta'], false);
    }, 500);
}

/* Mostrar productos recomendados según el tipo y características */
function showRecommendedProducts(tipo) {
    // Usar el catálogo JSON cargado globalmente
    const catalogToUse = peisaProductsFromJSON || [];
    
    if (catalogToUse.length === 0) {
        console.error('❌ Catálogo de productos no cargado');
        return;
    }
    
    const cargaTermica = parseFloat(contextData['Carga térmica']) || 0;
    let recommendedProducts = [];
    
    // Filtrar por tipo de sistema
    if (tipo.toLowerCase().includes('radiador')) {
        // Para radiadores, recomendar según la carga térmica
        recommendedProducts = catalogToUse.filter(p => p.family === 'Radiadores');
        
        // Priorizar radiadores eléctricos para cargas pequeñas (<2000W)
        if (cargaTermica < 2000) {
            recommendedProducts = recommendedProducts.filter(p => 
                p.model.toLowerCase().includes('eléctrico') || 
                p.model.toLowerCase().includes('electrico')
            );
        }
    } else if (tipo.toLowerCase().includes('caldera')) {
        // Para calderas, recomendar calderas murales
        recommendedProducts = catalogToUse.filter(p => 
            p.family === 'Calderas' && 
            (p.category?.toLowerCase().includes('mural') || 
             p.description?.toLowerCase().includes('mural'))
        );
    } else if (tipo.toLowerCase().includes('piso')) {
        // Para piso radiante, recomendar calderas doble servicio
        recommendedProducts = catalogToUse.filter(p => 
            p.family === 'Calderas' && 
            (p.description?.toLowerCase().includes('doble servicio') ||
             p.model.toLowerCase().includes('prima'))
        );
    }
    
    // Si no hay productos específicos, usar productos populares
    if (recommendedProducts.length === 0) {
        recommendedProducts = catalogToUse.filter(p => 
            p.model.includes('Prima Tec Smart') || 
            p.model.includes('Radiador Eléctrico Broen E') ||
            p.model.includes('Caldera Diva')
        );
    }
    
    // RECOMENDAR SOLO 1 PRODUCTO (el más adecuado)
    const finalProducts = recommendedProducts.slice(0, 1);
    
    console.log('💡 Producto recomendado para', tipo, '(carga:', cargaTermica, 'W):', finalProducts.length);
    
    if (finalProducts.length > 0) {
        renderProducts(finalProducts);
    } else {
        console.error('❌ No se encontraron productos para recomendar');
    }
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
