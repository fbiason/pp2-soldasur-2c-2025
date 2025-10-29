/* Configuración Ollama */
const OLLAMA_URL = 'http://localhost:11434/api/chat';
const OLLAMA_MODEL = 'llama3.2:3b';
const conversationHistory = [];
const MAX_HISTORY_LENGTH = 10; // Mantener últimos 10 mensajes para no saturar el contexto
let conversationContext = ''; // Resumen del contexto de la conversación
let waitingForCity = false; // Estado para saber si estamos esperando que el usuario elija ciudad
let selectedProductForConsult = null; // Producto elegido para consulta comercial
let peisaProductsFromJSON = []; // Catálogo cargado desde JSON

/* Cargar catálogo desde JSON */
async function loadProductCatalog() {
    try {
        // Ruta relativa desde app/soldasur2025.html hacia data/products_catalog.json
        const response = await fetch('../data/products_catalog.json');
        if (!response.ok) throw new Error('Error cargando catálogo');
        peisaProductsFromJSON = await response.json();
        console.log(`✅ Catálogo cargado: ${peisaProductsFromJSON.length} productos con información completa`);
    } catch (error) {
        console.error('❌ Error cargando catálogo:', error);
        console.error('   Asegurate de que el archivo data/products_catalog.json existe');
        console.error('   Ejecutá: python app/modules/scraping/product_scraper.py');
        peisaProductsFromJSON = [];
    }
}

// Cargar catálogo al iniciar
loadProductCatalog();

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
    
    // Mensaje contextual si viene de "Consultar producto"
    if (selectedProductForConsult) {
        appendMessage('system', `Consulta por ${selectedProductForConsult.model}: ¿Querés que te contacten? Acá están nuestros datos según tu ciudad:`);
    } else {
        appendMessage('system', '¡Perfecto! Acá están nuestros datos de contacto:');
    }
    
    const chatContainer = document.getElementById('chat-container');
    const contactDiv = document.createElement('div');
    contactDiv.className = 'fade-in mt-2';
    contactDiv.innerHTML = contactHTML;
    chatContainer.appendChild(contactDiv);
    scrollToBottom();
    // Resetear producto seleccionado después de mostrar contactos
    selectedProductForConsult = null;
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
        
        // Interceptar consultas de precio/costo y derivar a ventas
        if (isPriceQuestion(question)) {
            waitingForCity = true;
            appendMessage('system', 'Para precios y compras, ¿estás en Río Grande o Ushuaia?');
            // Botones rápidos
            const chatContainer = document.getElementById('chat-container');
            const div = document.createElement('div');
            div.className = 'fade-in mt-2 flex gap-2';
            const btnRG = document.createElement('button');
            btnRG.className = 'text-xs px-3 py-1 bg-blue-100 hover:bg-blue-200 text-blue-800 rounded';
            btnRG.textContent = 'Río Grande';
            btnRG.onclick = () => { showContactInfo('riogrande'); waitingForCity = false; showChatInput(); };
            const btnUsh = document.createElement('button');
            btnUsh.className = 'text-xs px-3 py-1 bg-green-100 hover:bg-green-200 text-green-800 rounded';
            btnUsh.textContent = 'Ushuaia';
            btnUsh.onclick = () => { showContactInfo('ushuaia'); waitingForCity = false; showChatInput(); };
            div.appendChild(btnRG); div.appendChild(btnUsh);
            chatContainer.appendChild(div);
            scrollToBottom();
            return;
        }
        
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
            
            // Enriquecer el mensaje con enlaces a productos mencionados
            const enrichedMessage = enrichMessageWithLinks(response.message);
            appendMessage('system', enrichedMessage);
            
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
    // Usar el catálogo JSON actualizado (con descripciones completas, ventajas y características)
    const catalogToUse = peisaProductsFromJSON;
    
    // Verificar que el catálogo esté cargado
    if (!catalogToUse || catalogToUse.length === 0) {
        console.error('⚠️ Catálogo vacío - no se pueden recomendar productos');
        return 'Disculpá, estoy teniendo problemas para acceder al catálogo. Por favor, recargá la página.';
    }
    
    // Crear versión simplificada del catálogo para el prompt (solo info clave + URL)
    const simplifiedCatalog = catalogToUse.map(p => ({
        model: p.model,
        family: p.family,
        category: p.category,
        description: p.description?.substring(0, 150) || '', // Limitar descripción
        advantages: p.advantages?.slice(0, 2) || [], // Solo primeras 2 ventajas
        url: p.url // IMPORTANTE: incluir URL
    }));
    
    // Crear el contexto del sistema con información de productos
    let systemPrompt = `Eres Soldy, asesor de ventas experto de SOLDASUR (vendemos productos marca PEISA). Tu misión es VENDER recomendando LA MEJOR SOLUCIÓN del catálogo según la necesidad del cliente.

CATÁLOGO COMPLETO (${catalogToUse.length} productos con descripciones, ventajas y características):
${JSON.stringify(simplifiedCatalog, null, 2)}

REGLAS DE ORO:
1. ANALIZA la necesidad del cliente (frío, calefacción, agua caliente, espacio, etc.)
2. RECOMIENDA el producto MÁS ADECUADO del catálogo por nombre completo
3. MENCIONA 1 producto por defecto; hasta 3 SOLO si piden "opciones", "alternativas" o "varios"
4. EXPLICA por qué ese producto es ideal para su necesidad específica
5. USA información real del catálogo (descripción, ventajas)
6. Respuestas: 2-3 oraciones (30-40 palabras)
7. Español argentino (vos/podés)
8. NUNCA precios - si preguntan: "Para precios, ¿estás en Río Grande o Ushuaia?"

FORMATO DE RESPUESTA:
"[Comprensión de necesidad]. Te recomiendo [Producto] – [por qué es ideal para su caso]."

EJEMPLOS POR NECESIDAD:

Usuario: "Tengo frío"
Soldy: "Para calentarte rápido, te recomiendo el Radiador Broen E – control digital y calor inmediato para tu ambiente."

Usuario: "Necesito calefacción para toda la casa"
Soldy: "Para toda la casa, la Prima Tec Smart es ideal – calefacción y agua caliente con 90% eficiencia y control wifi."

Usuario: "¿Qué opciones tengo para calefacción?" (PIDE OPCIONES)
Soldy: "Tenés 3 opciones: Prima Tec Smart (caldera wifi), Radiador Broen E (control digital) o Caldera Diva 24 (doble servicio)."

Usuario: "Necesito agua caliente"
Soldy: "Para agua caliente, el Termotanque Peisa es perfecto – recuperación rápida y bajo consumo."

Usuario: "Departamento chico"
Soldy: "Para espacios chicos, el Radiador Broen E es ideal – compacto, eficiente y control preciso."

IMPORTANTE:
- Branding: PEISA = marca, SOLDASUR = empresa
- SIEMPRE usa productos REALES del catálogo
- ADAPTA la recomendación a la necesidad específica
- NO inventes productos ni características`;

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
                num_predict: 150,  // Suficiente para respuestas completas con 1-2 productos
                top_p: 0.9,
                top_k: 40
            }
        })
    });
    
    if (!response.ok) {
        throw new Error('Error en la API de Ollama');
    }
    
    const data = await response.json();
            const assistantMessage = fixBranding(briefenResponse(data.message.content));
    
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

/* Forzar brevedad y foco producto-only en el mensaje */
function briefenResponse(text) {
    if (!text) return '';
    
    // Unificar espacios y líneas
    let t = text.replace(/\s+/g, ' ').trim();
    
    // Permitir hasta 50 palabras para respuestas con productos
    const words = t.split(' ');
    const maxWords = 50;
    
    if (words.length > maxWords) {
        // Buscar el segundo o tercer punto para permitir 2-3 oraciones
        const sentences = t.split(/[.!?]+/).filter(s => s.trim().length > 0);
        
        if (sentences.length >= 2) {
            // Tomar las primeras 2-3 oraciones
            t = sentences.slice(0, 3).join('. ') + '.';
        } else {
            // Si no hay puntos, cortar en maxWords
            t = words.slice(0, maxWords).join(' ');
            if (!/[\.!?]$/.test(t)) t += '.';
        }
    } else {
        // Agregar punto final si no lo tiene
        if (!/[\.!?]$/.test(t)) t += '.';
    }
    
    return t;
}

/* Corregir branding: PEISA es marca; la empresa es Soldasur */
function fixBranding(text) {
    if (!text) return '';
    let t = text;
    // Cambios directos de frases típicas
    t = t.replace(/visita a\s+peisa/gi, 'visita a Soldasur');
    t = t.replace(/en\s+peisa\b/gi, 'en Soldasur');
    t = t.replace(/(sucursales?|local|tienda|showroom|empresa|oficina|contacto)s?\s+de\s+peisa/gi, '$1 de Soldasur');
    t = t.replace(/empresa\s+peisa/gi, 'empresa Soldasur');
    // Evitar tocar menciones válidas de productos/catálogo PEISA
    return t;
}

/* Detectar consultas de precio/costo */
function isPriceQuestion(text) {
    if (!text) return false;
    const t = text.toLowerCase();
    const keywords = [
        'precio', 'precios', 'costo', 'costos', 'presupuesto', 'cuesta', 'vale', 'sale',
        'descuento', 'promoción', 'promocion', 'oferta', 'cuotas', 'financiación', 'financiacion'
    ];
    const currencyRegex = /(ar\$|u\$s|us\$|usd|eur|€|\$)\s*\d{1,3}(?:[\.,]\d{3})*(?:[\.,]\d{2})?/i;
    return keywords.some(k => t.includes(k)) || currencyRegex.test(text);
}

/* Consultar por un producto sugerido (se llama desde productCatalog.js) */
function consultProduct(product) {
    try {
        selectedProductForConsult = product || null;
        waitingForCity = true;
        appendMessage('system', `¿Querés consultar por ${product?.model || 'este producto'}? Elegí tu ciudad:`);
        // Botones rápidos locales (no usan handleOptionClick)
        const chatContainer = document.getElementById('chat-container');
        const div = document.createElement('div');
        div.className = 'fade-in mt-2 flex gap-2';
        const btnRG = document.createElement('button');
        btnRG.className = 'text-xs px-3 py-1 bg-blue-100 hover:bg-blue-200 text-blue-800 rounded';
        btnRG.textContent = 'Río Grande';
        btnRG.onclick = () => { showContactInfo('riogrande'); waitingForCity = false; showChatInput(); };
        const btnUsh = document.createElement('button');
        btnUsh.className = 'text-xs px-3 py-1 bg-green-100 hover:bg-green-200 text-green-800 rounded';
        btnUsh.textContent = 'Ushuaia';
        btnUsh.onclick = () => { showContactInfo('ushuaia'); waitingForCity = false; showChatInput(); };
        div.appendChild(btnRG); div.appendChild(btnUsh);
        chatContainer.appendChild(div);
        scrollToBottom();
    } catch (e) {
        console.error('Error iniciando consulta de producto', e);
    }
}

/* Actualizar contexto de conversación */
function updateConversationContext() {
    // Usar el catálogo JSON actualizado
    const catalogToUse = peisaProductsFromJSON;
    
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
            catalogToUse.forEach(product => {
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
    // Usar el catálogo JSON actualizado
    const catalogToUse = peisaProductsFromJSON;
    
    const mentioned = [];
    const messageLower = message.toLowerCase();
    
    for (const product of catalogToUse) {
        const modelLower = product.model.toLowerCase();
        if (messageLower.includes(modelLower)) {
            mentioned.push(product);
        }
    }
    
    // Si no se mencionan productos específicos pero se habla de categorías
    if (mentioned.length === 0) {
        if (messageLower.includes('caldera') || messageLower.includes('calderas')) {
            return catalogToUse.filter(p => p.family === 'Calderas').slice(0, 3);
        } else if (messageLower.includes('radiador') || messageLower.includes('radiadores')) {
            return catalogToUse.filter(p => p.family === 'Radiadores').slice(0, 3);
        } else if (messageLower.includes('toallero') || messageLower.includes('toalleros')) {
            return catalogToUse.filter(p => p.family === 'Radiadores' && p.type?.toLowerCase().includes('toallero')).slice(0, 3);
        } else if (messageLower.includes('termotanque') || messageLower.includes('termotanques')) {
            return catalogToUse.filter(p => p.family === 'Termotanques').slice(0, 3);
        } else if (messageLower.includes('calefón') || messageLower.includes('calefones')) {
            return catalogToUse.filter(p => p.family === 'Calefones').slice(0, 3);
        }
    }
    
    return mentioned.slice(0, 5); // Limitar a 5 productos
}

/* Enriquecer mensaje con enlaces a productos mencionados */
function enrichMessageWithLinks(message) {
    if (!peisaProductsFromJSON || peisaProductsFromJSON.length === 0) {
        return message;
    }
    
    let enrichedMessage = message;
    const replacedProducts = new Set(); // Evitar reemplazos duplicados
    
    // Ordenar productos por longitud de nombre (más largos primero) para evitar reemplazos parciales
    const sortedProducts = [...peisaProductsFromJSON].sort((a, b) => b.model.length - a.model.length);
    
    // Buscar productos mencionados y reemplazar con enlaces
    for (const product of sortedProducts) {
        // Escapar caracteres especiales en el nombre del producto para regex
        const escapedModel = product.model.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        
        // Buscar el nombre del producto en el mensaje (case insensitive, palabra completa)
        const regex = new RegExp(`\\b(${escapedModel})\\b`, 'gi');
        
        if (regex.test(enrichedMessage) && !replacedProducts.has(product.model.toLowerCase())) {
            // Reemplazar con enlace HTML
            enrichedMessage = enrichedMessage.replace(regex, 
                `<a href="${product.url}" target="_blank" class="product-link" title="Ver ${product.model} en PEISA">$1</a>`
            );
            replacedProducts.add(product.model.toLowerCase());
        }
    }
    
    return enrichedMessage;
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
