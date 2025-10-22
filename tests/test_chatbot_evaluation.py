"""
Script de Evaluación del Chatbot Soldy - VERSIÓN DEMO
Evalúa el desempeño con respuestas simuladas (no requiere Ollama corriendo)
"""

from typing import Dict, List

class ChatbotEvaluator:
    """Evaluador de desempeño del chatbot"""
    
    def __init__(self):
        self.test_cases = self._load_test_cases()
    
    def _load_test_cases(self) -> List[Dict]:
        """Casos de prueba con respuestas esperadas y simuladas"""
        return [
            {
                "id": 1,
                "categoria": "Consulta Producto Específico",
                "pregunta": "¿Qué caldera me recomendás para 80m²?",
                "respuesta_simulada": "Para 80m² te recomiendo la Prima Tec Smart, es eficiente y perfecta para ese tamaño.",
                "intencion_esperada": "Recomendación de producto para superficie específica",
                "debe_incluir": ["producto específico", "beneficio", "tono vos/podés"],
                "no_debe_incluir": ["precio", "explicación técnica larga"],
                "respuesta_ideal": "Para 80m² te recomiendo la Prima Tec Smart, es eficiente y perfecta para ese tamaño. ¿Querés saber más sobre instalación?"
            },
            {
                "id": 2,
                "categoria": "Consulta Precios",
                "pregunta": "¿Cuánto sale la Prima Tec Smart?",
                "respuesta_simulada": "Para precios y compras, ¿estás en Río Grande o Ushuaia? Te paso el contacto de la sucursal.",
                "intencion_esperada": "Consulta de precio",
                "debe_incluir": ["Río Grande o Ushuaia", "contacto"],
                "no_debe_incluir": ["precio", "monto", "$", "pesos"],
                "respuesta_ideal": "Para precios y compras, ¿estás en Río Grande o Ushuaia? Te paso el contacto de la sucursal."
            },
            {
                "id": 3,
                "categoria": "Consulta Técnica Simple",
                "pregunta": "¿Los radiadores Broen son buenos?",
                "respuesta_simulada": "Sí, los Broen son excelentes, eficientes y duraderos. Son ideales para calefacción residencial.",
                "intencion_esperada": "Consulta sobre calidad de producto",
                "debe_incluir": ["Broen", "beneficio", "recomendación"],
                "no_debe_incluir": ["tecnicismos complejos"],
                "respuesta_ideal": "Sí, los Broen son excelentes, eficientes y duraderos. Son ideales para calefacción residencial."
            },
            {
                "id": 4,
                "categoria": "Consulta Técnica Compleja",
                "pregunta": "¿Cómo funciona el sistema de condensación?",
                "respuesta_simulada": "El sistema de condensación aprovecha mejor el calor, ahorrando gas. La Summa Condens usa esta tecnología.",
                "intencion_esperada": "Explicación técnica",
                "debe_incluir": ["explicación simple", "producto con esa tecnología"],
                "no_debe_incluir": ["tecnicismos excesivos"],
                "respuesta_ideal": "El sistema de condensación aprovecha mejor el calor, ahorrando gas. La Summa Condens usa esta tecnología."
            },
            {
                "id": 5,
                "categoria": "Consulta Fuera de Tema",
                "pregunta": "¿Cuál es el mejor restaurante de Ushuaia?",
                "respuesta_simulada": "Jaja, no soy experto en restaurantes, pero sí en calefacción. ¿Necesitás algo para tu hogar?",
                "intencion_esperada": "Pregunta no relacionada",
                "debe_incluir": ["respuesta amable", "redirección a productos"],
                "no_debe_incluir": ["respuesta sobre restaurantes"],
                "respuesta_ideal": "Jaja, no soy experto en restaurantes, pero sí en calefacción. ¿Necesitás algo para tu hogar?"
            },
            {
                "id": 6,
                "categoria": "Consulta Comparación",
                "pregunta": "¿Qué diferencia hay entre Prima Tec y Diva Tecno?",
                "respuesta_simulada": "La Prima Tec Smart es más moderna con mejor eficiencia, mientras la Diva Tecno es más económica. Ambas son excelentes.",
                "intencion_esperada": "Comparación de productos",
                "debe_incluir": ["ambos productos", "diferencia clave"],
                "no_debe_incluir": ["explicación muy larga"],
                "respuesta_ideal": "La Prima Tec Smart es más moderna con mejor eficiencia, mientras la Diva Tecno es más económica. Ambas son excelentes."
            },
            {
                "id": 7,
                "categoria": "Consulta Dónde Comprar",
                "pregunta": "¿Dónde puedo comprar radiadores?",
                "respuesta_simulada": "¿Estás en Río Grande o Ushuaia? Te paso los datos de nuestras sucursales para que puedas visitarnos.",
                "intencion_esperada": "Consulta de punto de venta",
                "debe_incluir": ["Río Grande o Ushuaia", "contacto"],
                "no_debe_incluir": ["precio"],
                "respuesta_ideal": "¿Estás en Río Grande o Ushuaia? Te paso los datos de nuestras sucursales para que puedas visitarnos."
            },
            {
                "id": 8,
                "categoria": "Consulta Instalación",
                "pregunta": "¿Es difícil instalar una caldera?",
                "respuesta_simulada": "La instalación debe hacerla un profesional matriculado. Si querés, te paso contacto de nuestros técnicos.",
                "intencion_esperada": "Consulta sobre instalación",
                "debe_incluir": ["profesional", "contacto técnico"],
                "no_debe_incluir": ["instrucciones de instalación DIY"],
                "respuesta_ideal": "La instalación debe hacerla un profesional matriculado. Si querés, te paso contacto de nuestros técnicos."
            }
        ]
    
    def evaluate_response(self, pregunta: str, respuesta: str, caso: Dict) -> Dict:
        """Evalúa una respuesta según las 4 métricas"""
        
        # 1. Detección de Intención (1-5)
        intencion_score = self._evaluate_intention(respuesta, caso)
        
        # 2. Relevancia (1-5)
        relevancia_score = self._evaluate_relevance(respuesta, caso)
        
        # 3. Claridad (1-5)
        claridad_score = self._evaluate_clarity(respuesta)
        
        # 4. Tono (1-5)
        tono_score = self._evaluate_tone(respuesta)
        
        promedio = (intencion_score + relevancia_score + claridad_score + tono_score) / 4
        
        return {
            "pregunta": pregunta,
            "respuesta": respuesta,
            "categoria": caso["categoria"],
            "metricas": {
                "deteccion_intencion": intencion_score,
                "relevancia": relevancia_score,
                "claridad": claridad_score,
                "tono": tono_score,
                "promedio": round(promedio, 2)
            },
            "justificaciones": {
                "intencion": self._justify_intention(intencion_score, caso),
                "relevancia": self._justify_relevance(relevancia_score, caso),
                "claridad": self._justify_clarity(claridad_score, respuesta),
                "tono": self._justify_tone(tono_score, respuesta)
            },
            "aspectos_positivos": self._get_positive_aspects(respuesta, caso),
            "aspectos_mejorar": self._get_improvement_aspects(respuesta, caso),
            "respuesta_ideal": caso["respuesta_ideal"]
        }
    
    def _evaluate_intention(self, respuesta: str, caso: Dict) -> int:
        """Evalúa si detectó correctamente la intención"""
        respuesta_lower = respuesta.lower()
        
        # Verificar elementos que debe incluir
        debe_incluir_count = sum(1 for item in caso["debe_incluir"] 
                                  if any(keyword in respuesta_lower for keyword in item.split()))
        
        # Verificar elementos que NO debe incluir
        no_debe_incluir_count = sum(1 for item in caso["no_debe_incluir"] 
                                     if any(keyword in respuesta_lower for keyword in item.split()))
        
        total_debe = len(caso["debe_incluir"])
        
        if debe_incluir_count == total_debe and no_debe_incluir_count == 0:
            return 5
        elif debe_incluir_count >= total_debe * 0.7 and no_debe_incluir_count == 0:
            return 4
        elif debe_incluir_count >= total_debe * 0.5:
            return 3
        elif debe_incluir_count > 0:
            return 2
        else:
            return 1
    
    def _evaluate_relevance(self, respuesta: str, caso: Dict) -> int:
        """Evalúa la relevancia de la respuesta"""
        respuesta_lower = respuesta.lower()
        
        # Verificar si menciona productos del catálogo cuando corresponde
        productos_mencionados = ["prima tec", "diva", "summa", "broen", "tropical", "gamma"]
        tiene_producto = any(prod in respuesta_lower for prod in productos_mencionados)
        
        # Verificar si responde la pregunta
        debe_incluir_presente = any(keyword in respuesta_lower 
                                     for item in caso["debe_incluir"] 
                                     for keyword in item.split())
        
        if debe_incluir_presente and (tiene_producto or "contacto" in respuesta_lower):
            return 5
        elif debe_incluir_presente:
            return 4
        elif tiene_producto:
            return 3
        else:
            return 2
    
    def _evaluate_clarity(self, respuesta: str) -> int:
        """Evalúa la claridad de la respuesta"""
        palabras = len(respuesta.split())
        frases = respuesta.count('.') + respuesta.count('?') + respuesta.count('!')
        
        # Ideal: 20-30 palabras, 2-3 frases
        if 20 <= palabras <= 35 and 2 <= frases <= 3:
            return 5
        elif 15 <= palabras <= 45 and 1 <= frases <= 4:
            return 4
        elif 10 <= palabras <= 60:
            return 3
        elif palabras < 10 or palabras > 80:
            return 2
        else:
            return 1
    
    def _evaluate_tone(self, respuesta: str) -> int:
        """Evalúa el tono de la respuesta"""
        respuesta_lower = respuesta.lower()
        
        # Indicadores de buen tono argentino
        tono_argentino = ["podés", "querés", "necesitás", "te recomiendo", "te paso"]
        tiene_tono_argentino = sum(1 for palabra in tono_argentino if palabra in respuesta_lower)
        
        # Indicadores de calidez
        calidez = ["perfecto", "excelente", "ideal", "jaja", "¡", "😊"]
        tiene_calidez = sum(1 for palabra in calidez if palabra in respuesta_lower)
        
        # Penalizaciones
        muy_formal = any(palabra in respuesta_lower for palabra in ["usted", "le recomiendo", "estimado"])
        muy_tecnico = any(palabra in respuesta_lower for palabra in ["kw/h", "coeficiente", "parámetros"])
        
        if tiene_tono_argentino >= 2 and tiene_calidez >= 1 and not muy_formal and not muy_tecnico:
            return 5
        elif tiene_tono_argentino >= 1 and not muy_formal:
            return 4
        elif not muy_formal and not muy_tecnico:
            return 3
        elif muy_formal or muy_tecnico:
            return 2
        else:
            return 1
    
    def _justify_intention(self, score: int, caso: Dict) -> str:
        """Justifica el puntaje de detección de intención"""
        if score >= 4:
            return f"Identifica correctamente la intención: {caso['intencion_esperada']}"
        elif score == 3:
            return f"Identifica parcialmente la intención, falta precisión"
        else:
            return f"No identifica correctamente la intención esperada: {caso['intencion_esperada']}"
    
    def _justify_relevance(self, score: int, caso: Dict) -> str:
        """Justifica el puntaje de relevancia"""
        if score >= 4:
            return "Respuesta totalmente relevante y útil para la consulta"
        elif score == 3:
            return "Respuesta parcialmente relevante, podría ser más específica"
        else:
            return "Respuesta poco relevante o genérica"
    
    def _justify_clarity(self, score: int, respuesta: str) -> str:
        """Justifica el puntaje de claridad"""
        palabras = len(respuesta.split())
        if score >= 4:
            return f"Respuesta clara y concisa ({palabras} palabras)"
        elif score == 3:
            return f"Respuesta comprensible pero podría ser más concisa ({palabras} palabras)"
        else:
            return f"Respuesta confusa o demasiado {'corta' if palabras < 15 else 'larga'} ({palabras} palabras)"
    
    def _justify_tone(self, score: int, respuesta: str) -> str:
        """Justifica el puntaje de tono"""
        if score >= 4:
            return "Tono cálido, empático y profesional con español argentino"
        elif score == 3:
            return "Tono aceptable pero podría ser más cálido o usar más vos/podés"
        else:
            return "Tono inadecuado (muy formal, técnico o impersonal)"
    
    def _get_positive_aspects(self, respuesta: str, caso: Dict) -> List[str]:
        """Identifica aspectos positivos de la respuesta"""
        positivos = []
        respuesta_lower = respuesta.lower()
        
        if any(palabra in respuesta_lower for palabra in ["podés", "querés", "necesitás"]):
            positivos.append("Usa español argentino (vos/podés)")
        
        if len(respuesta.split()) <= 35:
            positivos.append("Respuesta breve y concisa")
        
        productos = ["prima tec", "diva", "summa", "broen", "tropical"]
        if any(prod in respuesta_lower for prod in productos):
            positivos.append("Recomienda producto específico del catálogo")
        
        if "río grande o ushuaia" in respuesta_lower:
            positivos.append("Maneja correctamente consultas de precio/compra")
        
        return positivos if positivos else ["Ninguno identificado"]
    
    def _get_improvement_aspects(self, respuesta: str, caso: Dict) -> List[str]:
        """Identifica aspectos a mejorar"""
        mejoras = []
        respuesta_lower = respuesta.lower()
        
        # Verificar elementos que NO debe incluir
        for item in caso["no_debe_incluir"]:
            if any(keyword in respuesta_lower for keyword in item.split()):
                mejoras.append(f"No debe incluir: {item}")
        
        # Verificar elementos que debe incluir
        for item in caso["debe_incluir"]:
            if not any(keyword in respuesta_lower for keyword in item.split()):
                mejoras.append(f"Debe incluir: {item}")
        
        if len(respuesta.split()) > 40:
            mejoras.append("Reducir extensión (máximo 30 palabras)")
        
        if not any(palabra in respuesta_lower for palabra in ["podés", "querés", "necesitás"]):
            mejoras.append("Usar más español argentino (vos/podés)")
        
        return mejoras if mejoras else ["Ninguno identificado"]
    
    def run_evaluation(self):
        """Ejecuta la evaluación completa"""
        print("=" * 80)
        print("📊 EVALUACIÓN DE DESEMPEÑO DEL CHATBOT SOLDY (DEMO)")
        print("=" * 80)
        print("\n⚠️  NOTA: Usando respuestas simuladas ideales para demostración")
        print("    Para evaluar con Ollama real, instala: pip install ollama")
        print()
        
        resultados = []
        
        for caso in self.test_cases:
            print(f"\n{'='*80}")
            print(f"🔍 CASO {caso['id']}: {caso['categoria']}")
            print(f"{'='*80}")
            print(f"\n👤 Usuario: {caso['pregunta']}")
            
            # Usar respuesta simulada
            respuesta = caso['respuesta_simulada']
            print(f"🤖 Soldy: {respuesta}")
            
            # Evaluar respuesta
            evaluacion = self.evaluate_response(caso['pregunta'], respuesta, caso)
            resultados.append(evaluacion)
            
            # Mostrar métricas
            print(f"\n📈 MÉTRICAS:")
            print(f"  • Detección de Intención: {evaluacion['metricas']['deteccion_intencion']}/5")
            print(f"    └─ {evaluacion['justificaciones']['intencion']}")
            print(f"  • Relevancia: {evaluacion['metricas']['relevancia']}/5")
            print(f"    └─ {evaluacion['justificaciones']['relevancia']}")
            print(f"  • Claridad: {evaluacion['metricas']['claridad']}/5")
            print(f"    └─ {evaluacion['justificaciones']['claridad']}")
            print(f"  • Tono: {evaluacion['metricas']['tono']}/5")
            print(f"    └─ {evaluacion['justificaciones']['tono']}")
            print(f"\n  ⭐ PROMEDIO: {evaluacion['metricas']['promedio']}/5")
            
            # Aspectos positivos y a mejorar
            print(f"\n✅ Aspectos Positivos:")
            for aspecto in evaluacion['aspectos_positivos']:
                print(f"  • {aspecto}")
            
            print(f"\n⚠️ Aspectos a Mejorar:")
            for aspecto in evaluacion['aspectos_mejorar']:
                print(f"  • {aspecto}")
        
        # Resumen general
        print(f"\n\n{'='*80}")
        print("📊 RESUMEN GENERAL")
        print(f"{'='*80}")
        
        if resultados:
            promedio_general = sum(r['metricas']['promedio'] for r in resultados) / len(resultados)
            promedio_intencion = sum(r['metricas']['deteccion_intencion'] for r in resultados) / len(resultados)
            promedio_relevancia = sum(r['metricas']['relevancia'] for r in resultados) / len(resultados)
            promedio_claridad = sum(r['metricas']['claridad'] for r in resultados) / len(resultados)
            promedio_tono = sum(r['metricas']['tono'] for r in resultados) / len(resultados)
            
            print(f"\n📈 Promedios por Métrica:")
            print(f"  • Detección de Intención: {promedio_intencion:.2f}/5")
            print(f"  • Relevancia: {promedio_relevancia:.2f}/5")
            print(f"  • Claridad: {promedio_claridad:.2f}/5")
            print(f"  • Tono: {promedio_tono:.2f}/5")
            print(f"\n  ⭐ PROMEDIO GENERAL: {promedio_general:.2f}/5")
            
            # Clasificación
            if promedio_general >= 4.5:
                clasificacion = "🏆 EXCELENTE"
            elif promedio_general >= 3.5:
                clasificacion = "✅ BUENO"
            elif promedio_general >= 2.5:
                clasificacion = "⚠️ ACEPTABLE"
            else:
                clasificacion = "❌ DEFICIENTE"
            
            print(f"\n  {clasificacion}")
            
            # Recomendaciones
            print(f"\n💡 Recomendaciones Generales:")
            if promedio_intencion < 4.0:
                print("  • Mejorar detección de intención con más keywords y ejemplos")
            if promedio_relevancia < 4.0:
                print("  • Asegurar que siempre recomiende productos específicos")
            if promedio_claridad < 4.0:
                print("  • Ajustar límites de tokens para respuestas más concisas")
            if promedio_tono < 4.0:
                print("  • Reforzar uso de español argentino (vos/podés) en system prompt")
            
            if promedio_general >= 4.5:
                print("\n🎉 ¡Excelente trabajo! El chatbot está funcionando muy bien.")
        
        print(f"\n{'='*80}\n")

if __name__ == "__main__":
    evaluator = ChatbotEvaluator()
    evaluator.run_evaluation()
