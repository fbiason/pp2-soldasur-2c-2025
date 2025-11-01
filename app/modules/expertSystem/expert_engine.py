from typing import Dict, Any, List, Optional
import json
from math import ceil
from bisect import bisect_left
from pathlib import Path
from .models import RADIATOR_MODELS
from .product_loader import get_product_loader
from app.app import replace_variables, perform_calculation


class ExpertEngine:
    """
    Motor del sistema experto con capacidad de enriquecimiento RAG.
    Maneja el flujo conversacional guiado basado en la base de conocimiento.
    """
    
    def __init__(self, knowledge_base_path: str = "app/peisa_advisor_knowledge_base.json"):
        """
        Inicializa el motor experto.
        
        Args:
            knowledge_base_path: Ruta al archivo JSON de la base de conocimiento
        """
        self.knowledge_base = []
        self.rag_engine = None  # Se inyectará después
        self.rag_enrichment_enabled = True
        self.product_loader = get_product_loader()  # Cargador de productos dinámico
        
        # Cargar base de conocimiento
        try:
            with open(knowledge_base_path, "r", encoding="utf-8") as f:
                self.knowledge_base = json.load(f)
        except FileNotFoundError:
            print(f"Advertencia: No se encontró {knowledge_base_path}")
    
    def set_rag_engine(self, rag_engine):
        """Inyecta el motor RAG para enriquecimiento"""
        self.rag_engine = rag_engine
    
    def get_node_by_id(self, node_id: str) -> Optional[Dict[str, Any]]:
        """
        Busca un nodo por su ID en la base de conocimiento.
        
        Args:
            node_id: ID del nodo a buscar
            
        Returns:
            Diccionario con los datos del nodo o None si no se encuentra
        """
        for node in self.knowledge_base:
            if node.get('id') == node_id:
                return node
        return None
    
    async def process(self, conversation_id: str, expert_state: Dict[str, Any],
                     option_index: Optional[int] = None,
                     input_values: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Procesa la interacción del usuario en el flujo experto.
        
        Args:
            conversation_id: ID de la conversación
            expert_state: Estado actual del experto (current_node, variables)
            option_index: Índice de opción seleccionada
            input_values: Valores de entrada del usuario
            
        Returns:
            Diccionario con la respuesta y el siguiente estado
        """
        current_node_id = expert_state.get('current_node', 'inicio')
        context = expert_state.get('variables', {})
        
        print(f"[DEBUG] Processing node: {current_node_id}, option_index: {option_index}, input_values: {input_values}")
        
        node = self.get_node_by_id(current_node_id)
        if not node:
            return {
                'error': 'Nodo no encontrado',
                'node_id': current_node_id
            }
        
        # Procesar entrada del usuario si existe
        if option_index is not None or input_values:
            result = self._process_user_input(node, context, option_index, input_values)
            if result.get('error'):
                return result
            
            # Avanzar al siguiente nodo
            next_node_id = result.get('next_node')
            print(f"[DEBUG] next_node_id from result: {next_node_id}")
            if next_node_id:
                expert_state['current_node'] = next_node_id
                node = self.get_node_by_id(next_node_id)
                print(f"[DEBUG] Advanced to node: {next_node_id}, node found: {node is not None}")
        
        # Obtener el mensaje del nodo actual
        return await self._get_node_message(node, context, expert_state)
    
    def _process_user_input(self, node: Dict[str, Any], context: Dict[str, Any],
                           option_index: Optional[int], 
                           input_values: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Procesa la entrada del usuario según el tipo de nodo"""
        
        # Nodo de entrada de usuario (numérico)
        if node.get('tipo') == 'entrada_usuario':
            try:
                if 'variable' in node:
                    value = str(input_values.get('value', '')).replace(',', '.')
                    context[node['variable']] = float(value)
                elif 'variables' in node:
                    for var in node['variables']:
                        value = str(input_values.get(var, '')).replace(',', '.')
                        context[var] = float(value)
                
                return {'next_node': node['siguiente']}
            
            except (ValueError, KeyError) as e:
                return {
                    'error': 'Por favor ingrese valores numéricos válidos (ej: 4.5, 3.75)',
                    'node_id': node['id']
                }
        
        # Nodo con opciones
        elif 'opciones' in node and option_index is not None:
            if 0 <= option_index < len(node['opciones']):
                selected = node['opciones'][option_index]
                print(f"[DEBUG] Selected option: {selected.get('texto')}, siguiente: {selected.get('siguiente')}")
                
                # Determinar qué variable usar (la definida en el nodo o el ID del nodo)
                variable_name = node.get('variable', node['id'])
                
                # Guardar el valor
                context[variable_name] = selected.get('valor', selected['texto'])
                
                # Guardar también el texto para mostrar (si hay variable definida)
                if 'variable' in node:
                    context[f"{variable_name}_texto"] = selected['texto']
                else:
                    context[f"{node['id']}_texto"] = selected['texto']
                
                print(f"[DEBUG] Returning next_node: {selected['siguiente']}")
                return {'next_node': selected['siguiente']}
            else:
                return {
                    'error': 'Opción inválida',
                    'node_id': node['id']
                }
        
        return {}
    
    async def _get_node_message(self, node: Dict[str, Any], context: Dict[str, Any],
                               expert_state: Dict[str, Any]) -> Dict[str, Any]:
        """Obtiene el mensaje a mostrar para el nodo actual"""
        print(f"[DEBUG] _get_node_message for node: {node['id']}, tipo: {node.get('tipo')}, has opciones: {'opciones' in node}, has pregunta: {'pregunta' in node}")
        
        # Nodo de cálculo: ejecutar y avanzar automáticamente
        if node.get('tipo') == 'calculo':
            try:
                perform_calculation(node, context)
                # Actualizar el contexto en expert_state
                expert_state['variables'] = context
                expert_state['current_node'] = node['siguiente']
                next_node = self.get_node_by_id(node['siguiente'])
                return await self._get_node_message(next_node, context, expert_state)
            except Exception as e:
                print(f"[ERROR] Error en cálculo del nodo {node['id']}: {e}")
                import traceback
                traceback.print_exc()
                return {
                    'type': 'error',
                    'node_id': node['id'],
                    'text': f'Error al procesar el cálculo: {str(e)}',
                    'error': str(e),
                    'expert_state': expert_state
                }
        
        # Nodo con pregunta
        elif 'pregunta' in node:
            # Actualizar variables en el estado
            expert_state['variables'] = context
            
            response = {
                'type': 'question',
                'node_id': node['id'],
                'text': replace_variables(node['pregunta'], context),
                'expert_state': expert_state
            }
            
            # Agregar opciones si existen
            if 'opciones' in node:
                response['options'] = [opt['texto'] for opt in node['opciones']]
            # Si NO tiene opciones pero ES un nodo de entrada de usuario
            elif node.get('tipo') == 'entrada_usuario':
                if 'variable' in node:
                    print(f"[DEBUG] Setting input_type='number' for variable: {node['variable']}")
                    response['input_type'] = 'number'
                    response['input_label'] = node.get('etiqueta', 'Ingrese el valor')
                elif 'variables' in node:
                    print(f"[DEBUG] Setting input_type='multiple' for variables: {node['variables']}")
                    response['input_type'] = 'multiple'
                    response['inputs'] = [
                        {'name': var, 'label': f'Ingrese {var} (metros)', 'type': 'number'}
                        for var in node['variables']
                    ]
            
            # Enriquecimiento RAG si está habilitado
            if self.rag_enrichment_enabled and node.get('enrich_with_rag') and self.rag_engine:
                enrichment = await self._enrich_with_rag(node, context)
                if enrichment:
                    response['additional_info'] = enrichment
            
            return response
        
        # Nodo de respuesta (final o intermedio)
        elif node.get('tipo') == 'respuesta':
            # Actualizar variables en el estado
            expert_state['variables'] = context
            
            response = {
                'type': 'response',
                'node_id': node['id'],
                'text': replace_variables(node['texto'], context),
                'expert_state': expert_state
            }
            
            # Si tiene opciones, no es final
            if 'opciones' in node:
                response['options'] = [opt['texto'] for opt in node['opciones']]
                response['is_final'] = False
            else:
                response['is_final'] = True
            
            return response
        
        # Nodo con opciones dinámicas
        elif node.get('tipo') == 'opciones_dinamicas':
            if 'modelos_recomendados' in context:
                models = context['modelos_recomendados']
                return {
                    'type': 'question',
                    'node_id': node['id'],
                    'text': node['pregunta'],
                    'options': [
                        f"{model['name']} (Potencia: {model['potencia']*model['coeficiente']:.0f} kcal/h)"
                        for model in models
                    ],
                    'variables': context
                }
        
        return {
            'error': 'Tipo de nodo no reconocido',
            'node_id': node['id']
        }
    
    async def _enrich_with_rag(self, node: Dict[str, Any], 
                              context: Dict[str, Any]) -> Optional[str]:
        """
        Enriquece la respuesta del nodo con información del RAG.
        
        Args:
            node: Nodo actual
            context: Contexto de variables
            
        Returns:
            Información adicional del RAG o None
        """
        if not self.rag_engine:
            return None
        
        try:
            # Construir query para el RAG basado en el nodo
            query = node.get('rag_query', node.get('pregunta', ''))
            
            # Obtener información relevante del RAG
            rag_result = await self.rag_engine.get_context(
                query=query,
                filters=node.get('rag_filters', {})
            )
            
            return rag_result.get('summary', '')
        
        except Exception as e:
            print(f"Error en enriquecimiento RAG: {e}")
            return None
    
    async def suggest_next_step(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sugiere el siguiente paso basado en el contexto actual.
        Útil para el modo híbrido.
        
        Args:
            context: Contexto de variables del experto
            
        Returns:
            Sugerencia de siguiente paso
        """
        # Analizar qué información ya tenemos
        has_area = 'superficie' in context or any('m2' in str(k).lower() for k in context.keys())
        has_location = 'zona' in context or 'ubicacion' in context
        has_type = 'tipo_calefaccion' in context or 'inicio' in context
        
        # Sugerir siguiente paso
        if not has_type:
            return {
                'suggestion': '¿Qué tipo de calefacción deseas calcular?',
                'options': ['Piso radiante', 'Radiadores', 'Calderas']
            }
        elif not has_area:
            return {
                'suggestion': '¿Cuál es la superficie a calefaccionar?',
                'input_type': 'number',
                'input_label': 'Superficie en m²'
            }
        elif not has_location:
            return {
                'suggestion': '¿En qué zona geográfica se encuentra?',
                'options': ['Norte', 'Centro', 'Sur']
            }
        else:
            return {
                'suggestion': 'Tengo suficiente información. ¿Quieres que continúe con el cálculo?',
                'options': ['Sí, continuar', 'No, quiero modificar algo']
            }
    
    def _replace_variables(self, text: str, context: Dict[str, Any]) -> str:
        """
        Reemplaza variables en el texto usando el contexto.
        Soporta tanto {{variable}} como templates Jinja2.
        
        Args:
            text: Texto con variables
            context: Contexto de variables
            
        Returns:
            Texto con variables reemplazadas
        """
        if not isinstance(text, str):
            return text
        
        # Reemplazo simple de {{variable}}
        for key, val in context.items():
            if isinstance(val, (int, float, str)):
                text = text.replace("{{"+key+"}}", str(val))
        
        # Intentar con Jinja2 para expresiones más complejas
        try:
            from jinja2 import Template
            template = Template(text)
            return template.render(**context)
        except Exception as e:
            # Si falla Jinja2, devolver el texto con reemplazo simple
            return text
    
    def _perform_calculation(self, node: Dict[str, Any], context: Dict[str, Any]) -> None:
        """
        Ejecuta los cálculos definidos en un nodo.
        
        Args:
            node: Nodo de tipo 'calculo'
            context: Contexto donde se guardan los resultados
        """
        # Agregar parámetros al contexto
        params = node.get("parametros", {})
        for key, val in params.items():
            context[key] = val
        
        # Ejecutar acciones (expresiones matemáticas)
        for action in node.get("acciones", []):
            self._exec_expression(action, context)
    
    def _exec_expression(self, expr: str, context: Dict[str, Any]) -> None:
        """
        Ejecuta una expresión matemática y guarda el resultado en el contexto.
        
        Args:
            expr: Expresión a evaluar (ej: "carga_termica = superficie * potencia_m2")
            context: Contexto donde se guarda el resultado
        """
        try:
            # Funciones especiales disponibles en expresiones
            local_context = {
                'filter_radiators': filter_radiators,
                'format_radiator_recommendations': format_radiator_recommendations,
                'recommend_boiler': recommend_boiler,
                'recommend_floor_heating_kit': recommend_floor_heating_kit,
                'recommend_radiator_from_catalog': recommend_radiator_from_catalog,
                'recommend_towel_rack_from_catalog': recommend_towel_rack_from_catalog,
                'format_towel_rack_recommendation': format_towel_rack_recommendation,
                'load_product_catalog': load_product_catalog,
                'ceil': ceil,
                'context': context
            }
            
            # Dividir la expresión en variable y valor
            var, val_expr = [x.strip() for x in expr.split("=", 1)]
            
            # Reemplazar context['variable'] por simplemente variable
            val_expr = val_expr.replace("context['", "").replace("']", "")
            
            # Evaluar la expresión con las variables del contexto
            val = eval(val_expr, {"__builtins__": None}, {**context, **local_context})
            context[var] = val
        
        except Exception as e:
            print(f"Error evaluando expresión '{expr}': {e}")
            raise


# Funciones auxiliares (mantenidas de app.py)

def filter_radiators(radiator_type: str, installation: str, style: str, 
                    color: str, heat_load: float) -> Dict[str, Any]:
    """
    Filtra y recomienda UN SOLO radiador según las preferencias del usuario.
    Usa products_catalog.json como fuente de datos.
    
    Args:
        radiator_type: Tipo de radiador
        installation: Tipo de instalación
        style: Estilo del radiador
        color: Color preferido
        heat_load: Carga térmica requerida
        
    Returns:
        UN radiador recomendado (el más adecuado)
    """
    # Usar la función de recomendación del catálogo
    # Convertir heat_load de kcal/h a W
    power_w = heat_load / 0.859845
    
    # Obtener recomendación del catálogo
    recommended = recommend_radiator_from_catalog(power_w)
    
    # Si no hay recomendación, retornar genérico
    if not recommended:
        return {
            'model': 'Radiador genérico',
            'description': f'Radiador para {heat_load:.0f} kcal/h',
            'family': 'Radiadores',
            'power_required_kcal': heat_load
        }
    
    return recommended


def format_radiator_recommendations(model: Dict[str, Any], 
                                   heat_load: float) -> str:
    """
    Formatea la recomendación de UN radiador para mostrarlo al usuario.
    
    Args:
        model: Modelo recomendado (diccionario)
        heat_load: Carga térmica requerida
        
    Returns:
        Texto formateado con la recomendación
    """
    if not model or not isinstance(model, dict):
        return "No encontramos un modelo que coincida con tus requisitos. Por favor intenta con diferentes parámetros."
    
    try:
        # Obtener información del producto
        model_name = model.get('model', 'Modelo desconocido')
        description = model.get('description', 'Sin descripción disponible')
        power_kcal = model.get('power_required_kcal', heat_load)
        url = model.get('url', '')
        
        # Formatear recomendación
        result = [
            f"✅ PRODUCTO RECOMENDADO: {model_name}",
            f"",
            f"📋 Descripción:",
            f"{description}",
            f"",
            f"⚡ Potencia requerida: {power_kcal:.0f} kcal/h",
        ]
        
        # Agregar características técnicas si existen
        if 'technical_features' in model and model['technical_features']:
            result.append("")
            result.append("🔧 Características técnicas:")
            for feature in model['technical_features'][:3]:  # Mostrar solo las primeras 3
                result.append(f"  • {feature}")
        
        # Agregar URL si existe
        if url:
            result.append("")
            result.append(f"🔗 Más información: {url}")
        
        return "\n".join(result)
        
    except Exception as e:
        print(f"Error formateando modelo {model}: {e}")
        return f"Recomendación: {model.get('model', 'Producto PEISA')}"


def load_product_catalog(catalog_path: str = "data/products_catalog.json") -> List[Dict[str, Any]]:
    """
    Carga el catálogo de productos desde products_catalog.json.
    Este es el mismo catálogo que usa el chatbot Soldy.
    
    Args:
        catalog_path: Ruta al archivo del catálogo JSON
        
    Returns:
        Lista de productos cargados desde products_catalog.json
    """
    loader = get_product_loader()
    # Retornar todos los productos del catálogo
    return loader.get_all_products()


def recommend_boiler(power_required_w: float, boiler_type: str, 
                    catalog: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """
    Recomienda una caldera específica del catálogo según la potencia requerida.
    Usa products_catalog.json como fuente de datos.
    
    Args:
        power_required_w: Potencia requerida en Watts
        boiler_type: Tipo de caldera ('mural' o 'piso')
        catalog: Catálogo de productos (se carga automáticamente si no se provee)
        
    Returns:
        Diccionario con la caldera recomendada del catálogo
    """
    if catalog is None:
        catalog = load_product_catalog()
    
    # Filtrar calderas del catálogo
    boilers = [p for p in catalog if p.get('family') == 'Calderas']
    
    # Filtrar por tipo si se especifica (buscar en type y description)
    if boiler_type == 'mural':
        boilers = [b for b in boilers 
                  if 'mural' in b.get('type', '').lower() 
                  or 'mural' in b.get('description', '').lower()]
    elif boiler_type == 'piso':
        boilers = [b for b in boilers 
                  if 'piso' in b.get('type', '').lower() 
                  or 'potencia' in b.get('category', '').lower()]
    
    if not boilers:
        return {
            'model': 'Caldera genérica',
            'description': f'Caldera {boiler_type} de {power_required_w:.0f}W requerida',
            'url': '',
            'family': 'Calderas'
        }
    
    # Convertir potencia a kcal/h para referencia
    power_kcal = power_required_w * 0.859845
    
    # Priorizar calderas según características:
    # 1. Calderas doble servicio (más versátiles)
    # 2. Calderas con tecnología inteligente (Prima Tec Smart)
    # 3. Calderas económicas (Diva)
    def get_priority(boiler):
        desc = boiler.get('description', '').lower()
        model = boiler.get('model', '').lower()
        
        # Prioridad 1: Doble servicio con wifi
        if 'doble servicio' in desc and ('wifi' in desc or 'smart' in model):
            return 1
        # Prioridad 2: Doble servicio
        elif 'doble servicio' in desc:
            return 2
        # Prioridad 3: Otras calderas
        else:
            return 3
    
    boilers_sorted = sorted(boilers, key=get_priority)
    recommended = boilers_sorted[0]
    
    # Agregar información de potencia calculada al resultado
    recommended['power_required_w'] = power_required_w
    recommended['power_required_kcal'] = power_kcal
    
    return recommended


def recommend_floor_heating_kit(surface_m2: float, zona_geografica: str = 'norte',
                               catalog: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """
    Recomienda productos para piso radiante según la superficie y zona.
    Usa products_catalog.json como fuente de datos.
    
    Args:
        surface_m2: Superficie en metros cuadrados
        zona_geografica: Zona del país ('norte' o 'sur')
        catalog: Catálogo de productos
        
    Returns:
        Diccionario con los productos recomendados para piso radiante
    """
    if catalog is None:
        catalog = load_product_catalog()
    
    # Calcular potencia necesaria según zona (de peisa_advisor_knowledge_base.json)
    potencia_m2 = {'norte': 100, 'sur': 125}
    power_required_w = surface_m2 * potencia_m2.get(zona_geografica, 100)
    
    # Buscar calderas adecuadas para piso radiante (doble servicio)
    calderas = [p for p in catalog 
                if p.get('family') == 'Calderas' 
                and 'doble servicio' in p.get('description', '').lower()]
    
    # Buscar productos relacionados con piso radiante
    piso_radiante_products = [p for p in catalog 
                             if 'piso radiante' in p.get('description', '').lower() 
                             or 'piso radiante' in p.get('model', '').lower()]
    
    # Si hay calderas, recomendar la mejor para piso radiante
    if calderas:
        # Priorizar calderas con wifi/smart
        calderas_sorted = sorted(calderas, 
                                key=lambda x: ('wifi' in x.get('description', '').lower() or 
                                             'smart' in x.get('model', '').lower()),
                                reverse=True)
        
        recommended_caldera = calderas_sorted[0]
        recommended_caldera['power_required_w'] = power_required_w
        recommended_caldera['power_required_kcal'] = power_required_w * 0.859845
        recommended_caldera['surface_m2'] = surface_m2
        recommended_caldera['zona_geografica'] = zona_geografica
        
        return recommended_caldera
    
    # Si no hay calderas específicas, retornar el primer producto relacionado
    if piso_radiante_products:
        recommended = piso_radiante_products[0]
        recommended['power_required_w'] = power_required_w
        recommended['power_required_kcal'] = power_required_w * 0.859845
        recommended['surface_m2'] = surface_m2
        recommended['zona_geografica'] = zona_geografica
        return recommended
    
    # Si no hay productos, retornar información genérica
    return {
        'model': f'Sistema Piso Radiante {surface_m2:.0f}m²',
        'description': f'Sistema completo para {surface_m2:.0f}m² en zona {zona_geografica}',
        'family': 'Piso Radiante',
        'power_required_w': power_required_w,
        'power_required_kcal': power_required_w * 0.859845,
        'surface_m2': surface_m2,
        'zona_geografica': zona_geografica
    }


def recommend_radiator_from_catalog(power_required_w: float,
                                   catalog: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """
    Recomienda UN SOLO radiador del catálogo según la potencia requerida.
    Usa products_catalog.json como fuente de datos.
    
    Args:
        power_required_w: Potencia requerida en Watts
        catalog: Catálogo de productos
        
    Returns:
        UN radiador recomendado del catálogo (el más adecuado)
    """
    if catalog is None:
        catalog = load_product_catalog()
    
    # Filtrar radiadores del catálogo (excluyendo toalleros)
    radiators = [
        p for p in catalog 
        if p.get('family') == 'Radiadores' 
        and p.get('category') == 'Radiadores'  # Excluye toalleros
        and 'toallero' not in p.get('model', '').lower()
    ]
    
    if not radiators:
        return {
            'model': 'Radiador genérico',
            'description': f'Radiador para {power_required_w:.0f}W',
            'family': 'Radiadores'
        }
    
    # Convertir potencia a kcal/h para referencia
    power_kcal = power_required_w * 0.859845
    
    # Priorizar según potencia requerida
    if power_kcal < 2000:
        # Para potencias bajas: priorizar radiadores eléctricos
        electric_rads = [r for r in radiators 
                        if 'eléctrico' in r.get('model', '').lower() 
                        or 'electrico' in r.get('model', '').lower()
                        or 'electric' in r.get('type', '').lower()]
        if electric_rads:
            # Retornar el PRIMER radiador eléctrico (el más adecuado)
            recommended = electric_rads[0]
            recommended['power_required_w'] = power_required_w
            recommended['power_required_kcal'] = power_kcal
            return recommended
    
    # Para potencias mayores: ordenar por popularidad y características
    # Prioridad: Broen, Tropical, Gamma, BR (modelos conocidos de PEISA)
    priority_models = ['Broen', 'Tropical', 'Gamma', 'BR', 'Radiador']
    
    def get_priority(rad):
        model = rad.get('model', '')
        desc = rad.get('description', '')
        
        # Buscar en modelo y descripción
        for i, priority in enumerate(priority_models):
            if priority.lower() in model.lower() or priority.lower() in desc.lower():
                return i
        return len(priority_models)
    
    radiators_sorted = sorted(radiators, key=get_priority)
    
    # Retornar EL MEJOR radiador (el primero de la lista ordenada)
    recommended = radiators_sorted[0]
    recommended['power_required_w'] = power_required_w
    recommended['power_required_kcal'] = power_kcal
    
    return recommended


def recommend_towel_rack_from_catalog(catalog: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """
    Recomienda UN toallero del catálogo.
    Usa products_catalog.json como fuente de datos.
    
    Args:
        catalog: Catálogo de productos
        
    Returns:
        UN toallero recomendado del catálogo
    """
    if catalog is None:
        catalog = load_product_catalog()
    
    # Filtrar toalleros del catálogo
    towel_racks = [
        p for p in catalog 
        if p.get('category') == 'Toalleros'
        or 'toallero' in p.get('model', '').lower()
        or 'toallero' in p.get('type', '').lower()
    ]
    
    if not towel_racks:
        return {
            'model': 'Toallero PEISA',
            'description': 'Toallero para baño',
            'family': 'Radiadores',
            'category': 'Toalleros'
        }
    
    # Priorizar toalleros eléctricos (más versátiles)
    electric_towel_racks = [
        t for t in towel_racks
        if 'eléctrico' in t.get('model', '').lower()
        or 'electric' in t.get('type', '').lower()
    ]
    
    if electric_towel_racks:
        return electric_towel_racks[0]
    
    # Si no hay eléctricos, retornar el primero
    return towel_racks[0]


def format_towel_rack_recommendation(model: Dict[str, Any]) -> str:
    """
    Formatea la recomendación de UN toallero para mostrarlo al usuario.
    
    Args:
        model: Modelo de toallero recomendado
        
    Returns:
        Texto formateado con la recomendación
    """
    if not model or not isinstance(model, dict):
        return "No encontramos un toallero que coincida con tus requisitos."
    
    try:
        model_name = model.get('model', 'Toallero PEISA')
        description = model.get('description', 'Sin descripción disponible')
        url = model.get('url', '')
        
        result = [
            f"✅ TOALLERO RECOMENDADO: {model_name}",
            f"",
            f"📋 Descripción:",
            f"{description}",
        ]
        
        # Agregar características técnicas si existen
        if 'technical_features' in model and model['technical_features']:
            result.append("")
            result.append("🔧 Características técnicas:")
            for feature in model['technical_features'][:3]:
                result.append(f"  • {feature}")
        
        # Agregar ventajas si existen
        if 'advantages' in model and model['advantages']:
            result.append("")
            result.append("✨ Ventajas:")
            for advantage in model['advantages'][:2]:
                result.append(f"  • {advantage}")
        
        if url:
            result.append("")
            result.append(f"🔗 Más información: {url}")
        
        return "\n".join(result)
        
    except Exception as e:
        print(f"Error formateando toallero {model}: {e}")
        return f"Recomendación: {model.get('model', 'Toallero PEISA')}"
