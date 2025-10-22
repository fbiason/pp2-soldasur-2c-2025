/* ============================================
   CHATBOT - INTEGRACIÓN CON OLLAMA
   ============================================ */

/* Configuración Ollama */
const OLLAMA_URL = 'http://localhost:11434/api/chat';
const OLLAMA_MODEL = 'llama3.2:3b';
const conversationHistory = [];
const MAX_HISTORY_LENGTH = 10; // Mantener últimos 10 mensajes para no saturar el contexto
let conversationContext = ''; // Resumen del contexto de la conversación
let waitingForCity = false; // Estado para saber si estamos esperando que el usuario elija ciudad

/* Iniciar modo chatbot */
function startChatbot() {
    if (conversationHistory.length > 0) {
        appendMessage('system', '¡Continuemos! ¿Qué más necesitas saber?');
    } else {
        appendMessage('system', '¿Qué necesitas saber?');
    }
    showChatInput();
}

/* Resetear historial de conversación */
function resetChatHistory() {
    conversationHistory.length = 0;
    conversationContext = '';
    waitingForCity = false;
}

/* Mostrar información de contacto según la ciudad */
function showContactInfo(city) {
    let contactHTML = '';
    
    if (city === 'riogrande') {
        contactHTML = `
            <div class="bg-blue-50 border-l-4 border-blue-600 p-4 rounded">
                <div class="font-bold text-blue-900 mb-2">📍 RÍO GRANDE</div>
                <div class="space-y-2 text-sm">
                    <div>
                        <strong>Sucursal 1:</strong><br>
                        Islas Malvinas 1950<br>
                        📞 Tel. 02964 422350<br>
                        ✉️ ventasrg@soldasur.com.ar
                    </div>
                    <div class="pt-2 border-t border-blue-200">
                        <strong>Sucursal 2:</strong><br>
                        Av. San Martín 366<br>
                        📞 Tel. 02964 422131
                    </div>
                </div>
            </div>
        `;
    } else if (city === 'ushuaia') {
        contactHTML = `
            <div class="bg-green-50 border-l-4 border-green-600 p-4 rounded">
                <div class="font-bold text-green-900 mb-2">📍 USHUAIA</div>
                <div class="space-y-2 text-sm">
                    <div>
                        <strong>Sucursal 1:</strong><br>
                        Héroes de Malvinas 4180<br>
                        📞 Tel. 02901 436392<br>
                        ✉️ ventasush@soldasur.com.ar
                    </div>
                    <div class="pt-2 border-t border-green-200">
                        <strong>Sucursal 2:</strong><br>
                        Gobernador Paz 665<br>
                        📞 Tel. 02901 430886
                    </div>
                </div>
            </div>
        `;
    }
    
    appendMessage('system', '¡Perfecto! Acá están nuestros datos de contacto:');
    
    const chatContainer = document.getElementById('chat-container');
    const contactDiv = document.createElement('div');
    contactDiv.className = 'fade-in mt-2';
    contactDiv.innerHTML = contactHTML;
    chatContainer.appendChild(contactDiv);
    scrollToBottom();
}

/* Mostrar input de chat */
function showChatInput() {
    const inputArea = document.getElementById('input-area');
    const showResetButton = conversationHistory.length > 2; // Mostrar después de 2 mensajes
    
    inputArea.innerHTML = `
        <div class="space-y-2">
            <div class="flex gap-2">
                <input type="text" id="chat-input" class="flex-1 border border-gray-300 rounded px-3 py-2" placeholder="Escribe tu pregunta...">
                <button onclick="handleChatInput()" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition">
                    Enviar
                </button>
            </div>
            ${showResetButton ? `
                <button onclick="handleResetConversation()" class="w-full text-xs text-gray-500 hover:text-gray-700 py-1">
                     Nueva conversación
                </button>
            ` : ''}
        </div>
    `;
    document.getElementById('chat-input').focus();
    document.getElementById('chat-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleChatInput();
    });
}

/* Manejar reset de conversación */
function handleResetConversation() {
    if (confirm('¿Deseas iniciar una nueva conversación? Se perderá el contexto actual.')) {
        resetChatHistory();
        document.getElementById('chat-container').innerHTML = '';
        startChatbot();
    }
}

/* Manejar input de chat */
async function handleChatInput() {
    const input = document.getElementById('chat-input');
    const question = input.value.trim();
    
    if (question) {
        appendMessage('user', question);
        input.value = '';
        
        // Detectar si el usuario está respondiendo con una ciudad
        if (waitingForCity && (question.toLowerCase().includes('río grande') || question.toLowerCase().includes('rio grande') || question.toLowerCase().includes('rg'))) {
            showContactInfo('riogrande');
            waitingForCity = false;
            showChatInput();
            return;
        } else if (waitingForCity && (question.toLowerCase().includes('ushuaia') || question.toLowerCase().includes('ush'))) {
            showContactInfo('ushuaia');
            waitingForCity = false;
            showChatInput();
            return;
        }
        
        showLoadingIndicator();
        
        try {
            const response = await callOllama(question);
            hideLoadingIndicator();
            appendMessage('system', response.message);
            
            // Detectar si la respuesta pregunta por la ciudad
            if (response.message.toLowerCase().includes('río grande o ushuaia') || 
                response.message.toLowerCase().includes('rio grande o ushuaia')) {
                waitingForCity = true;
            }
            
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
    let systemPrompt = `Eres Soldy, asesor de ventas de PEISA-SOLDASUR. Tu objetivo es ayudar con calidez y profesionalismo.

CATÁLOGO:
${JSON.stringify(peisaProducts, null, 2)}

REGLAS DE ORO:
1. ✅ Respuestas BREVES: Máximo 2-3 frases cortas (20-30 palabras total)
2. ✅ Tono CÁLIDO y HUMANO: Como un asesor real, empático y servicial
3. ✅ DIRECTO AL PUNTO: Sin rodeos ni explicaciones largas
4. ✅ Recomienda 1 producto específico por nombre cuando sea relevante
5. ✅ COHERENCIA: Recuerda lo que el cliente ya preguntó

🚫 NUNCA MENCIONES PRECIOS, COSTOS O MONTOS
Si preguntan por precio/compra/presupuesto, responde:
"Para precios y compras, ¿estás en Río Grande o Ushuaia?"

EJEMPLOS:
❌ MAL: "Para calentar tu hogar eficientemente, especialmente con un perro como Rufus que necesita un ambiente acogedor, te recomiendo considerar un sistema de calefacción completo..."
✅ BIEN: "Podés usar radiadores Broen, son eficientes y fáciles de mantener. Si querés saber precios, te paso el contacto según tu ciudad."

Español argentino, vos/podés, tono cercano.`;

    // Agregar contexto de conversación previa si existe
    if (conversationContext) {
        systemPrompt += `\n\nCONTEXTO DE LA CONVERSACIÓN:\n${conversationContext}`;
    }

    // Agregar mensaje del usuario al historial
    conversationHistory.push({
        role: 'user',
        content: userMessage
    });

    // Limitar el historial para no saturar el contexto
    if (conversationHistory.length > MAX_HISTORY_LENGTH) {
        // Guardar resumen del contexto antes de eliminar mensajes antiguos
        updateConversationContext();
        conversationHistory.splice(0, conversationHistory.length - MAX_HISTORY_LENGTH);
    }

    // Preparar mensajes para Ollama (incluir system prompt solo la primera vez)
    const messages = [
        { role: 'system', content: systemPrompt },
        ...conversationHistory
    ];
    
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
                num_predict: 80  // Respuestas breves y concisas (2-3 frases)
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

/* Actualizar contexto de conversación */
function updateConversationContext() {
    // Crear un resumen de los temas tratados en la conversación
    const topics = [];
    const mentionedProducts = new Set();
    
    conversationHistory.forEach(msg => {
        if (msg.role === 'user') {
            // Extraer temas clave de las preguntas del usuario
            const content = msg.content.toLowerCase();
            if (content.includes('caldera')) topics.push('calderas');
            if (content.includes('radiador')) topics.push('radiadores');
            if (content.includes('termotanque')) topics.push('termotanques');
            if (content.includes('calefón')) topics.push('calefones');
            if (content.includes('toallero')) topics.push('toalleros');
            if (content.includes('m²') || content.includes('metros')) topics.push('dimensiones');
            if (content.includes('precio') || content.includes('costo')) topics.push('precios');
        } else if (msg.role === 'assistant') {
            // Extraer productos mencionados por el asistente
            peisaProducts.forEach(product => {
                if (msg.content.toLowerCase().includes(product.model.toLowerCase())) {
                    mentionedProducts.add(product.model);
                }
            });
        }
    });
    
    // Construir resumen del contexto
    let contextSummary = '';
    if (topics.length > 0) {
        contextSummary += `Temas consultados: ${[...new Set(topics)].join(', ')}. `;
    }
    if (mentionedProducts.size > 0) {
        contextSummary += `Productos ya recomendados: ${[...mentionedProducts].join(', ')}.`;
    }
    
    conversationContext = contextSummary;
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
