from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import json
import math
from math import ceil
from bisect import bisect_left
from .models import RADIATOR_MODELS

knowledge_base = None

def init_knowledge_base(kb):
    """Inicializa la base de conocimiento"""
    global knowledge_base
    knowledge_base = kb

def get_node_by_id(node_id):
    """Busca un nodo por su ID en la base de conocimiento"""
    if knowledge_base is None:
        raise RuntimeError("Knowledge base not initialized")
    for node in knowledge_base:
        if node.get('id') == node_id:
            return node
    return None

def replace_variables(text: str, context: Dict[str, Any]) -> str:
    """Reemplaza variables en el texto usando el contexto"""
    if not isinstance(text, str):
        return text
        
    for key, val in context.items():
        if isinstance(val, (int, float, str)):
            text = text.replace("{{"+key+"}}", str(val))
    
    try:
        from jinja2 import Template
        template = Template(text)
        return template.render(**context)
    except Exception as e:
        print(f"Error en template Jinja2: {e}")
        return text

def filter_radiators(radiator_type: str, installation: str, style: str, color: str, heat_load: float) -> List[Dict[str, Any]]:
    """Filtra radiadores según las preferencias del usuario"""
    recommended = []
    
    for name, model in RADIATOR_MODELS.items():
        # Filtrar por tipo de radiador (aceptar si coincide o si está en la lista)
        if isinstance(model.get('type'), str):
            if model.get('type') != radiator_type:
                continue
        else:
            if radiator_type not in model.get('type', []):
                continue
                
        # Filtrar por tipo de instalación
        if installation != 'cualquiera':
            if isinstance(model['installation'], str):
                if model['installation'] != installation:
                    continue
            elif installation not in model['installation']:
                continue
                
        # Filtrar por estilo
        if style != 'cualquiera' and model['style'] != style:
            continue
            
        # Filtrar por color
        if color != 'cualquiera' and color not in model['colors']:
            continue
            
        recommended.append({
            'name': name,
            'description': model['description'],
            'coeficiente': model.get('coeficiente', 1.0),
            'potencia': model['potencia'],
            'colors': model['colors']
        })
    
    # Ordenar por mejor ajuste a la carga térmica
    recommended.sort(key=lambda x: abs(x['potencia'] * x['coeficiente'] - heat_load))
    
    return recommended[:3]  # Top 3 recomendaciones

def format_radiator_recommendations(models: List[Dict[str, Any]], heat_load: float) -> str:
    """Formatea las recomendaciones para mostrarlas al usuario"""
    if not models or not isinstance(models, list):
        return "No encontramos modelos que coincidan con tus requisitos. Por favor intenta con diferentes parámetros."
    
    result = []
    for i, model in enumerate(models, 1):
        try:
            potencia_efectiva = model.get('potencia', 0) * model.get('coeficiente', 1)
            modulos_estimados = ceil(heat_load / potencia_efectiva) if potencia_efectiva > 0 else 0
            
            model_info = [
                f"{i}. {model.get('name', 'Modelo desconocido')}",
                f"   - Potencia efectiva: {potencia_efectiva:.0f} kcal/h",
                f"   - Módulos estimados: {modulos_estimados}",
                f"   - Descripción: {model.get('description', 'Sin descripción disponible')}"
            ]
            
            if 'colors' in model:
                model_info.append(f"   - Colores disponibles: {', '.join(model['colors'])}")
                
            result.append("\n".join(model_info))
        except Exception as e:
            print(f"Error formateando modelo {model}: {e}")
            continue
    
    return "\n\n".join(result) if result else "No se pudieron generar recomendaciones."

def perform_calculation(node: Dict[str, Any], context: Dict[str, Any]) -> None:
    """Ejecuta los cálculos definidos en un nodo"""
    params = node.get("parametros", {})
    for key, val in params.items():
        context[key] = val

    for action in node.get("acciones", []):
        exec_expression(action, context)

def calculate_boiler(total_heat_load: float, has_hot_water: bool = False) -> Dict[str, Any]:
    """
    Calcula la potencia de caldera necesaria según la documentación del sistema experto
    
    Args:
        total_heat_load: Carga térmica total en kcal/h
        has_hot_water: Si requiere agua caliente sanitaria
    
    Returns:
        Diccionario con potencia recomendada y tipo de caldera
    """
    safety_factor = 1.2
    hot_water_extra = 5000 if has_hot_water else 0  # kcal/h adicionales para ACS
    
    required_power = (total_heat_load * safety_factor) + hot_water_extra
    
    # Redondear a potencias estándar: 18000, 24000, 30000, 35000, 45000 kcal/h
    standard_powers = [18000, 24000, 30000, 35000, 45000]
    
    selected_power = standard_powers[-1]  # Por defecto la máxima
    for power in standard_powers:
        if power >= required_power:
            selected_power = power
            break
    
    boiler_type = "Caldera mixta (calefacción + ACS)" if has_hot_water else "Caldera estándar (solo calefacción)"
    
    return {
        'potencia_requerida': required_power,
        'potencia_recomendada': selected_power,
        'tipo_caldera': boiler_type,
        'factor_seguridad': safety_factor
    }

def recommend_towel_rack_from_catalog() -> Dict[str, Any]:
    """
    Recomienda un toallero del catálogo basado en popularidad y características
    
    Returns:
        Diccionario con información del toallero recomendado
    """
    # Toalleros recomendados por defecto
    towel_racks = [
        {
            'name': 'Toallero Cromado Premium 500x800',
            'potencia': 350,
            'medidas': '500mm x 800mm',
            'color': 'Cromado',
            'descripcion': 'Toallero de diseño moderno con acabado cromado brillante',
            'precio_aprox': 'Consultar'
        },
        {
            'name': 'Toallero Blanco Clásico 600x1000',
            'potencia': 450,
            'medidas': '600mm x 1000mm',
            'color': 'Blanco',
            'descripcion': 'Toallero tradicional de gran capacidad',
            'precio_aprox': 'Consultar'
        }
    ]
    
    # Devolver el primero como recomendación principal
    return towel_racks[0]

def format_towel_rack_recommendation(towel_rack: Dict[str, Any]) -> str:
    """
    Formatea la recomendación de toallero para mostrarla al usuario
    
    Args:
        towel_rack: Diccionario con información del toallero
        
    Returns:
        String formateado con la recomendación
    """
    if not towel_rack:
        return "No se encontró un toallero adecuado. Por favor contacte a nuestro equipo de ventas."
    
    recommendation = [
        f"🔥 {towel_rack.get('name', 'Toallero')}",
        f"   • Potencia: {towel_rack.get('potencia', 'N/A')} W",
        f"   • Medidas: {towel_rack.get('medidas', 'N/A')}",
        f"   • Color: {towel_rack.get('color', 'N/A')}",
        f"   • {towel_rack.get('descripcion', '')}",
        f"   • Precio: {towel_rack.get('precio_aprox', 'Consultar')}"
    ]
    
    return "\n".join(recommendation)

def search_floor_heating_products(potencia_watts: float) -> List[Dict[str, Any]]:
    """
    Busca productos para piso radiante en el catálogo
    
    Args:
        potencia_watts: Potencia requerida en watts
        
    Returns:
        Lista de productos recomendados
    """
    from query.query import search_filtered
    
    query = f"piso radiante caño {potencia_watts} watts"
    products = search_filtered(query, top_k=3)
    
    return products if products else []

def search_boiler_products(potencia_kcal: float, tiene_acs: bool = False) -> List[Dict[str, Any]]:
    """
    Busca calderas en el catálogo
    
    Args:
        potencia_kcal: Potencia requerida en kcal/h
        tiene_acs: Si necesita agua caliente sanitaria
        
    Returns:
        Lista de calderas recomendadas
    """
    from query.query import search_filtered
    
    tipo = "mixta ACS" if tiene_acs else "estándar"
    query = f"caldera {tipo} {potencia_kcal} kcal"
    products = search_filtered(query, top_k=3)
    
    return products if products else []

def format_product_list(products: List[Dict[str, Any]]) -> str:
    """
    Formatea una lista de productos para mostrar al usuario
    
    Args:
        products: Lista de productos del catálogo
        
    Returns:
        String formateado con los productos
    """
    if not products:
        return "No se encontraron productos específicos en el catálogo. Por favor consulte con nuestro equipo de ventas."
    
    result = []
    for i, prod in enumerate(products, 1):
        prod_info = [
            f"\n{i}. {prod.get('model', 'Producto')}",
            f"   • Familia: {prod.get('family', 'N/A')}",
            f"   • Tipo: {prod.get('type', 'N/A')}"
        ]
        
        if prod.get('power'):
            prod_info.append(f"   • Potencia: {prod.get('power')} W")
        
        if prod.get('dimensions'):
            prod_info.append(f"   • Dimensiones: {prod.get('dimensions')}")
            
        if prod.get('description'):
            prod_info.append(f"   • {prod.get('description')}")
        
        result.append("\n".join(prod_info))
    
    return "\n".join(result)

def exec_expression(expr: str, context: Dict[str, Any]) -> None:
    """Ejecuta una expresión matemática y guarda el resultado en el contexto"""
    try:
        print(f"[DEBUG] Ejecutando expresión: {expr}")
        
        # Dividir la expresión en variable y valor
        var, val_expr = [x.strip() for x in expr.split("=", 1)]
        
        print(f"[DEBUG] Evaluando: {var} = {val_expr}")
        
        # Crear un contexto seguro solo con valores simples
        safe_context = {}
        for key, value in context.items():
            # Solo incluir tipos básicos y seguros
            if isinstance(value, (int, float, str, bool, list, dict, type(None))):
                safe_context[key] = value
        
        # Agregar funciones permitidas
        safe_context.update({
            'filter_radiators': filter_radiators,
            'format_radiator_recommendations': format_radiator_recommendations,
            'calculate_boiler': calculate_boiler,
            'recommend_towel_rack_from_catalog': recommend_towel_rack_from_catalog,
            'format_towel_rack_recommendation': format_towel_rack_recommendation,
            'search_floor_heating_products': search_floor_heating_products,
            'search_boiler_products': search_boiler_products,
            'format_product_list': format_product_list,
            'ceil': ceil,
            'round': round,
            'abs': abs,
            'min': min,
            'max': max,
        })
        
        # Evaluar la expresión
        val = eval(val_expr, {"__builtins__": {}}, safe_context)
        context[var] = val
        
        print(f"[DEBUG] Resultado: {var} = {val}")
    except Exception as e:
        print(f"[ERROR] Error evaluando expresión '{expr}': {e}")
        print(f"[ERROR] Contexto disponible: {list(context.keys())}")
        import traceback
        traceback.print_exc()
        raise




