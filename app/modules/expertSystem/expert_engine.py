"""
expert_engine.py - Motor del Sistema Experto con Enriquecimiento RAG

Este módulo contiene el motor del sistema experto basado en reglas,
con capacidad de enriquecimiento mediante el sistema RAG.
"""

from typing import Dict, Any, List, Optional
import json
from math import ceil
from bisect import bisect_left
from pathlib import Path
from .models import RADIATOR_MODELS
from .product_loader import get_product_loader


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
            if next_node_id:
                expert_state['current_node'] = next_node_id
                node = self.get_node_by_id(next_node_id)
        
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
                # Guardar el valor usando el ID del nodo como clave
                context[node['id']] = selected.get('valor', selected['texto'])
                # Guardar también el texto para mostrar
                context[f"{node['id']}_texto"] = selected['texto']
                
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
        
        # Nodo de cálculo: ejecutar y avanzar automáticamente
        if node.get('tipo') == 'calculo':
            self._perform_calculation(node, context)
            expert_state['current_node'] = node['siguiente']
            next_node = self.get_node_by_id(node['siguiente'])
            return await self._get_node_message(next_node, context, expert_state)
        
        # Nodo con pregunta
        elif 'pregunta' in node:
            response = {
                'type': 'question',
                'node_id': node['id'],
                'text': self._replace_variables(node['pregunta'], context),
                'variables': context
            }
            
            # Agregar opciones si existen
            if 'opciones' in node:
                response['options'] = [opt['texto'] for opt in node['opciones']]
            
            # Nodo de entrada de usuario
            elif node.get('tipo') == 'entrada_usuario':
                if 'variable' in node:
                    response['input_type'] = 'number'
                    response['input_label'] = 'Ingrese el valor'
                elif 'variables' in node:
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
            response = {
                'type': 'response',
                'node_id': node['id'],
                'text': self._replace_variables(node['texto'], context),
                'variables': context
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
                    color: str, heat_load: float) -> List[Dict[str, Any]]:
    """
    Filtra radiadores según las preferencias del usuario.
    Usa el cargador dinámico de productos desde Excel.
    
    Args:
        radiator_type: Tipo de radiador
        installation: Tipo de instalación
        style: Estilo del radiador
        color: Color preferido
        heat_load: Carga térmica requerida
        
    Returns:
        Lista de radiadores recomendados
    """
    loader = get_product_loader()
    radiators = loader.filter_radiators_by_criteria(
        radiator_type=radiator_type,
        installation=installation,
        style=style,
        color=color,
        heat_load=heat_load
    )
    
    # Formatear para compatibilidad con código existente
    recommended = []
    for rad in radiators:
        recommended.append({
            'name': rad['name'],
            'description': rad['description'],
            'coeficiente': rad.get('coeficiente', 1.0),
            'potencia': rad['potencia'],
            'colors': rad['colors']
        })
    
    return recommended[:3]  # Top 3 recomendaciones


def format_radiator_recommendations(models: List[Dict[str, Any]], 
                                   heat_load: float) -> str:
    """
    Formatea las recomendaciones de radiadores para mostrarlas al usuario.
    
    Args:
        models: Lista de modelos recomendados
        heat_load: Carga térmica requerida
        
    Returns:
        Texto formateado con las recomendaciones
    """
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


def load_product_catalog(catalog_path: str = "data/products_catalog.json") -> List[Dict[str, Any]]:
    """
    Carga el catálogo de productos dinámicamente desde Excel.
    El parámetro catalog_path se mantiene por compatibilidad pero no se usa.
    
    Args:
        catalog_path: Ruta al archivo del catálogo (no usado, por compatibilidad)
        
    Returns:
        Lista de productos cargados desde Excel
    """
    loader = get_product_loader()
    return loader.get_all_products()


def recommend_boiler(power_required_w: float, boiler_type: str, 
                    catalog: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """
    Recomienda una caldera específica del catálogo según la potencia requerida.
    
    Args:
        power_required_w: Potencia requerida en Watts
        boiler_type: Tipo de caldera ('mural' o 'piso')
        catalog: Catálogo de productos (se carga automáticamente si no se provee)
        
    Returns:
        Diccionario con la caldera recomendada
    """
    if catalog is None:
        catalog = load_product_catalog()
    
    # Filtrar calderas del catálogo
    boilers = [p for p in catalog if p.get('family') == 'Calderas']
    
    # Filtrar por tipo si se especifica
    type_map = {'mural': 'Caldera mural', 'piso': 'Caldera de piso'}
    if boiler_type in type_map:
        boilers = [b for b in boilers if b.get('type') == type_map[boiler_type]]
    
    if not boilers:
        return {
            'model': 'Caldera genérica',
            'power_w': power_required_w,
            'description': f'Caldera {boiler_type} de {power_required_w:.0f}W requerida'
        }
    
    # Encontrar la caldera con potencia más cercana (pero suficiente)
    suitable_boilers = [b for b in boilers if b.get('power_w', 0) >= power_required_w]
    
    if suitable_boilers:
        # Elegir la de menor potencia que cumpla el requisito
        recommended = min(suitable_boilers, key=lambda x: x.get('power_w', float('inf')))
    else:
        # Si ninguna cumple, elegir la de mayor potencia disponible
        recommended = max(boilers, key=lambda x: x.get('power_w', 0))
    
    return recommended


def recommend_floor_heating_kit(surface_m2: float, 
                               catalog: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """
    Recomienda un kit de piso radiante según la superficie.
    
    Args:
        surface_m2: Superficie en metros cuadrados
        catalog: Catálogo de productos
        
    Returns:
        Diccionario con el kit recomendado
    """
    if catalog is None:
        catalog = load_product_catalog()
    
    # Filtrar kits de piso radiante
    kits = [p for p in catalog if p.get('family') == 'Piso Radiante' and 'KIT' in p.get('model', '')]
    
    if not kits:
        return {
            'model': f'Kit Piso Radiante {surface_m2:.0f}m²',
            'description': f'Kit completo para {surface_m2:.0f}m²'
        }
    
    # Extraer superficie de cada kit (del campo dimentions o model)
    for kit in kits:
        model_name = kit.get('model', '')
        if 'KIT' in model_name and 'm²' in model_name:
            try:
                # Extraer número de m² del nombre (ej: "PEISA PISO RADIANTE KIT 15m²")
                surface_str = model_name.split('KIT')[1].strip().replace('m²', '')
                kit['surface_m2'] = float(surface_str)
            except:
                kit['surface_m2'] = 0
    
    # Encontrar el kit más adecuado
    suitable_kits = [k for k in kits if k.get('surface_m2', 0) >= surface_m2]
    
    if suitable_kits:
        recommended = min(suitable_kits, key=lambda x: x.get('surface_m2', float('inf')))
    else:
        # Si la superficie es mayor que todos los kits, recomendar el más grande
        recommended = max(kits, key=lambda x: x.get('surface_m2', 0))
        # Calcular cuántos kits se necesitan
        kits_needed = ceil(surface_m2 / recommended.get('surface_m2', 1))
        recommended['kits_needed'] = kits_needed
    
    return recommended


def recommend_radiator_from_catalog(power_required_w: float,
                                   catalog: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
    """
    Recomienda radiadores del catálogo según la potencia requerida.
    
    Args:
        power_required_w: Potencia requerida en Watts
        catalog: Catálogo de productos
        
    Returns:
        Lista de radiadores recomendados
    """
    if catalog is None:
        catalog = load_product_catalog()
    
    # Filtrar radiadores del catálogo (excluyendo toalleros)
    radiators = [
        p for p in catalog 
        if p.get('family') == 'Radiadores' 
        and 'toallero' not in p.get('type', '').lower()
        and 'TOALLERO' not in p.get('model', '')
    ]
    
    if not radiators:
        return []
    
    # Ordenar por cercanía a la potencia requerida
    for rad in radiators:
        rad['power_diff'] = abs(rad.get('power_w', 0) - power_required_w)
    
    radiators.sort(key=lambda x: x['power_diff'])
    
    # Retornar top 3
    return radiators[:3]
