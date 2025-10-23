# app/llm_wrapper.py - Wrapper mejorado para Ollama con Mistral
import ollama
import os
from typing import List, Dict, Optional
import json

class OllamaLLM:
    """Wrapper para interactuar con Ollama usando el modelo Mistral"""
    
    def __init__(self, model: str = "llama3.2:3b"):
        self.model = model
        # Configurar host de Ollama; respeta OLLAMA_HOST si está definida
        self.ollama_host = os.getenv('OLLAMA_HOST', 'http://127.0.0.1:11434')
        try:
            self.client = ollama.Client(host=self.ollama_host)
        except Exception:
            # Fallback simple al módulo si falla la creación del cliente
            self.client = None
        self.system_prompt = """Eres Soldy, asesor de ventas de PEISA-SOLDASUR. Tu objetivo es ayudar con calidez y profesionalismo.

REGLAS DE ORO:
✅ Respuestas MUY BREVES: 1 sola oración (15–20 palabras)
✅ Solo sobre PRODUCTOS: Si hay contexto de productos, menciona únicamente esos modelos (no inventes otros)
✅ DIRECTO AL PUNTO: Sin rodeos ni explicaciones largas
✅ 1 recomendación (o 2 como máximo) con modelo y potencia
✅ Español argentino: vos/podés, tono cercano

🚫 NUNCA MENCIONES PRECIOS, COSTOS O MONTOS
Si preguntan por precio/compra/presupuesto/dónde consigo, responde:
"Para precios y compras, ¿estás en Río Grande o Ushuaia?"

FORMATO DE RESPUESTA:
- "<Modelo> – <potencia> W – <motivo breve>" (1 o 2 ítems como máximo, en una sola oración si es posible)

EJEMPLOS:
❌ MAL: "Para calentar tu hogar eficientemente... te recomiendo considerar un sistema de calefacción completo..."
✅ BIEN: "Caldera Diva 24 – 24000 W – alcanza tu carga; o Diva 30 si querés más margen."

✗ No inventes datos técnicos
✗ No recomiendes productos fuera del catálogo/contexto
✗ No des explicaciones largas o técnicas
✗ No repitas información
    - TERMINA SIEMPRE CON PUNTO FINAL (.)"""

        # CTA opcional desde variable de entorno
        self.contact_cta = os.getenv('SOLDASUR_CONTACT_CTA')
        if self.contact_cta:
            self.system_prompt += f"\nContacto comercial: {self.contact_cta}"
    
    def generate(self, 
                 question: str, 
                 context: Optional[List[Dict]] = None,
                 temperature: float = 0.2,
                 max_tokens: int = 80) -> str:
        """
        Genera una respuesta usando Ollama Mistral
        
        Args:
            question: Pregunta del usuario
            context: Lista de productos relevantes del catálogo
            temperature: Creatividad de la respuesta (0.0-1.0)
            max_tokens: Máximo de tokens en la respuesta
        """
        try:
            # Si preguntan por precio, responder sin pasar por el LLM
            if self._is_price_question(question):
                safe = self._price_refusal_response(context)
                return self._ensure_final_period(safe)

            # Construir el prompt con contexto
            prompt = self._build_prompt(question, context)
            
            # Llamar a Ollama con control ESTRICTO de longitud
            # Usar cliente si está disponible; si no, usar API global
            generate_fn = self.client.generate if self.client else ollama.generate
            response = generate_fn(
                model=self.model,
                prompt=prompt,
                system=self.system_prompt,
                options={
                    'temperature': temperature,
                    # Límite de tokens (por defecto 80 para respuestas breves)
                    'num_predict': max_tokens,
                    'top_p': 0.5,  # Más determinismo
                    'top_k': 20,   # Bajo para máximo control
                    'repeat_penalty': 1.3,  # Penaliza repeticiones
                    'num_ctx': 1024  # Contexto limitado para foco
                }
            )
            
            answer = response['response'].strip()
            
            # POST-PROCESAMIENTO: Truncar a primera oración completa
            answer = self._truncate_to_brief(answer)
            # Sanitizar menciones de precios
            answer = self._sanitize_prices(answer)
            # Asegurar punto final
            answer = self._ensure_final_period(answer)
            
            # Log para debugging
            word_count = len(answer.split())
            print(f"🤖 Ollama respondió: {word_count} palabras, {len(answer)} caracteres")
            
            return answer
            
        except Exception as e:
            print(f"❌ Error en Ollama: {e}")
            return self._fallback_response(question, context)
    
    def _truncate_to_brief(self, text: str, max_words: int = 30) -> str:
        """
        Trunca la respuesta para garantizar brevedad (2-3 frases, 20-30 palabras)
        Corta en la primera oración completa o en max_words
        """
        # Eliminar saltos de línea múltiples
        text = ' '.join(text.split())
        
        # Si ya es corto, retornar
        words = text.split()
        if len(words) <= max_words:
            return self._ensure_final_period(text)
        
        # Buscar primer punto, signo de pregunta o exclamación
        for i, char in enumerate(text):
            if char in ['.', '?', '!']:
                sentence = text[:i+1].strip()
                # Verificar que la oración tenga al menos 10 palabras
                if len(sentence.split()) >= 10:
                    return self._ensure_final_period(sentence)
        
        # Si no hay puntuación, truncar a max_words
        truncated = ' '.join(words[:max_words])
        # Agregar punto si no termina en puntuación
        return self._ensure_final_period(truncated)

    def _ensure_final_period(self, text: str) -> str:
        """Normaliza el cierre: reemplaza ?/! por punto y añade punto si falta.
        También retira comillas o paréntesis sueltos al final antes de cerrar.
        """
        if not text:
            return text
        # Quitar espacios y cierres sueltos al final
        stripped = text.rstrip()
        # Si termina en ? o !, reemplazar por .
        if stripped.endswith('?') or stripped.endswith('!'):
            stripped = stripped[:-1].rstrip()
        # Quitar comillas o paréntesis finales sueltos antes de puntuar
        while stripped and stripped[-1] in ['"', '”', '’', "'", ')', ']']:
            stripped = stripped[:-1].rstrip()
        # Asegurar punto final
        if not stripped.endswith('.'):
            stripped += '.'
        return stripped

    def _sanitize_prices(self, text: str) -> str:
        """Reemplaza patrones de precios/montos por 'precio a consultar'.
        Cubre $ 1.234,56 | $1234 | 1.234.567 | 1234,56 | AR$ | USD | U$S, evitando números técnicos (W, kW, V, mm, cm, %).
        """
        import re
        if not text:
            return text
        # Sólo considerar montos con contexto monetario
        currency = r"(?:AR\$|U\$S|US\$|USD|EUR|€|\$)"
        amount   = r"\d{1,3}(?:[\.,]\d{3})*(?:[\.,]\d{2})?"
        units_exclusion = r"(?!\s*(W|kW|V|mm|cm|m|°C|%|kg|m²|m3)\b)"
        word_currency = r"(?:ars|pesos?|usd|dólares?|euros?)"

        patterns = [
            rf"\b{currency}\s*{amount}{units_exclusion}\b",
            rf"\b{amount}\s*{word_currency}{units_exclusion}\b",
            rf"\b(precio|costo|vale|sale|cuesta|presupuesto)\s*(aprox\.?|aproximado|estimado|es|:)?\s*{currency}?\s*{amount}{units_exclusion}\b",
        ]
        sanitized = text
        for p in patterns:
            sanitized = re.sub(p, 'precio a consultar', sanitized, flags=re.IGNORECASE)
        return sanitized

    def _is_price_question(self, text: str) -> bool:
        """Detecta si el usuario está preguntando por precios o costos."""
        if not text:
            return False
        t = text.lower()
        keywords = [
            'precio', 'precios', 'costo', 'costos', 'presupuesto', 'cuesta', 'vale', 'sale',
            'descuento', 'promoción', 'promocion', 'oferta', 'cuotas', 'financiación', 'financiacion',
            'usd', 'u$s', 'u$s', 'ar$', '$', '€', 'eur'
        ]
        return any(k in t for k in keywords)

    def _price_refusal_response(self, context: Optional[List[Dict]] = None) -> str:
        """Respuesta estándar cuando se consultan precios."""
        if context:
            products = ", ".join([p.get('model', 'N/A') for p in context[:2]])
            base = f"No informamos precios por este medio; te recomiendo {products} y el precio es a consultar. ¿Estás en Río Grande o Ushuaia?"
        else:
            base = "No informamos precios por este medio; el precio es a consultar con nuestro equipo comercial. ¿Estás en Río Grande o Ushuaia?"
        if self.contact_cta:
            base += f" Contacto: {self.contact_cta}."
        return self._ensure_final_period(base)
    
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
        prompt_parts.append("\n\n💬 RESPONDE SOLO CON 1 ORACIÓN (15–20 palabras) mencionando 1–2 modelos del contexto, con potencia y motivo breve. Nada más:")
        
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
            chat_fn = self.client.chat if self.client else ollama.chat
            response = chat_fn(
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
