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

/* Renderizar productos */
function renderProducts(products) {
    console.log('renderProducts llamado con:', products.length, 'productos');
    const container = document.createElement('div');
    container.className = 'mt-3 space-y-2';
    
    const productsToShow = products.slice(0, 10);
    console.log('Mostrando', productsToShow.length, 'productos');
    
    productsToShow.forEach((product, index) => {
        const card = document.createElement('div');
        card.className = 'product-card fade-in';
        card.style.animationDelay = `${index * 0.05}s`;
        card.innerHTML = `
            <div class="flex justify-between items-start gap-2">
                <div class="flex-1 cursor-pointer js-open-link">
                    <div class="font-semibold text-blue-800">${product.model || 'N/A'}</div>
                    <div class="text-sm text-gray-600">
                        <span class="inline-block px-2 py-0.5 bg-blue-50 rounded text-xs mr-1">${product.family || ''}</span>
                        ${product.category ? `<span class="text-xs">${product.category}</span>` : ''}
                    </div>
                    ${product.description ? `<div class="text-xs text-gray-500 mt-1">${product.description}</div>` : ''}
                </div>
                <div class="ml-2 flex-shrink-0 flex flex-col items-end gap-1">
                    <button class="text-xs px-2 py-1 bg-blue-600 text-white rounded hover:bg-blue-700 js-consult">Consultar</button>
                </div>
            </div>
        `;

        // Abrir ficha
        card.querySelector('.js-open, .js-open-link').addEventListener('click', (e) => {
            e.stopPropagation();
            window.open(product.url, '_blank');
        });

        // Consultar producto
        card.querySelector('.js-consult').addEventListener('click', (e) => {
            e.stopPropagation();
            if (typeof consultProduct === 'function') {
                consultProduct(product);
            } else {
                alert('Para consultar por este producto, indicá tu ciudad: Río Grande o Ushuaia.');
            }
        });

        container.appendChild(card);
    });
    
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

/* Navegación por categorías */
function showProductsByCategory(category) {
    const categoryProducts = peisaProducts.filter(p => p.family === category);
    console.log('Categoría seleccionada:', category);
    console.log('Productos encontrados:', categoryProducts.length, categoryProducts);

    if (categoryProducts.length > 0) {
        appendMessage('system', `📦 Aquí están nuestros <strong>${categoryProducts.length} productos de ${category}</strong>:`);
        setTimeout(() => {
            renderProducts(categoryProducts);
            appendMessage('system', `💡 <em>Haz clic en cualquier producto para ver más detalles en nuestra web.</em>`);
            renderOptions(['🤖 Hacer un cálculo', '💬 Hacer una pregunta', '📦 Ver otras categorías'], false);
        }, 500);
    } else {
        appendMessage('system', `Lo siento, no encontré productos en la categoría ${category}. ¿Te gustaría ver otra categoría?`);
        renderOptions(['📦 Ver otras categorías', '🤖 Hacer un cálculo', '💬 Hacer una pregunta'], false);
    }
}

/* Mostrar todos los productos destacados */
function showAllProducts() {
    appendMessage('system', '📦 Aquí está una selección de nuestros <strong>productos destacados</strong>:');
    setTimeout(() => {
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
}

/* Mostrar menú de categorías */
function showCategoryMenu() {
    appendMessage('system', '📦 ¿Qué tipo de producto te interesa?');
    renderOptions(['Calderas', 'Radiadores', 'Termotanques', 'Calefones', 'Toalleros', 'Climatizadores', 'Ver todos'], false);
}
