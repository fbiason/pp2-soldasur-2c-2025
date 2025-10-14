"""
rag_engine.py - Motor RAG con Conciencia de Contexto Experto

Este módulo contiene el motor RAG (Retrieval-Augmented Generation)
con capacidad de usar el contexto del sistema experto para mejorar respuestas.
"""

"""from typing import Dict, Any, List, Optional
import sys
from pathlib import Path
"""

# Importar módulos existentes
sys.path.append(str(Path(__file__).parent.parent))
from query import query
from app.llm_wrapper import answer as llm_answer


class RAGEngine:
    """
    Motor RAG con capacidad de usar el contexto del sistema experto.
    Combina búsqueda vectorial con generación de lenguaje natural.
    """
    
    def __init__(self):
        """Inicializa el motor RAG"""
        self.expert_engine = None  # Se inyectará después
        self.default_top_k = 5
    
    def set_expert_engine(self, expert_engine):
        """Inyecta el motor experto para enriquecimiento mutuo"""
        self.expert_engine = expert_engine
    
    async def query(self, question: str, expert_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Procesa una consulta del usuario usando RAG.
        
        Args:
            question: Pregunta del usuario
            expert_context: Contexto del sistema experto (opcional)
            
        Returns:
            Diccionario con la respuesta y metadatos
        """
        # Búsqueda vectorial en el catálogo
        relevant_products = self._search_products(question, self.default_top_k)
        
        # Filtrar productos según el contexto del experto si existe
        if expert_context:
            relevant_products = self._filter_by_context(relevant_products, expert_context)
        
        # Construir prompt contextual
        if expert_context:
            prompt = self._build_contextual_prompt(question, relevant_products, expert_context)
        else:
            prompt = question
        
        # Generar respuesta con LLM
        try:
            answer = llm_answer(prompt, relevant_products)
        except Exception as e:
            print(f"Error generando respuesta con LLM: {e}")
            answer = self._fallback_answer(question, relevant_products)
        
        # Sugerir flujo guiado si es relevante
        expert_suggestion = None
        if self._should_suggest_expert_flow(question, expert_context):
            expert_suggestion = await self._get_expert_suggestion(expert_context)
        
        return {
            'answer': answer,
            'products': relevant_products,
            'sources': [p['model'] for p in relevant_products[:3]],
            'expert_suggestion': expert_suggestion,
            'context_used': expert_context is not None
        }
    
    async def search_products(self, query_text: str, top_k: int = 5) -> Dict[str, Any]:
        """
        Búsqueda específica de productos.
        
        Args:
            query_text: Texto de búsqueda
            top_k: Número de resultados
            
        Returns:
            Diccionario con productos encontrados
        """
        products = self._search_products(query_text, top_k)
        
        return {
            'type': 'product_search',
            'products': products,
            'count': len(products),
            'answer': self._format_product_results(products)
        }
    
    async def get_context(self, query: str, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Obtiene contexto relevante para enriquecer el sistema experto.
        
        Args:
            query: Query para buscar contexto
            filters: Filtros adicionales
            
        Returns:
            Diccionario con contexto relevante
        """
        # Buscar información relevante
        products = self._search_products(query, top_k=3)
        
        # Aplicar filtros si existen
        if filters:
            products = [p for p in products if self._matches_filters(p, filters)]
        
        # Generar resumen del contexto
        summary = self._generate_context_summary(products, query)
        
        return {
            'summary': summary,
            'products': products,
            'query': query
        }
    
    def _search_products(self, query_text: str, top_k: int) -> List[Dict[str, Any]]:
        """
        Realiza búsqueda vectorial en el catálogo de productos.
        
        Args:
            query_text: Texto de búsqueda
            top_k: Número de resultados
            
        Returns:
            Lista de productos relevantes
        """
        try:
            # Usar el módulo query existente
            results = query.search_filtered(query_text, top_k=top_k)
            return results
        except Exception as e:
            print(f"Error en búsqueda de productos: {e}")
            return []
    
    def _filter_by_context(self, products: List[Dict[str, Any]], 
                          context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Filtra productos según el contexto del experto.
        
        Args:
            products: Lista de productos
            context: Contexto del experto
            
        Returns:
            Lista filtrada de productos
        """
        filtered = products.copy()
        
        # Filtrar por potencia si está en el contexto
        if 'carga_termica' in context:
            required_power = context['carga_termica']
            # Filtrar productos con potencia adecuada (±20%)
            filtered = [
                p for p in filtered 
                if p.get('power_w') and 
                   0.8 * required_power <= p['power_w'] <= 1.5 * required_power
            ]
        
        # Filtrar por tipo si está en el contexto
        if 'tipo_calefaccion' in context or 'inicio' in context:
            tipo = context.get('tipo_calefaccion') or context.get('inicio')
            if tipo and 'caldera' in str(tipo).lower():
                filtered = [p for p in filtered if 'caldera' in p.get('type', '').lower()]
            elif tipo and 'radiador' in str(tipo).lower():
                filtered = [p for p in filtered if 'radiador' in p.get('type', '').lower()]
        
        # Si el filtrado elimina todos los productos, devolver los originales
        return filtered if filtered else products
    
    def _build_contextual_prompt(self, question: str, products: List[Dict[str, Any]], 
                                context: Dict[str, Any]) -> str:
        """
        Construye un prompt enriquecido con el contexto del experto.
        
        Args:
            question: Pregunta del usuario
            products: Productos relevantes
            context: Contexto del experto
            
        Returns:
            Prompt enriquecido
        """
        # Extraer información relevante del contexto
        context_info = []
        
        if 'superficie' in context:
            context_info.append(f"Superficie a calefaccionar: {context['superficie']} m²")
        
        if 'zona' in context or 'ubicacion' in context:
            zona = context.get('zona') or context.get('ubicacion')
            context_info.append(f"Ubicación: {zona}")
        
        if 'carga_termica' in context:
            context_info.append(f"Carga térmica calculada: {context['carga_termica']} kcal/h")
        
        if 'tipo_calefaccion' in context or 'inicio' in context:
            tipo = context.get('tipo_calefaccion') or context.get('inicio')
            context_info.append(f"Tipo de calefacción: {tipo}")
        
        # Construir prompt
        if context_info:
            context_str = "\n".join(context_info)
            prompt = f"{question}\n\nContexto adicional:\n{context_str}"
        else:
            prompt = question
        
        return prompt
    
    def _matches_filters(self, product: Dict[str, Any], 
                        filters: Dict[str, Any]) -> bool:
        """Verifica si un producto coincide con los filtros"""
        for key, value in filters.items():
            if key in product:
                if isinstance(value, list):
                    if product[key] not in value:
                        return False
                elif product[key] != value:
                    return False
        return True
    
    def _generate_context_summary(self, products: List[Dict[str, Any]], 
                                 query: str) -> str:
        """
        Genera un resumen del contexto para enriquecer el experto.
        
        Args:
            products: Productos relevantes
            query: Query original
            
        Returns:
            Resumen textual
        """
        if not products:
            return "No se encontró información adicional relevante."
        
        # Generar resumen básico
        summary_parts = []
        
        # Información sobre tipos de productos encontrados
        types = set(p.get('type', 'Desconocido') for p in products)
        if types:
            summary_parts.append(f"Tipos disponibles: {', '.join(types)}")
        
        # Rango de potencias
        powers = [p.get('power_w', 0) for p in products if p.get('power_w')]
        if powers:
            min_power = min(powers)
            max_power = max(powers)
            summary_parts.append(f"Rango de potencias: {min_power}-{max_power} W")
        
        # Modelos destacados
        if len(products) > 0:
            top_model = products[0]
            summary_parts.append(
                f"Modelo destacado: {top_model.get('model', 'N/A')} "
                f"({top_model.get('family', 'N/A')})"
            )
        
        return " | ".join(summary_parts)
    
    def _format_product_results(self, products: List[Dict[str, Any]]) -> str:
        """
        Formatea los resultados de productos para mostrar al usuario.
        
        Args:
            products: Lista de productos
            
        Returns:
            Texto formateado
        """
        if not products:
            return "No se encontraron productos que coincidan con tu búsqueda."
        
        result_lines = [f"Encontré {len(products)} producto(s) relevante(s):\n"]
        
        for i, product in enumerate(products, 1):
            lines = [
                f"{i}. **{product.get('model', 'N/A')}** ({product.get('family', 'N/A')})",
                f"   - Tipo: {product.get('type', 'N/A')}",
            ]
            
            if product.get('power_w'):
                lines.append(f"   - Potencia: {product['power_w']} W")
            
            if product.get('description'):
                desc = product['description'][:100] + "..." if len(product['description']) > 100 else product['description']
                lines.append(f"   - Descripción: {desc}")
            
            result_lines.append("\n".join(lines))
        
        return "\n\n".join(result_lines)
    
    def _fallback_answer(self, question: str, products: List[Dict[str, Any]]) -> str:
        """
        Genera una respuesta de fallback si el LLM falla.
        
        Args:
            question: Pregunta del usuario
            products: Productos relevantes
            
        Returns:
            Respuesta de fallback
        """
        if not products:
            return "No encontré información específica sobre tu consulta. ¿Podrías reformular la pregunta?"
        
        return self._format_product_results(products)
    
    def _should_suggest_expert_flow(self, question: str, 
                                   context: Optional[Dict[str, Any]]) -> bool:
        """
        Determina si se debe sugerir un flujo guiado del experto.
        
        Args:
            question: Pregunta del usuario
            context: Contexto actual
            
        Returns:
            True si se debe sugerir flujo guiado
        """
        # Palabras clave que indican necesidad de cálculo
        calculation_keywords = [
            'calcular', 'dimensionar', 'cuántos', 'necesito',
            'requiero', 'instalar', 'proyecto'
        ]
        
        question_lower = question.lower()
        has_calculation_intent = any(kw in question_lower for kw in calculation_keywords)
        
        # Si ya está en un flujo experto, no sugerir
        if context and context.get('current_node') != 'inicio':
            return False
        
        return has_calculation_intent
    
    async def _get_expert_suggestion(self, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Obtiene una sugerencia del sistema experto.
        
        Args:
            context: Contexto actual
            
        Returns:
            Sugerencia del experto
        """
        if not self.expert_engine:
            return {
                'message': '¿Quieres que te guíe paso a paso en el cálculo?',
                'action': 'start_expert_flow'
            }
        
        # Obtener sugerencia del experto
        try:
            suggestion = await self.expert_engine.suggest_next_step(context or {})
            return {
                'message': suggestion.get('suggestion', '¿Quieres que te guíe en el cálculo?'),
                'action': 'start_expert_flow',
                'options': suggestion.get('options', [])
            }
        except Exception as e:
            print(f"Error obteniendo sugerencia del experto: {e}")
            return {
                'message': '¿Quieres que te guíe paso a paso en el cálculo?',
                'action': 'start_expert_flow'
            }
