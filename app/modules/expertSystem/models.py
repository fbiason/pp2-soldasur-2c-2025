"""
models.py - Modelos de productos cargados dinámicamente

Este módulo proporciona acceso a los modelos de productos cargados
desde la base de datos Excel (Products_db.xlsx).
"""

from typing import Dict, Any
from .product_loader import load_radiator_models, get_product_loader

# Cargar modelos dinámicamente desde Excel
RADIATOR_MODELS = load_radiator_models()

# Función para recargar modelos si es necesario
def reload_models():
    """Recarga los modelos desde el archivo Excel"""
    global RADIATOR_MODELS
    loader = get_product_loader()
    loader.load_products()
    RADIATOR_MODELS = loader.get_radiators_dict()
    print(f"✓ Modelos recargados: {len(RADIATOR_MODELS)} radiadores")
