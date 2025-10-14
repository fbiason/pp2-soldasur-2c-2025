/* Estado Global */
        let conversationId = 'user_' + Math.random().toString(36).substr(2, 9);
        let lastUserResponse = null;
        let isLoading = false;
        let currentMode = 'hybrid';
        let contextData = {};
        let conversationStep = 0;
        let userInputs = {};
        let inMainMenu = true;
        
        /* Configuración OpenAI */
        const OPENAI_API_KEY = '';
        const conversationHistory = [];
        
        /* Catálogo de productos PEISA */
        const peisaProducts = [
            // Calderas hogareñas
            { model: "Prima Tec Smart", family: "Calderas", category: "Caldera Mural", description: "Caldera doble servicio", url: "https://peisa.com.ar/productos/prima-tec-smart" },
            { model: "Prima Tec", family: "Calderas", category: "Caldera Mural", description: "Caldera para calefacción y agua caliente", url: "https://peisa.com.ar/productos/prima-tec1" },
            { model: "Diva Tecno", family: "Calderas", category: "Caldera mural", description: "Caldera para calefacción y agua caliente", url: "https://peisa.com.ar/productos/caldera-Diva-tecno" },
            { model: "Diva DS", family: "Calderas", category: "Caldera mural", description: "Caldera para calefacción y agua caliente", url: "https://peisa.com.ar/productos/diva-ds" },
            { model: "Summa Condens", family: "Calderas", category: "Caldera mural", description: "Caldera de condensación para calefacción y agua caliente", url: "https://peisa.com.ar/productos/summa-condens" },
            { model: "Diva C", family: "Calderas", category: "Caldera mural", description: "Caldera para Calefacción", url: "https://peisa.com.ar/productos/diva-c" },
            { model: "CM", family: "Calderas", category: "Caldera Mural Eléctrica", description: "Caldera eléctrica para calefacción", url: "https://peisa.com.ar/productos/caldera_electrica_CM" },
            
            // Calderas centrales
            { model: "Optima Condens", family: "Calderas", category: "Caldera de potencia", description: "Caldera de condensación para calefacción y agua caliente", url: "https://peisa.com.ar/productos/optima-condens" },
            { model: "Magna", family: "Calderas", category: "Caldera de potencia", description: "Caldera para calefacción y agua caliente", url: "https://peisa.com.ar/productos/magna" },
            { model: "Modal & Ellprex", family: "Calderas", category: "Caldera de potencia", description: "Caldera para calefacción y agua caliente", url: "https://peisa.com.ar/productos/modal-ellprex" },
            { model: "XP", family: "Calderas", category: "Caldera de potencia", description: "Caldera para calefacción y agua caliente", url: "https://peisa.com.ar/productos/Potencia_XP" },
            
            // Radiadores
            { model: "BR 500", family: "Radiadores", category: "Radiadores", description: "Radiador para calefacción por agua", url: "https://peisa.com.ar/productos/br" },
            { model: "Broen", family: "Radiadores", category: "Radiadores", description: "Radiador para calefacción por agua", url: "https://peisa.com.ar/productos/broen" },
            { model: "Broen Plus", family: "Radiadores", category: "Radiadores", description: "Radiador para calefacción por agua", url: "https://peisa.com.ar/productos/broen-plus" },
            { model: "Tropical", family: "Radiadores", category: "Radiadores", description: "Radiador para calefacción por agua", url: "https://peisa.com.ar/productos/tropical" },
            { model: "Gamma", family: "Radiadores", category: "Radiadores", description: "Radiador para calefacción por agua", url: "https://peisa.com.ar/productos/radiador-gamma" },
            { model: "Radiador Eléctrico Broen E Smart con Wifi", family: "Radiadores", category: "Radiadores Eléctricos", description: "Radiador eléctrico para calefacción con WiFi", url: "https://peisa.com.ar/productos/smart-broen-e" },
            { model: "L500-E", family: "Radiadores", category: "Radiadores Eléctricos", description: "Radiador eléctrico para calefacción", url: "https://peisa.com.ar/productos/l500-e" },
            { model: "Radiador Eléctrico Broen E", family: "Radiadores", category: "Radiadores Eléctricos", description: "Radiador eléctrico para calefacción", url: "https://peisa.com.ar/productos/broen-e" },
            
            // Toalleros
            { model: "Domino", family: "Toalleros", category: "Toallero", description: "Toallero para calefacción por agua", url: "https://peisa.com.ar/productos/Toallero_Domino" },
            { model: "Scala", family: "Toalleros", category: "Toallero", description: "Toallero para calefacción por agua", url: "https://peisa.com.ar/productos/scala" },
            { model: "Scala S", family: "Toalleros", category: "Toallero Eléctrico", description: "Toallero eléctrico para calefacción", url: "https://peisa.com.ar/productos/Scala_s" },
            { model: "Scala E", family: "Toalleros", category: "Toallero Eléctrico", description: "Toallero eléctrico para calefacción", url: "https://peisa.com.ar/productos/scala%20E" },
            { model: "Domino D", family: "Toalleros", category: "Toallero Eléctrico", description: "Toallero eléctrico para calefacción", url: "https://peisa.com.ar/productos/toallero_domino_d_electrico" },
            { model: "Domino S", family: "Toalleros", category: "Toallero Eléctrico", description: "Toallero eléctrico para calefacción", url: "https://peisa.com.ar/productos/toallero_domino_s_electrico" },
            
            // Termostatos
            { model: "Termostato wifi Zentraly", family: "Termostatos", category: "Accesorios", description: "Asistente inteligente para la calefacción", url: "https://peisa.com.ar/productos/Termostato_wifi_zentraly" },
            { model: "Termostato Digital / Inalámbrico", family: "Termostatos", category: "Accesorios", description: "Control de calefacción residencial y comercial", url: "https://peisa.com.ar/productos/termostato-de-ambiente-digital-programable-inalambrico" },
            
            // Calefones
            { model: "Digital 14 TBF", family: "Calefones", category: "Agua caliente sanitaria", description: "Calefón a gas, compacto, sin llama piloto", url: "https://peisa.com.ar/productos/calefon-14-tbf" },
            { model: "Acqua", family: "Calefones", category: "Agua caliente sanitaria", description: "Calefón a gas, sin llama piloto", url: "https://peisa.com.ar/productos/calefon-acqua" },
            
            // Termotanques
            { model: "Termotanque Eléctrico Digital", family: "Termotanques", category: "Termotanque", description: "Termotanque eléctrico", url: "https://peisa.com.ar/productos/termotanque-electrico-digital" },
            { model: "Termotanque Eléctrico Analógico", family: "Termotanques", category: "Termotanque", description: "Termotanque eléctrico", url: "https://peisa.com.ar/productos/termotanque-electrico" },
            { model: "Termotanque solar presurizado", family: "Termotanques", category: "Termotanque", description: "Placa plana", url: "https://peisa.com.ar/productos/termotanque-solar" },
            
            // Climatizadores de piscina
            { model: "Bomba de calor Inverter con Wifi", family: "Climatizadores", category: "Climatizador de piscina", description: "Para uso residencial", url: "https://peisa.com.ar/productos/Bomba_de_calor" },
            { model: "TX70", family: "Climatizadores", category: "Climatizador de piscinas a gas", description: "Un modelo para cada tipo de pileta", url: "https://peisa.com.ar/productos/tx70" },
            { model: "TX40", family: "Climatizadores", category: "Climatizador de piscinas a gas", description: "Fácil instalación. Larga vida útil.", url: "https://peisa.com.ar/productos/tx40" }
        ];

        /* Toggle del chat flotante */
        let chatIsOpen = false;
        
        function toggleChat() {
            const chatWidget = document.getElementById('chat-widget');
            const chatButton = document.getElementById('chat-toggle-btn');
            const soldyMessage = document.getElementById('soldy-message');
            const soldyChatImage = document.getElementById('soldy-chat-image');
            
            chatIsOpen = !chatIsOpen;
            
            if (chatIsOpen) {
                chatWidget.classList.add('active');
                chatButton.style.display = 'none';
                // Mostrar imagen de Soldy al abrir el chat
                if (soldyChatImage) {
                    soldyChatImage.style.display = 'block';
                }
                // Ocultar mensaje de bienvenida al abrir
                if (soldyMessage) {
                    soldyMessage.classList.add('hidden');
                }
                // Iniciar conversación si es la primera vez
                if (document.getElementById('chat-container').children.length === 0) {
                    startConversation();
                }
            } else {
                chatWidget.classList.remove('active');
                chatButton.style.display = 'block';
                // Ocultar imagen de Soldy al cerrar el chat
                if (soldyChatImage) {
                    soldyChatImage.style.display = 'none';
                }
                // Mostrar mensaje de bienvenida al cerrar
                if (soldyMessage) {
                    soldyMessage.classList.remove('hidden');
                }
            }
        }
        
        /* Ocultar mensaje después de un tiempo */
        document.addEventListener('DOMContentLoaded', () => {
            setTimeout(() => {
                const soldyMessage = document.getElementById('soldy-message');
                if (soldyMessage && !chatIsOpen) {
                    soldyMessage.style.animation = 'fadeOut 0.5s ease-out forwards';
                    setTimeout(() => {
                        soldyMessage.style.display = 'none';
                    }, 500);
                }
            }, 8000); // Ocultar después de 8 segundos
        });

        /* Login - Inicio automático sin autenticación */
        document.addEventListener('DOMContentLoaded', () => {
            // No iniciar conversación automáticamente, esperar a que se abra el chat
            
            // Mantener el código de login por si se necesita en el futuro
            const loginForm = document.getElementById('login-form');
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
        });

        /* Mostrar/Ocultar botón de volver */
        function showBackButton() {
            document.getElementById('back-button').classList.remove('hidden');
            inMainMenu = false;
        }
        
        function hideBackButton() {
            document.getElementById('back-button').classList.add('hidden');
            inMainMenu = true;
        }
        
        /* Función para volver al menú principal */
        function goBack() {
            // Limpiar el estado
            conversationStep = 0;
            userInputs = {};
            contextData = {};
            updateContextPanel();
            
            // Limpiar el chat
            document.getElementById('chat-container').innerHTML = '';
            
            // Volver al menú principal
            startConversation();
            hideBackButton();
        }

        /* Cambio de modo */
        function switchMode(mode) {
            currentMode = mode;
            conversationId = 'user_' + Math.random().toString(36).substr(2, 9);
            document.getElementById('chat-container').innerHTML = '';
            lastUserResponse = null;
            contextData = {};
            updateContextPanel();
            
            // Limpiar el chat
            document.getElementById('chat-container').innerHTML = '';
            
            // Volver al menú principal
            startConversation();
            hideBackButton();
        }
        
        /* Iniciar conversación - VERSIÓN STANDALONE */
        function startConversation() {
            conversationStep = 0;
            userInputs = {};
            
            // Modo híbrido fijo - siempre muestra las opciones iniciales
            appendMessage('system', '¡Hola! Soy <strong>Soldy</strong> tu asistente inteligente de SOLDASUR. Puedo ayudarte de diferentes formas. ¿Qué necesitas?');
            renderOptions([' Guíame en un cálculo', ' Tengo una pregunta', ' Buscar productos'], false);
        }
        
        /* Preguntar siguiente paso */
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
                // Cálculo final
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
                    // Filtrar productos según el tipo seleccionado
                    let recommendedProducts = [];
                    if (tipo.toLowerCase().includes('radiador')) {
                        recommendedProducts = peisaProducts.filter(p => p.family === 'Radiadores');
                    } else if (tipo.toLowerCase().includes('caldera')) {
                        recommendedProducts = peisaProducts.filter(p => p.family === 'Calderas');
                    } else if (tipo.toLowerCase().includes('piso')) {
                        // Para piso radiante, recomendar calderas y accesorios
                        recommendedProducts = peisaProducts.filter(p => 
                            p.family === 'Calderas' || p.model.toLowerCase().includes('piso')
                        );
                    }
                    
                    // Si no hay productos específicos, mostrar una mezcla
                    if (recommendedProducts.length === 0) {
                        recommendedProducts = [...peisaProducts.filter(p => p.family === 'Calderas').slice(0, 2),
                                              ...peisaProducts.filter(p => p.family === 'Radiadores').slice(0, 2)];
                    }
                    
                    renderProducts(recommendedProducts.slice(0, 5));
                    renderOptions(['Nuevo cálculo', 'Hacer una pregunta'], false);
                }, 500);
            }
        }

        /* Actualizar indicador de modo */
        function updateModeIndicator(mode, label) {
            const indicator = document.getElementById('mode-indicator');
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

        /* Renderizar productos */
        function renderProducts(products) {
            console.log('renderProducts llamado con:', products.length, 'productos');
            const container = document.createElement('div');
            container.className = 'mt-3 space-y-2';
            
            const productsToShow = products.slice(0, 10); // Mostrar hasta 10 productos
            console.log('Mostrando', productsToShow.length, 'productos');
            
            productsToShow.forEach((product, index) => {
                const card = document.createElement('div');
                card.className = 'product-card fade-in cursor-pointer';
                card.style.animationDelay = `${index * 0.05}s`;
                card.onclick = () => window.open(product.url, '_blank');
                card.innerHTML = `
                    <div class="flex justify-between items-start">
                        <div class="flex-1">
                            <div class="font-semibold text-blue-800">${product.model || 'N/A'}</div>
                            <div class="text-sm text-gray-600">
                                <span class="inline-block px-2 py-0.5 bg-blue-50 rounded text-xs mr-1">${product.family || ''}</span>
                                ${product.category ? `<span class="text-xs">${product.category}</span>` : ''}
                            </div>
                            ${product.description ? `<div class="text-xs text-gray-500 mt-1">${product.description}</div>` : ''}
                        </div>
                        <div class="ml-2 flex-shrink-0">
                            <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path>
                            </svg>
                        </div>
                    </div>
                `;
                container.appendChild(card);
            });
            
            // Agregar contador si hay más productos
            if (products.length > productsToShow.length) {
                const moreInfo = document.createElement('div');
                moreInfo.className = 'text-center text-sm text-gray-500 mt-2';
                moreInfo.innerHTML = `<em>Mostrando ${productsToShow.length} de ${products.length} productos</em>`;
                container.appendChild(moreInfo);
            }
            
            const chatContainer = document.getElementById('chat-container');
            console.log('Agregando productos al contenedor:', chatContainer);
            chatContainer.appendChild(container);
            scrollToBottom();
        }

        /* Renderizar sugerencia */
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

        /* Renderizar opciones */
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
        
        /* Manejar click en opción */
        function handleOptionClick(option) {
            appendMessage('user', option);
            
            // Manejar selección de categorías de productos PRIMERO (antes de verificar conversationStep)
            if (['Calderas', 'Radiadores', 'Termotanques', 'Calefones', 'Toalleros', 'Climatizadores', 'Termostatos'].includes(option)) {
                console.log('Categoría seleccionada:', option);
                const categoryProducts = peisaProducts.filter(p => p.family === option);
                console.log('Productos encontrados:', categoryProducts.length, categoryProducts);
                
                if (categoryProducts.length > 0) {
                    appendMessage('system', `📦 Aquí están nuestros <strong>${categoryProducts.length} productos de ${option}</strong>:`);
                    setTimeout(() => {
                        renderProducts(categoryProducts);
                        appendMessage('system', `💡 <em>Haz clic en cualquier producto para ver más detalles en nuestra web.</em>`);
                        renderOptions(['🤖 Hacer un cálculo', '💬 Hacer una pregunta', '📦 Ver otras categorías'], false);
                    }, 500);
                } else {
                    appendMessage('system', `Lo siento, no encontré productos en la categoría ${option}. ¿Te gustaría ver otra categoría?`);
                    renderOptions(['📦 Ver otras categorías', '🤖 Hacer un cálculo', '💬 Hacer una pregunta'], false);
                }
                return;
            }
            
            // Opciones de "Ver todos" y navegación de categorías
            if (option === 'Ver todos') {
                appendMessage('system', '📦 Aquí está una selección de nuestros <strong>productos destacados</strong>:');
                setTimeout(() => {
                    // Mostrar una mezcla de productos
                    const featured = [
                        ...peisaProducts.filter(p => p.family === 'Calderas').slice(0, 2),
                        ...peisaProducts.filter(p => p.family === 'Radiadores').slice(0, 2),
                        ...peisaProducts.filter(p => p.family === 'Termotanques').slice(0, 1),
                        ...peisaProducts.filter(p => p.family === 'Climatizadores').slice(0, 1)
                    ];
                    renderProducts(featured);
                    appendMessage('system', `💡 <em>Tenemos ${peisaProducts.length} productos en total. Haz clic en cualquiera para ver más detalles.</em>`);
                    renderOptions(['🤖 Hacer un cálculo', '💬 Hacer una pregunta', '📦 Ver por categoría'], false);
                }, 500);
                return;
            } else if (option === '📦 Ver otras categorías' || option === '📦 Ver por categoría') {
                appendMessage('system', '📦 ¿Qué tipo de producto te interesa?');
                renderOptions(['Calderas', 'Radiadores', 'Termotanques', 'Calefones', 'Toalleros', 'Climatizadores', 'Ver todos'], false);
                return;
            }
            
            // Opciones iniciales del modo híbrido
            if (conversationStep === 0) {
                if (option.includes('Guíame') || option.includes('cálculo')) {
                    // Iniciar flujo experto
                    showBackButton(); // Mostrar botón de volver
                    appendMessage('system', '¡Perfecto! Te guiaré paso a paso para calcular tu sistema de calefacción.');
                    setTimeout(() => askQuestion(), 500);
                } else if (option.includes('pregunta')) {
                    // Abrir chat libre
                    showBackButton(); // Mostrar botón de volver
                    appendMessage('system', '¿Qué te gustaría saber sobre nuestros productos de calefacción?');
                    showChatInput();
                } else if (option.includes('Buscar') || option.includes('productos')) {
                    // Mostrar catálogo con categorías
                    showBackButton(); // Mostrar botón de volver
                    appendMessage('system', '📦 ¿Qué tipo de producto te interesa?');
                    renderOptions(['Calderas', 'Radiadores', 'Termotanques', 'Calefones', 'Toalleros', 'Climatizadores', 'Ver todos'], false);
                }
                return;
            }
            
            // Guardar respuesta según el paso del flujo experto
            if (conversationStep === 1) {
                userInputs.tipo = option;
                contextData.tipo = option;
            } else if (conversationStep === 3) {
                userInputs.zona = option;
            } else if (conversationStep === 4) {
                userInputs.aislacion = option;
            }
            
            // Opciones finales después del cálculo
            if (option === 'Nuevo cálculo' || option.includes('Hacer un cálculo')) {
                conversationStep = 0;
                userInputs = {};
                contextData = {};
                updateContextPanel();
                appendMessage('system', '¡Perfecto! Iniciemos un nuevo cálculo.');
                setTimeout(() => askQuestion(), 500);
            } else if (option === 'Hacer una pregunta' || option.includes('pregunta')) {
                appendMessage('system', '¿Qué te gustaría saber?');
                showChatInput();
            } else {
                // Continuar con el flujo experto
                setTimeout(() => askQuestion(), 500);
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
        
        /* Manejar input de chat con OpenAI */
        async function handleChatInput() {
            const input = document.getElementById('chat-input');
            const question = input.value.trim();
            
            if (question) {
                appendMessage('user', question);
                input.value = '';
                showLoadingIndicator();
                
                try {
                    // Llamar a OpenAI
                    const response = await callOpenAI(question);
                    hideLoadingIndicator();
                    appendMessage('system', response.message);
                    
                    // Si OpenAI recomienda productos, mostrarlos
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
        
        /* Llamar a la API de OpenAI */
        async function callOpenAI(userMessage) {
            // Agregar mensaje del usuario al historial
            conversationHistory.push({
                role: 'user',
                content: userMessage
            });
            
            // Crear el contexto del sistema con información de productos
            const systemPrompt = `Eres un asistente experto en productos de calefacción de PEISA - SOLDASUR S.A. 
Tu objetivo es ayudar a los clientes a encontrar los productos adecuados para sus necesidades.

CATÁLOGO DE PRODUCTOS DISPONIBLES:
${JSON.stringify(peisaProducts, null, 2)}

INSTRUCCIONES:
1. Responde de manera amigable y profesional
2. Si el usuario pregunta por productos específicos (calderas, radiadores, termotanques, etc.), recomienda productos del catálogo
3. Si recomiendas productos, menciona sus nombres exactos y características
4. Proporciona información técnica cuando sea relevante
5. Si el usuario pregunta sobre instalación, mantenimiento o garantías, proporciona información general
6. Mantén las respuestas concisas pero informativas

FORMATO DE RESPUESTA:
- Responde en español de Argentina
- Usa un tono profesional pero cercano
- Si recomiendas productos, menciónalos claramente en tu respuesta`;

            const messages = [
                { role: 'system', content: systemPrompt },
                ...conversationHistory
            ];
            
            const response = await fetch('https://api.openai.com/v1/chat/completions', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${OPENAI_API_KEY}`
                },
                body: JSON.stringify({
                    model: 'gpt-4',
                    messages: messages,
                    temperature: 0.7,
                    max_tokens: 500
                })
            });
            
            if (!response.ok) {
                throw new Error('Error en la API de OpenAI');
            }
            
            const data = await response.json();
            const assistantMessage = data.choices[0].message.content;
            
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

        /* Crear múltiples inputs */
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
                sendReply({ input_values: values });
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

        /* Crear botón de reinicio */
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

        /* Helpers */
        function showLoadingIndicator() {
            document.getElementById('input-area').innerHTML = 
                '<div class="text-center py-2"><div class="loading-spinner inline-block"></div></div>';
        }

        function hideLoadingIndicator() {}

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