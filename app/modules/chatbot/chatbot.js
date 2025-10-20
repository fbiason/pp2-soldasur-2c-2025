/* ============================================
   CHATBOT - INTEGRACIÓN CON OLLAMA
   ============================================ */

/* Configuración Ollama */
const OLLAMA_URL = 'http://localhost:11434/api/chat';
const OLLAMA_MODEL = 'llama3.2:3b';
const conversationHistory = [];

/* Iniciar modo chatbot */
function startChatbot() {
    appendMessage('system', '¿Qué necesitas saber?');
    showChatInput();
}

/* Mostrar input de chat */
function showChatInput() {
    const inputArea = document.getElementById('input-area');
    inputArea.innerHTML = `
        <div class="flex gap-2">
            <input type="text" id="chat-input" class="flex-1 border border-gray-300 rounded px-3 py-2" placeholder="Escribe tu pregunta...">
            <button onclick="handleChatInput()" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition">
                Enviar
            </button>
        </div>
    `;
    document.getElementById('chat-input').focus();
    document.getElementById('chat-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleChatInput();
    });
}

/* Manejar input de chat */
async function handleChatInput() {
    const input = document.getElementById('chat-input');
    const question = input.value.trim();
    
    if (question) {
        appendMessage('user', question);
        input.value = '';
        showLoadingIndicator();
        
        try {
            const response = await callOllama(question);
            hideLoadingIndicator();
            appendMessage('system', response.message);
            
            // Si Ollama recomienda productos, mostrarlos
            if (response.products && response.products.length > 0) {
                setTimeout(() => {
                    renderProducts(response.products);
                }, 300);
            }
            
            // Volver a mostrar el input
            showChatInput();
        } catch (error) {
            hideLoadingIndicator();
            appendMessage('system', 'Lo siento, hubo un error al procesar tu consulta. Por favor, intenta nuevamente.');
            showChatInput();
        }
    }
}

/* Llamar a la API de Ollama */
async function callOllama(userMessage) {
    // Crear el contexto del sistema con información de productos
    const systemPrompt = `Eres Soldy, vendedor experto de PEISA-SOLDASUR. VENDE productos en respuestas ULTRA CORTAS.

CATÁLOGO:
${JSON.stringify(peisaProducts, null, 2)}

REGLAS ESTRICTAS:
1. Máximo 1-2 oraciones (80-120 caracteres TOTAL)
2. SIEMPRE responde la pregunta del cliente PRIMERO
3. Luego recomienda 1 producto específico por nombre relacionado a su necesidad
4. Formato: [Respuesta breve a la pregunta] + [Producto recomendado] + [Beneficio]
5. Ejemplo pregunta "¿Cómo calefacciono 80m²?" → "Para 80m² te recomiendo la Prima Tec Smart, perfecta para calefacción eficiente."
6. Si la pregunta NO es sobre calefacción/productos, responde amablemente y ofrece ayuda con productos
7. SIN explicaciones técnicas largas

Respuestas en español argentino, tono cercano y profesional.`;

    // Agregar mensaje del usuario al historial
    conversationHistory.push({
        role: 'user',
        content: userMessage
    });

    // Preparar mensajes para Ollama (incluir system prompt solo la primera vez)
    const messages = conversationHistory.length === 1 
        ? [
            { role: 'system', content: systemPrompt },
            ...conversationHistory
          ]
        : conversationHistory;
    
    const response = await fetch(OLLAMA_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            model: OLLAMA_MODEL,
            messages: messages,
            stream: false,
            options: {
                temperature: 0.7,
                num_predict: 80
            }
        })
    });
    
    if (!response.ok) {
        throw new Error('Error en la API de Ollama');
    }
    
    const data = await response.json();
    const assistantMessage = data.message.content;
    
    // Agregar respuesta del asistente al historial
    conversationHistory.push({
        role: 'assistant',
        content: assistantMessage
    });
    
    // Detectar productos mencionados en la respuesta
    const mentionedProducts = detectMentionedProducts(assistantMessage);
    
    return {
        message: assistantMessage,
        products: mentionedProducts
    };
}

/* Detectar productos mencionados en la respuesta */
function detectMentionedProducts(message) {
    const mentioned = [];
    const messageLower = message.toLowerCase();
    
    for (const product of peisaProducts) {
        const modelLower = product.model.toLowerCase();
        if (messageLower.includes(modelLower)) {
            mentioned.push(product);
        }
    }
    
    // Si no se mencionan productos específicos pero se habla de categorías
    if (mentioned.length === 0) {
        if (messageLower.includes('caldera') || messageLower.includes('calderas')) {
            return peisaProducts.filter(p => p.family === 'Calderas').slice(0, 3);
        } else if (messageLower.includes('radiador') || messageLower.includes('radiadores')) {
            return peisaProducts.filter(p => p.family === 'Radiadores').slice(0, 3);
        } else if (messageLower.includes('toallero') || messageLower.includes('toalleros')) {
            return peisaProducts.filter(p => p.family === 'Toalleros').slice(0, 3);
        } else if (messageLower.includes('termotanque') || messageLower.includes('termotanques')) {
            return peisaProducts.filter(p => p.family === 'Termotanques').slice(0, 3);
        } else if (messageLower.includes('calefón') || messageLower.includes('calefones')) {
            return peisaProducts.filter(p => p.family === 'Calefones').slice(0, 3);
        }
    }
    
    return mentioned.slice(0, 5); // Limitar a 5 productos
}

/* Indicadores de carga */
function showLoadingIndicator() {
    document.getElementById('input-area').innerHTML = 
        '<div class="text-center py-2"><div class="loading-spinner inline-block"></div></div>';
    
    const chatContainer = document.getElementById('chat-container');
    const thinkingDiv = document.createElement('div');
    thinkingDiv.id = 'thinking-indicator';
    thinkingDiv.className = 'chat-message system-message rounded-lg p-3 fade-in';
    thinkingDiv.innerHTML = `
        <div class="flex items-center gap-2">
            <div class="loading-spinner inline-block"></div>
            <span class="thinking-text">Soldy está pensando</span>
        </div>
    `;
    chatContainer.appendChild(thinkingDiv);
    scrollToBottom();
    
    let dots = 0;
    window.thinkingInterval = setInterval(() => {
        dots = (dots + 1) % 4;
        const thinkingText = document.querySelector('.thinking-text');
        if (thinkingText) {
            thinkingText.textContent = 'Soldy está pensando' + '.'.repeat(dots);
        }
    }, 500);
}

function hideLoadingIndicator() {
    if (window.thinkingInterval) {
        clearInterval(window.thinkingInterval);
        window.thinkingInterval = null;
    }
    
    const thinkingIndicator = document.getElementById('thinking-indicator');
    if (thinkingIndicator) {
        thinkingIndicator.remove();
    }
}
