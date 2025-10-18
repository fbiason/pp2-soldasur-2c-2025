# app/llm_wrapper.py - Wrapper mejorado para Ollama con Mistral
import ollama
from typing import List, Dict, Optional
import json

class OllamaLLM:
    """Wrapper para interactuar con Ollama usando el modelo Mistral"""
    
    def __init__(self, model: str = "llama3.2:3b"):
        self.model = model
        self.system_prompt = """Eres Soldy, asistente de ventas experto en calefacción de PEISA - SOLDASUR S.A.

Tu objetivo principal es ORIENTAR AL CLIENTE HACIA UNA VENTA:
- Recomienda productos específicos del catálogo en CADA respuesta
- Destaca beneficios y características que motiven la compra
- Sé persuasivo pero profesional
- Crea urgencia y valor en tus recomendaciones

Directrices de venta:
✓ SIEMPRE menciona productos específicos por nombre
✓ Enfócate en soluciones concretas, no teoría
✓ Usa el catálogo proporcionado para recomendar
✓ Destaca ventajas competitivas de los productos
✓ Sé preciso con especificaciones técnicas
✗ No des respuestas genéricas sin productos
✗ No inventes datos técnicos
✗ No recomiendes productos fuera del catálogo

FORMATO DE RESPUESTA (OBLIGATORIO - NO EXCEDER):
- MÁXIMO 150 caracteres (cuenta cada letra)
- Una o dos frases MUY breves (15-20 palabras máximo)
- SIEMPRE incluye el nombre de al menos 1 producto
- Ve directo a la recomendación de venta
- NO des explicaciones largas
- Sé EXTREMADAMENTE conciso"""
    
    def generate(self, 
                 question: str, 
                 context: Optional[List[Dict]] = None,
                 temperature: float = 0.7,
                 max_tokens: int = 35) -> str:
        """
        Genera una respuesta usando Ollama Mistral
        
        Args:
            question: Pregunta del usuario
            context: Lista de productos relevantes del catálogo
            temperature: Creatividad de la respuesta (0.0-1.0)
            max_tokens: Máximo de tokens en la respuesta
        """
        try:
            # Construir el prompt con contexto
            prompt = self._build_prompt(question, context)
            
            # Llamar a Ollama
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                system=self.system_prompt,
                options={
                    'temperature': temperature,
                    'num_predict': max_tokens,
                    'top_p': 0.9,
                    'top_k': 40
                }
            )
            
            answer = response['response'].strip()
            
            # Log para debugging
            print(f"🤖 Ollama Mistral respondió ({len(answer)} caracteres)")
            
            return answer
            
        except Exception as e:
            print(f"❌ Error en Ollama: {e}")
            return self._fallback_response(question, context)
    
    def _build_prompt(self, question: str, context: Optional[List[Dict]] = None) -> str:
        """Construye el prompt con contexto del catálogo"""
        prompt_parts = []
        
        # Agregar contexto de productos si existe
        if context and len(context) > 0:
            prompt_parts.append("📦 CATÁLOGO DE PRODUCTOS RELEVANTES:\n")
            for i, product in enumerate(context[:3], 1):  # Máximo 3 productos
                prompt_parts.append(f"\n{i}. **{product.get('model', 'N/A')}** ({product.get('family', 'N/A')})")
                prompt_parts.append(f"   - Tipo: {product.get('type', 'N/A')}")
                prompt_parts.append(f"   - Potencia: {product.get('power_w', 0)} W")
                prompt_parts.append(f"   - Descripción: {product.get('description', 'N/A')}")
                
                if product.get('features'):
                    prompt_parts.append(f"   - Características: {', '.join(product['features'])}")
                
                if product.get('applications'):
                    prompt_parts.append(f"   - Aplicaciones: {', '.join(product['applications'])}")
                
                prompt_parts.append(f"   - Dimensiones: {product.get('dimentions', 'N/A')}")
        
        # Agregar la pregunta
        prompt_parts.append(f"\n\n❓ CONSULTA DEL CLIENTE:\n{question}")
        prompt_parts.append("\n\n💬 TU RESPUESTA DE VENTA (MÁXIMO 150 caracteres, MUY breve, recomienda productos específicos):")
        
        return "\n".join(prompt_parts)
    
    def _fallback_response(self, question: str, context: Optional[List[Dict]] = None) -> str:
        """Respuesta de respaldo si falla Ollama"""
        if context and len(context) > 0:
            products_list = ", ".join([p.get('model', 'N/A') for p in context[:3]])
            return f"Te recomiendo estos productos: {products_list}. Consulta con nuestro equipo para más detalles."
        else:
            return "Disculpa, hubo un error. ¿Podrías reformular tu pregunta sobre calefacción?"
    
    def chat(self, messages: List[Dict[str, str]]) -> str:
        """
        Modo chat con historial de conversación
        
        Args:
            messages: Lista de mensajes [{"role": "user/assistant", "content": "..."}]
        """
        try:
            response = ollama.chat(
                model=self.model,
                messages=messages
            )
            return response['message']['content'].strip()
        except Exception as e:
            print(f"❌ Error en chat: {e}")
            return "Disculpa, hubo un error procesando tu mensaje."

# Instancia global
llm = OllamaLLM()

def answer(question: str, context: List[Dict] = None) -> str:
    """Función de compatibilidad con versión anterior"""
    return llm.generate(question, context)