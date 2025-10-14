"""
orchestrator.py - Orquestador Inteligente para Sistema Híbrido

Este módulo coordina la interacción entre el sistema experto (basado en reglas)
y el sistema RAG (búsqueda semántica + LLM generativo), proporcionando una
experiencia unificada al usuario.
"""

from typing import Dict, Any, Optional, List
from enum import Enum
import re


class IntentType(Enum):
    """Tipos de intención del usuario"""
    GUIDED_CALCULATION = "guided_calculation"  # Flujo guiado paso a paso
    FREE_QUERY = "free_query"                  # Pregunta abierta
    PRODUCT_SEARCH = "product_search"          # Búsqueda de productos
    HYBRID = "hybrid"                          # Combinación de ambos
    SWITCH_MODE = "switch_mode"                # Cambio de modo
    CLARIFICATION = "clarification"            # Pregunta tangencial durante flujo


class ConversationMode(Enum):
    """Modos de conversación"""
    EXPERT = "expert"      # Modo experto guiado
    RAG = "rag"           # Modo chat libre
    HYBRID = "hybrid"     # Modo híbrido automático


class Intent:
    """Representa la intención clasificada del usuario"""
    def __init__(self, intent_type: IntentType, confidence: float = 1.0, 
                 metadata: Optional[Dict[str, Any]] = None):
        self.type = intent_type
        self.confidence = confidence
        self.metadata = metadata or {}


class IntentClassifier:
    """
    Clasifica la intención del usuario para enrutar correctamente
    entre el sistema experto y el RAG.
    """
    
    # Patrones para clasificación basada en reglas
    PATTERNS = {
        IntentType.GUIDED_CALCULATION: [
            r"quiero calcular",
            r"necesito dimensionar",
            r"cuántos radiadores",
            r"piso radiante",
            r"ayúdame a calcular",
            r"guíame",
            r"paso a paso",
        ],
        IntentType.FREE_QUERY: [
            r"qué es",
            r"cómo funciona",
            r"diferencia entre",
            r"explica",
            r"cuál es mejor",
            r"ventajas",
            r"desventajas",
        ],
        IntentType.PRODUCT_SEARCH: [
            r"precio",
            r"modelo",
            r"disponibilidad",
            r"características",
            r"catálogo",
            r"tienen.*\?",
            r"busco",
        ],
        IntentType.SWITCH_MODE: [
            r"prefiero que me guíes",
            r"quiero preguntar libremente",
            r"modo experto",
            r"modo chat",
            r"cambiar modo",
        ],
        IntentType.CLARIFICATION: [
            r"qué significa",
            r"no entiendo",
            r"explícame",
            r"qué quiere decir",
        ]
    }
    
    def classify(self, message: str, context: Dict[str, Any]) -> Intent:
        """
        Clasifica la intención del usuario basándose en el mensaje y el contexto.
        
        Args:
            message: Mensaje del usuario
            context: Contexto de la conversación
            
        Returns:
            Intent: Intención clasificada con confianza
        """
        message_lower = message.lower().strip()
        
        # Si está en medio de un flujo guiado y hace una pregunta tangencial
        if context.get('mode') == ConversationMode.EXPERT.value:
            if self._matches_patterns(message_lower, IntentType.CLARIFICATION):
                return Intent(IntentType.CLARIFICATION, confidence=0.9)
            # Si responde con un número o selección, continuar flujo experto
            if message_lower.isdigit() or self._is_numeric_input(message):
                return Intent(IntentType.GUIDED_CALCULATION, confidence=1.0)
        
        # Detectar cambio de modo explícito
        if self._matches_patterns(message_lower, IntentType.SWITCH_MODE):
            target_mode = self._extract_target_mode(message_lower)
            return Intent(IntentType.SWITCH_MODE, confidence=0.95, 
                         metadata={'target_mode': target_mode})
        
        # Detectar búsqueda de productos
        if self._matches_patterns(message_lower, IntentType.PRODUCT_SEARCH):
            return Intent(IntentType.PRODUCT_SEARCH, confidence=0.85)
        
        # Detectar solicitud de cálculo guiado
        if self._matches_patterns(message_lower, IntentType.GUIDED_CALCULATION):
            return Intent(IntentType.GUIDED_CALCULATION, confidence=0.9)
        
        # Detectar pregunta abierta
        if self._matches_patterns(message_lower, IntentType.FREE_QUERY):
            return Intent(IntentType.FREE_QUERY, confidence=0.85)
        
        # Detectar modo híbrido (tiene datos específicos pero es abierto)
        if self._has_specific_data(message_lower):
            return Intent(IntentType.HYBRID, confidence=0.75)
        
        # Por defecto, usar modo híbrido
        return Intent(IntentType.HYBRID, confidence=0.5)
    
    def _matches_patterns(self, message: str, intent_type: IntentType) -> bool:
        """Verifica si el mensaje coincide con algún patrón del tipo de intención"""
        patterns = self.PATTERNS.get(intent_type, [])
        return any(re.search(pattern, message) for pattern in patterns)
    
    def _is_numeric_input(self, message: str) -> bool:
        """Verifica si el mensaje es una entrada numérica"""
        try:
            float(message.replace(',', '.'))
            return True
        except ValueError:
            return False
    
    def _extract_target_mode(self, message: str) -> str:
        """Extrae el modo objetivo de un mensaje de cambio de modo"""
        if any(word in message for word in ['guíes', 'experto', 'paso a paso']):
            return ConversationMode.EXPERT.value
        elif any(word in message for word in ['libremente', 'chat', 'preguntar']):
            return ConversationMode.RAG.value
        return ConversationMode.HYBRID.value
    
    def _has_specific_data(self, message: str) -> bool:
        """Detecta si el mensaje contiene datos específicos (números, ubicaciones, etc.)"""
        # Buscar números (ej: "50m²", "100 watts")
        has_numbers = bool(re.search(r'\d+', message))
        # Buscar ubicaciones conocidas
        locations = ['ushuaia', 'buenos aires', 'córdoba', 'mendoza', 'norte', 'sur']
        has_location = any(loc in message for loc in locations)
        return has_numbers or has_location


class UnifiedContext:
    """
    Contexto unificado que mantiene el estado de la conversación
    a través de ambos sistemas (experto y RAG).
    """
    def __init__(self, conversation_id: str):
        self.conversation_id = conversation_id
        self.mode = ConversationMode.HYBRID.value
        self.expert_state = {
            'current_node': 'inicio',
            'variables': {},
            'history': []
        }
        self.rag_history = []
        self.user_preferences = {}
        self.session_metadata = {
            'started_at': None,
            'last_interaction': None,
            'interaction_count': 0
        }
        self.paused_expert_node = None  # Para pausar y reanudar flujo experto
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el contexto a diccionario"""
        return {
            'conversation_id': self.conversation_id,
            'mode': self.mode,
            'expert_state': self.expert_state,
            'rag_history': self.rag_history,
            'user_preferences': self.user_preferences,
            'session_metadata': self.session_metadata,
            'paused_expert_node': self.paused_expert_node
        }
    
    def update_expert_state(self, node_id: str, variables: Dict[str, Any]):
        """Actualiza el estado del sistema experto"""
        self.expert_state['current_node'] = node_id
        self.expert_state['variables'].update(variables)
        self.expert_state['history'].append({
            'node': node_id,
            'variables': variables.copy()
        })
    
    def add_rag_interaction(self, query: str, response: str):
        """Registra una interacción con el sistema RAG"""
        self.rag_history.append({
            'query': query,
            'response': response
        })


class ConversationOrchestrator:
    """
    Orquesta la interacción entre el sistema experto y el RAG,
    proporcionando una experiencia unificada.
    """
    
    def __init__(self, expert_engine, rag_engine):
        """
        Args:
            expert_engine: Instancia del motor experto
            rag_engine: Instancia del motor RAG
        """
        self.expert_engine = expert_engine
        self.rag_engine = rag_engine
        self.intent_classifier = IntentClassifier()
        self.contexts: Dict[str, UnifiedContext] = {}
    
    def get_or_create_context(self, conversation_id: str) -> UnifiedContext:
        """Obtiene o crea un contexto unificado para la conversación"""
        if conversation_id not in self.contexts:
            self.contexts[conversation_id] = UnifiedContext(conversation_id)
        return self.contexts[conversation_id]
    
    async def process_message(self, conversation_id: str, message: str, 
                             option_index: Optional[int] = None,
                             input_values: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Procesa un mensaje del usuario y decide qué motor usar.
        
        Args:
            conversation_id: ID de la conversación
            message: Mensaje del usuario
            option_index: Índice de opción seleccionada (para flujo experto)
            input_values: Valores de entrada (para flujo experto)
            
        Returns:
            Dict con la respuesta y metadatos
        """
        context = self.get_or_create_context(conversation_id)
        context.session_metadata['interaction_count'] += 1
        
        # Clasificar intención
        intent = self.intent_classifier.classify(message, context.to_dict())
        
        # Enrutar según intención
        if intent.type == IntentType.GUIDED_CALCULATION:
            # Usuario quiere un flujo guiado
            result = await self._handle_expert_flow(
                conversation_id, message, option_index, input_values
            )
            context.mode = ConversationMode.EXPERT.value
            return result
        
        elif intent.type == IntentType.FREE_QUERY:
            # Usuario hace una pregunta abierta
            result = await self._handle_rag_query(conversation_id, message)
            context.mode = ConversationMode.RAG.value
            return result
        
        elif intent.type == IntentType.PRODUCT_SEARCH:
            # Búsqueda de productos
            result = await self._handle_product_search(conversation_id, message)
            return result
        
        elif intent.type == IntentType.CLARIFICATION:
            # Pregunta tangencial durante flujo guiado
            result = await self._handle_clarification(conversation_id, message)
            return result
        
        elif intent.type == IntentType.SWITCH_MODE:
            # Cambio de modo
            target_mode = intent.metadata.get('target_mode', ConversationMode.HYBRID.value)
            result = await self._handle_mode_switch(conversation_id, target_mode)
            return result
        
        elif intent.type == IntentType.HYBRID:
            # Modo híbrido: combinar ambos sistemas
            result = await self._handle_hybrid_mode(conversation_id, message)
            context.mode = ConversationMode.HYBRID.value
            return result
        
        # Fallback
        return await self._handle_hybrid_mode(conversation_id, message)
    
    async def _handle_expert_flow(self, conversation_id: str, message: str,
                                  option_index: Optional[int] = None,
                                  input_values: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Maneja el flujo del sistema experto"""
        context = self.get_or_create_context(conversation_id)
        
        # Procesar con el motor experto
        result = await self.expert_engine.process(
            conversation_id, 
            context.expert_state,
            option_index,
            input_values
        )
        
        # Actualizar contexto
        if 'node_id' in result:
            context.update_expert_state(result['node_id'], result.get('variables', {}))
        
        # Agregar metadatos de modo
        result['mode'] = ConversationMode.EXPERT.value
        result['mode_label'] = '🤖 Modo Experto'
        
        return result
    
    async def _handle_rag_query(self, conversation_id: str, message: str) -> Dict[str, Any]:
        """Maneja una consulta al sistema RAG"""
        context = self.get_or_create_context(conversation_id)
        
        # Obtener contexto del experto si existe
        expert_context = context.expert_state.get('variables', {})
        
        # Consultar al RAG con contexto
        result = await self.rag_engine.query(message, expert_context)
        
        # Registrar interacción
        context.add_rag_interaction(message, result.get('answer', ''))
        
        # Agregar sugerencia de flujo guiado si es relevante
        if self._should_suggest_guided_flow(message):
            result['suggestion'] = {
                'type': 'switch_to_expert',
                'message': '💡 ¿Quieres que te guíe en un cálculo preciso paso a paso?'
            }
        
        # Agregar metadatos de modo
        result['mode'] = ConversationMode.RAG.value
        result['mode_label'] = '💬 Modo Chat'
        
        return result
    
    async def _handle_product_search(self, conversation_id: str, message: str) -> Dict[str, Any]:
        """Maneja búsqueda de productos"""
        # Usar el RAG para búsqueda de productos
        result = await self.rag_engine.search_products(message)
        result['mode'] = ConversationMode.RAG.value
        result['mode_label'] = '🔍 Búsqueda de Productos'
        return result
    
    async def _handle_clarification(self, conversation_id: str, message: str) -> Dict[str, Any]:
        """Maneja pregunta tangencial durante flujo guiado"""
        context = self.get_or_create_context(conversation_id)
        
        # Pausar el flujo experto
        context.paused_expert_node = context.expert_state['current_node']
        
        # Responder con RAG
        result = await self.rag_engine.query(message, context.expert_state.get('variables', {}))
        
        # Agregar opción para continuar
        result['clarification_mode'] = True
        result['continue_option'] = {
            'text': '✓ Continuar con el cálculo',
            'action': 'resume_expert'
        }
        result['mode'] = ConversationMode.HYBRID.value
        result['mode_label'] = '⚡ Aclaración'
        
        return result
    
    async def _handle_mode_switch(self, conversation_id: str, target_mode: str) -> Dict[str, Any]:
        """Maneja cambio de modo"""
        context = self.get_or_create_context(conversation_id)
        context.mode = target_mode
        
        if target_mode == ConversationMode.EXPERT.value:
            # Iniciar o reanudar flujo experto
            if context.paused_expert_node:
                context.expert_state['current_node'] = context.paused_expert_node
                context.paused_expert_node = None
            return await self._handle_expert_flow(conversation_id, "", None, None)
        
        elif target_mode == ConversationMode.RAG.value:
            return {
                'type': 'mode_switch',
                'mode': ConversationMode.RAG.value,
                'mode_label': '💬 Modo Chat',
                'text': 'Perfecto, ahora puedes hacerme cualquier pregunta sobre calefacción.',
                'is_final': False
            }
        
        return {
            'type': 'mode_switch',
            'mode': ConversationMode.HYBRID.value,
            'mode_label': '⚡ Modo Híbrido',
            'text': 'Modo híbrido activado. Puedo guiarte o responder preguntas libremente.',
            'is_final': False
        }
    
    async def _handle_hybrid_mode(self, conversation_id: str, message: str) -> Dict[str, Any]:
        """Maneja modo híbrido combinando experto y RAG"""
        context = self.get_or_create_context(conversation_id)
        
        # Obtener información del RAG
        rag_result = await self.rag_engine.query(message, context.expert_state.get('variables', {}))
        
        # Obtener sugerencia del experto
        expert_suggestion = await self.expert_engine.suggest_next_step(
            context.expert_state.get('variables', {})
        )
        
        # Fusionar respuestas
        merged_result = self._merge_responses(rag_result, expert_suggestion)
        merged_result['mode'] = ConversationMode.HYBRID.value
        merged_result['mode_label'] = '⚡ Modo Híbrido'
        
        return merged_result
    
    def _merge_responses(self, rag_result: Dict[str, Any], 
                        expert_suggestion: Dict[str, Any]) -> Dict[str, Any]:
        """Fusiona respuestas del RAG y el experto"""
        merged = {
            'type': 'hybrid',
            'rag_answer': rag_result.get('answer', ''),
            'expert_suggestion': expert_suggestion.get('suggestion', ''),
            'options': []
        }
        
        # Agregar opciones del experto si existen
        if expert_suggestion.get('options'):
            merged['options'].extend(expert_suggestion['options'])
        
        # Agregar opción para búsqueda de productos si el RAG lo sugiere
        if rag_result.get('products'):
            merged['products'] = rag_result['products']
        
        return merged
    
    def _should_suggest_guided_flow(self, message: str) -> bool:
        """Determina si se debe sugerir un flujo guiado"""
        calculation_keywords = ['calcular', 'dimensionar', 'cuántos', 'necesito']
        return any(keyword in message.lower() for keyword in calculation_keywords)
