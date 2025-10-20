# app/product_scraper.py - Scraper y catálogo de productos PEISA
import json
from typing import List, Dict

def get_products_catalog() -> List[Dict]:
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

def save_catalog(filename: str = "data/products_catalog.json"):
    """Guarda el catálogo en un archivo JSON"""
    import os
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    products = get_products_catalog()
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Catálogo guardado: {len(products)} productos en {filename}")
    return products

if __name__ == "__main__":
    products = save_catalog()
    print(f"\n📦 Catálogo PEISA:")
    for p in products:
        print(f"  • {p['model']} ({p['family']}) - {p['power_w']}W")
