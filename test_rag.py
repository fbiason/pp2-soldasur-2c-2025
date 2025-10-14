# test_rag.py - Script de prueba para RAG Engine V2 con Ollama Mistral
import asyncio
from app.rag_engine_v2 import rag_engine_v2

async def test_rag():
    """Prueba el RAG Engine con diferentes consultas"""
    
    print("\n" + "="*60)
    print("🧪 PRUEBA DEL RAG ENGINE V2 CON OLLAMA MISTRAL")
    print("="*60 + "\n")
    
    # Consultas de prueba
    test_queries = [
        "¿Qué radiador me recomendas para un dormitorio de 10m²?",
        "Necesito un sistema de calefacción para una casa de 150m²",
        "¿Cuál es la diferencia entre piso radiante y radiadores?",
        "Quiero un termotanque para 4 personas"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'─'*60}")
        print(f"📝 Consulta {i}: {query}")
        print(f"{'─'*60}\n")
        
        try:
            # Ejecutar consulta
            result = await rag_engine_v2.query(query, top_k=3)
            
            # Mostrar respuesta
            print(f"💬 RESPUESTA:\n{result['answer']}\n")
            
            # Mostrar productos recomendados
            if result.get('products'):
                print(f"📦 PRODUCTOS RECOMENDADOS:")
                for j, product in enumerate(result['products'], 1):
                    print(f"  {j}. {product['model']} - {product['power_w']}W")
                    print(f"     {product['description'][:80]}...")
                print()
            
            # Mostrar sugerencia de experto si existe
            if result.get('expert_suggestion'):
                print(f"💡 SUGERENCIA: {result['expert_suggestion']['message']}\n")
            
        except Exception as e:
            print(f"❌ Error: {e}\n")
        
        # Pausa entre consultas
        if i < len(test_queries):
            print("\n⏳ Esperando 2 segundos...\n")
            await asyncio.sleep(2)
    
    print("\n" + "="*60)
    print("✅ PRUEBA COMPLETADA")
    print("="*60 + "\n")

if __name__ == "__main__":
    asyncio.run(test_rag())
