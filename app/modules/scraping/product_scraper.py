# app/product_scraper.py - Scraper y catálogo de productos PEISA
import json
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import re
import time

def scrape_peisa_products() -> List[Dict]:
    """
    Realiza scraping REAL del sitio web de PEISA para obtener productos actualizados.
    URL: https://peisa.com.ar/productos
    
    Returns:
        Lista de productos extraídos del sitio web
    """
    print("🌐 Iniciando scraping de PEISA...")
    products = []
    
    try:
        # URL base de productos PEISA
        base_url = "https://peisa.com.ar"
        products_url = f"{base_url}/productos"
        
        # Headers para simular navegador
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        print(f"  📡 Conectando a {products_url}...")
        response = requests.get(products_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        print("  ✅ Página cargada correctamente")
        
        # Buscar productos en la página - PEISA usa <a> con <article> dentro
        # Estructura: <a href="/productos/[nombre]"><article>...</article></a>
        product_links = soup.find_all('a', href=re.compile(r'/productos/[^/]+$'))
        
        # Filtrar solo los que tienen article dentro (son productos reales)
        product_cards = [link for link in product_links if link.find('article')]
        
        print(f"  🔍 Encontrados {len(product_cards)} productos")
        
        for idx, card in enumerate(product_cards[:50], 1):  # Limitar a 50 productos
            try:
                # Extraer información del producto
                product = extract_product_info(card, base_url)
                
                if product and product.get('model'):
                    products.append(product)
                    print(f"  ✓ [{idx}] {product['model']}")
                    
                # Pequeña pausa para no sobrecargar el servidor
                time.sleep(0.1)
                
            except Exception as e:
                print(f"  ⚠️  Error procesando producto {idx}: {e}")
                continue
        
        print(f"\n✅ Scraping completado: {len(products)} productos extraídos")
        
    except requests.RequestException as e:
        print(f"❌ Error de conexión: {e}")
        print("⚠️  Usando catálogo de respaldo...")
        return get_products_catalog_fallback()
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        print("⚠️  Usando catálogo de respaldo...")
        return get_products_catalog_fallback()
    
    # Si no se encontraron productos, usar fallback
    if not products:
        print("⚠️  No se encontraron productos, usando catálogo de respaldo...")
        return get_products_catalog_fallback()
    
    return products


def extract_product_info(card, base_url: str) -> Dict:
    """
    Extrae información de un elemento HTML de producto de PEISA.
    
    Estructura esperada:
    <a href="/productos/[nombre]">
        <article>
            <div class="text-peisared-600">CATEGORÍA</div>
            <h4>NOMBRE PRODUCTO</h4>
            <p>Descripción</p>
        </article>
    </a>
    
    Args:
        card: Elemento <a> que contiene el producto
        base_url: URL base del sitio
        
    Returns:
        Diccionario con información del producto
    """
    product = {}
    
    try:
        article = card.find('article')
        if not article:
            return product
        
        # Extraer categoría (texto en rojo)
        category_elem = article.find('div', class_=re.compile(r'peisared|uppercase'))
        category = category_elem.get_text(strip=True) if category_elem else ""
        
        # Extraer nombre/modelo (h4)
        title_elem = article.find(['h4', 'h3', 'h2'])
        if title_elem:
            product['model'] = title_elem.get_text(strip=True)
        else:
            return product  # Sin nombre, no es válido
        
        # Extraer descripción (párrafo)
        desc_elem = article.find('p')
        if desc_elem:
            product['description'] = desc_elem.get_text(strip=True)
        else:
            product['description'] = f"{category} - {product['model']}"
        
        # Determinar familia/categoría
        if category:
            product['family'] = map_category_to_family(category)
        else:
            product['family'] = determine_family(product.get('model', ''))
        
        product['type'] = determine_type(product.get('model', ''))
        
        # Extraer potencia (si está disponible en el texto)
        full_text = article.get_text()
        power_match = re.search(r'(\d+)\s*(w|kw|kcal)', full_text, re.I)
        if power_match:
            power_value = int(power_match.group(1))
            unit = power_match.group(2).lower()
            if unit == 'kw':
                power_value *= 1000
            elif unit == 'kcal':
                power_value = int(power_value * 1.163)  # Convertir kcal/h a W
            product['power_w'] = power_value
        else:
            product['power_w'] = 0
        
        # Valores por defecto
        product['features'] = []
        product['applications'] = []
        product['liters'] = 0
        product['max_pressure_bar'] = 10
        product['dimensions'] = "N/A"
        
        # URL del producto
        product_url = card.get('href', '')
        if product_url and not product_url.startswith('http'):
            product['url'] = base_url + product_url
        else:
            product['url'] = product_url
        
    except Exception as e:
        print(f"    Error extrayendo info: {e}")
    
    return product


def map_category_to_family(category: str) -> str:
    """Mapea la categoría de PEISA a nuestra familia de productos"""
    category_lower = category.lower()
    
    if 'caldera' in category_lower:
        return "Calderas"
    elif 'radiador' in category_lower or 'toallero' in category_lower:
        return "Radiadores"
    elif 'termotanque' in category_lower or 'tanque' in category_lower:
        return "Termotanques"
    elif 'calefon' in category_lower:
        return "Calefones"
    elif 'termostato' in category_lower:
        return "Termostatos"
    elif 'piscina' in category_lower or 'climatizador' in category_lower:
        return "Climatización Piscinas"
    elif 'detector' in category_lower:
        return "Seguridad"
    else:
        return "Otros"


def determine_family(model_name: str) -> str:
    """Determina la familia del producto según su nombre"""
    model_lower = model_name.lower()
    
    if any(word in model_lower for word in ['radiador', 'broen', 'panel', 'toallero']):
        return "Radiadores"
    elif any(word in model_lower for word in ['caldera', 'boiler', 'prima', 'diva', 'summa']):
        return "Calderas"
    elif any(word in model_lower for word in ['piso', 'radiante', 'suelo']):
        return "Piso Radiante"
    elif any(word in model_lower for word in ['termotanque', 'tanque', 'agua caliente']):
        return "Termotanques"
    elif any(word in model_lower for word in ['bomba', 'circulador']):
        return "Accesorios"
    else:
        return "Otros"


def determine_type(model_name: str) -> str:
    """Determina el tipo específico del producto"""
    model_lower = model_name.lower()
    
    if 'panel' in model_lower:
        return "Radiador de panel"
    elif 'toallero' in model_lower:
        return "Radiador toallero"
    elif 'caldera' in model_lower:
        return "Caldera mural"
    elif 'piso' in model_lower or 'radiante' in model_lower:
        return "Sistema completo"
    elif 'termotanque' in model_lower:
        return "Termotanque eléctrico"
    elif 'bomba' in model_lower:
        return "Bomba circuladora"
    else:
        return "Producto de calefacción"


def get_products_catalog_fallback() -> List[Dict]:
    """
    Retorna el catálogo de productos PEISA.
    En producción, esto podría scrapear https://peisa.com.ar/productos
    Por ahora, usamos un catálogo curado basado en productos reales.
    """
    return [
        {
            "model": "BROEN PLUS 800",
            "family": "Radiadores",
            "type": "Radiador de panel",
            "power_w": 800,
            "description": "Radiador de panel de acero de alta eficiencia, ideal para ambientes medianos de 8-12m². Diseño compacto y moderno con acabado esmaltado.",
            "dimentions": "600x800mm",
            "liters": 4.5,
            "max_pressure_bar": 10,
            "features": ["Alta eficiencia térmica", "Diseño compacto", "Fácil instalación"],
            "applications": ["Dormitorios", "Oficinas", "Espacios medianos"]
        },
        {
            "model": "BROEN PLUS 1200",
            "family": "Radiadores",
            "type": "Radiador de panel",
            "power_w": 1200,
            "description": "Radiador de panel de acero para espacios grandes de 12-18m². Excelente relación calidad-precio con distribución uniforme del calor.",
            "dimentions": "600x1200mm",
            "liters": 6.8,
            "max_pressure_bar": 10,
            "features": ["Mayor potencia", "Distribución uniforme", "Bajo consumo"],
            "applications": ["Salas de estar", "Comedores", "Espacios amplios"]
        },
        {
            "model": "BROEN PLUS 1600",
            "family": "Radiadores",
            "type": "Radiador de panel",
            "power_w": 1600,
            "description": "Radiador de alta potencia para ambientes grandes de 18-25m². Ideal para zonas frías con excelente rendimiento térmico.",
            "dimentions": "600x1600mm",
            "liters": 9.2,
            "max_pressure_bar": 10,
            "features": ["Alta potencia", "Zona fría", "Rendimiento superior"],
            "applications": ["Living grandes", "Locales comerciales", "Zonas frías"]
        },
        {
            "model": "PEISA PISO RADIANTE KIT 15m²",
            "family": "Piso Radiante",
            "type": "Sistema completo",
            "power_w": 1500,
            "description": "Kit completo de piso radiante para 15m². Incluye tubería PEX, colector, aislación y accesorios. Confort térmico superior.",
            "dimentions": "Kit para 15m²",
            "liters": 0,
            "max_pressure_bar": 6,
            "features": ["Confort superior", "Ahorro energético", "Distribución uniforme"],
            "applications": ["Construcciones nuevas", "Renovaciones", "Baños"]
        },
        {
            "model": "PEISA PISO RADIANTE KIT 30m²",
            "family": "Piso Radiante",
            "type": "Sistema completo",
            "power_w": 3000,
            "description": "Kit completo de piso radiante para 30m². Sistema eficiente con control de temperatura por zona. Ideal para viviendas.",
            "dimentions": "Kit para 30m²",
            "liters": 0,
            "max_pressure_bar": 6,
            "features": ["Control por zonas", "Máximo confort", "Eficiencia energética"],
            "applications": ["Departamentos", "Casas", "Oficinas"]
        },
        {
            "model": "CALDERA PEISA 12000",
            "family": "Calderas",
            "type": "Caldera mural",
            "power_w": 12000,
            "description": "Caldera mural de condensación de alta eficiencia para hasta 100m². Modulante con control digital y bajo consumo.",
            "dimentions": "800x450x350mm",
            "liters": 0,
            "max_pressure_bar": 3,
            "features": ["Condensación", "Modulante", "Control digital", "Bajo consumo"],
            "applications": ["Departamentos", "Casas pequeñas", "Calefacción central"]
        },
        {
            "model": "CALDERA PEISA 24000",
            "family": "Calderas",
            "type": "Caldera mural",
            "power_w": 24000,
            "description": "Caldera mural de condensación para hasta 200m². Doble servicio: calefacción y agua caliente sanitaria. Alta eficiencia.",
            "dimentions": "900x500x400mm",
            "liters": 0,
            "max_pressure_bar": 3,
            "features": ["Doble servicio", "Alta potencia", "Eficiencia A++", "Silenciosa"],
            "applications": ["Casas grandes", "Locales", "Instalaciones completas"]
        },
        {
            "model": "TERMOTANQUE PEISA 80L",
            "family": "Termotanques",
            "type": "Termotanque eléctrico",
            "power_w": 1500,
            "description": "Termotanque eléctrico de 80 litros para 3-4 personas. Resistencia blindada, aislación de poliuretano de alta densidad.",
            "dimentions": "450x450x900mm",
            "liters": 80,
            "max_pressure_bar": 8,
            "features": ["Resistencia blindada", "Aislación superior", "Termostato regulable"],
            "applications": ["Familias 3-4 personas", "Departamentos", "Casas"]
        },
        {
            "model": "TERMOTANQUE PEISA 120L",
            "family": "Termotanques",
            "type": "Termotanque eléctrico",
            "power_w": 2000,
            "description": "Termotanque eléctrico de 120 litros para 4-6 personas. Mayor capacidad con recuperación rápida de temperatura.",
            "dimentions": "500x500x1100mm",
            "liters": 120,
            "max_pressure_bar": 8,
            "features": ["Mayor capacidad", "Recuperación rápida", "Bajo consumo"],
            "applications": ["Familias grandes", "Casas", "Alto consumo ACS"]
        },
        {
            "model": "RADIADOR TOALLERO 500W",
            "family": "Radiadores",
            "type": "Radiador toallero",
            "power_w": 500,
            "description": "Radiador toallero cromado para baño. Conexión lateral, diseño elegante. Ideal para baños de 4-6m².",
            "dimentions": "500x1200mm",
            "liters": 2.5,
            "max_pressure_bar": 10,
            "features": ["Diseño elegante", "Cromado", "Doble función"],
            "applications": ["Baños", "Toilettes", "Vestidores"]
        },
        {
            "model": "COLECTOR PISO RADIANTE 8 VIAS",
            "family": "Piso Radiante",
            "type": "Accesorio",
            "power_w": 0,
            "description": "Colector de latón con 8 vías para distribución de piso radiante. Incluye caudalímetros y válvulas de corte.",
            "dimentions": "600x300mm",
            "liters": 0,
            "max_pressure_bar": 6,
            "features": ["8 circuitos", "Caudalímetros incluidos", "Latón cromado"],
            "applications": ["Instalaciones piso radiante", "Control por zonas"]
        },
        {
            "model": "BOMBA CIRCULADORA WILO 25-40",
            "family": "Accesorios",
            "type": "Bomba circuladora",
            "power_w": 45,
            "description": "Bomba circuladora de alta eficiencia clase A para sistemas de calefacción. 3 velocidades ajustables.",
            "dimentions": "180x150mm",
            "liters": 0,
            "max_pressure_bar": 10,
            "features": ["Clase A", "3 velocidades", "Silenciosa", "Bajo consumo"],
            "applications": ["Sistemas de calefacción", "Piso radiante", "Radiadores"]
        },
        {
            "model": "VALVULA TERMOSTATICA",
            "family": "Accesorios",
            "type": "Válvula",
            "power_w": 0,
            "description": "Válvula termostática para radiadores. Control preciso de temperatura ambiente con cabezal regulable.",
            "dimentions": "1/2 pulgada",
            "liters": 0,
            "max_pressure_bar": 10,
            "features": ["Control preciso", "Ahorro energético", "Fácil instalación"],
            "applications": ["Radiadores", "Control individual", "Ahorro energético"]
        },
        {
            "model": "VASO EXPANSION 12L",
            "family": "Accesorios",
            "type": "Vaso de expansión",
            "power_w": 0,
            "description": "Vaso de expansión de 12 litros para sistemas de calefacción cerrados. Membrana EPDM de alta calidad.",
            "dimentions": "270x350mm",
            "liters": 12,
            "max_pressure_bar": 10,
            "features": ["Membrana EPDM", "Alta durabilidad", "Precargado"],
            "applications": ["Sistemas cerrados", "Calderas", "Instalaciones completas"]
        }
    ]

def get_products_catalog(use_scraping: bool = False) -> List[Dict]:
    """
    Retorna el catálogo de productos PEISA.
    
    Args:
        use_scraping: Si True, intenta hacer scraping real. Si False, usa fallback.
        
    Returns:
        Lista de productos
    """
    if use_scraping:
        return scrape_peisa_products()
    else:
        return get_products_catalog_fallback()


def save_catalog(filename: str = "data/products_catalog.json", use_scraping: bool = True):
    """
    Guarda el catálogo en un archivo JSON.
    
    Args:
        filename: Ruta donde guardar el archivo
        use_scraping: Si True, intenta scraping real de PEISA
        
    Returns:
        Lista de productos guardados
    """
    import os
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    print(f"\n{'='*60}")
    print(f"🚀 SCRAPER DE PRODUCTOS PEISA")
    print(f"{'='*60}\n")
    
    # Obtener productos (con o sin scraping)
    products = get_products_catalog(use_scraping=use_scraping)
    
    # Guardar en JSON
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*60}")
    print(f"✅ Catálogo guardado exitosamente")
    print(f"📁 Archivo: {filename}")
    print(f"📦 Total productos: {len(products)}")
    print(f"{'='*60}\n")
    
    return products


if __name__ == "__main__":
    import sys
    
    # Verificar si se pasa argumento --no-scraping
    use_scraping = "--no-scraping" not in sys.argv
    
    if use_scraping:
        print("🌐 Modo: SCRAPING REAL de https://peisa.com.ar/productos")
    else:
        print("📋 Modo: Catálogo de respaldo (sin scraping)")
    
    # Ejecutar scraping y guardar
    products = save_catalog(use_scraping=use_scraping)
    
    # Mostrar resumen
    print(f"\n📊 RESUMEN DEL CATÁLOGO:")
    print(f"{'='*60}")
    
    # Agrupar por familia
    families = {}
    for p in products:
        family = p.get('family', 'Otros')
        families[family] = families.get(family, 0) + 1
    
    for family, count in sorted(families.items()):
        print(f"  • {family}: {count} productos")
    
    print(f"\n📋 PRODUCTOS EXTRAÍDOS:")
    print(f"{'='*60}")
    for idx, p in enumerate(products, 1):
        power = f"{p['power_w']}W" if p['power_w'] > 0 else "N/A"
        print(f"  {idx:2d}. {p['model']:<40} ({p['family']}) - {power}")
