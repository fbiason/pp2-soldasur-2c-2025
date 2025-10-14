# app/main.py - Sistema Unificado con Orquestador Inteligente
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import traceback

app = FastAPI(title="PEISA - SOLDASUR S.A", description="Asistente Inteligente Unificado para Calefacción")

# Modelos Pydantic para request/response
class StartConversationRequest(BaseModel):
    conversation_id: str
    mode: Optional[str] = "hybrid"  # "expert", "rag", o "hybrid"

class ReplyRequest(BaseModel):
    conversation_id: str
    message: Optional[str] = ""
    option_index: Optional[int] = None
    input_values: Optional[Dict[str, Any]] = {}

class ConversationResponse(BaseModel):
    conversation_id: str
    node_id: Optional[str] = None
    type: Optional[str] = None
    text: Optional[str] = None
    options: Optional[List[str]] = None
    input_type: Optional[str] = None
    input_label: Optional[str] = None
    inputs: Optional[List[Dict[str, Any]]] = None
    is_final: Optional[bool] = None
    error: Optional[str] = None
    mode: Optional[str] = None
    mode_label: Optional[str] = None
    additional_info: Optional[str] = None
    suggestion: Optional[Dict[str, Any]] = None
    products: Optional[List[Dict[str, Any]]] = None

# Variables globales para los motores (se inicializarán en startup)
orchestrator = None
expert_engine = None
rag_engine = None

@app.on_event("startup")
async def startup_event():
    """Inicializa los motores al arrancar el servidor"""
    global orchestrator, expert_engine, rag_engine
    
    try:
        print("\n" + "="*60)
        print("🚀 INICIANDO SISTEMA UNIFICADO PEISA - SOLDASUR")
        print("="*60 + "\n")
        
        # Importar módulos
        from app.expert_engine import ExpertEngine
        from app.rag_engine_v2 import rag_engine_v2
        from app.orchestrator import ConversationOrchestrator
        
        # Crear Expert Engine
        print("📋 Inicializando Expert Engine...")
        expert_engine = ExpertEngine()
        print("✅ Expert Engine listo\n")
        
        # Usar RAG Engine V2 (ya inicializado globalmente)
        rag_engine = rag_engine_v2
        if rag_engine is None:
            raise Exception("RAG Engine V2 no se pudo inicializar")
        print("✅ RAG Engine V2 listo\n")
        
        # Inyección de dependencias mutuas
        print("🔗 Configurando dependencias mutuas...")
        expert_engine.set_rag_engine(rag_engine)
        rag_engine.set_expert_engine(expert_engine)
        print("✅ Dependencias configuradas\n")
        
        # Crear orquestador
        print("🎭 Inicializando Orquestador...")
        orchestrator = ConversationOrchestrator(expert_engine, rag_engine)
        print("✅ Orquestador listo\n")
        
        print("="*60)
        print("🎉 SISTEMA UNIFICADO LISTO")
        print("="*60)
        print("\n📡 Servidor disponible en: http://localhost:8000")
        print("📚 Documentación API: http://localhost:8000/docs")
        print("💬 Chat Unificado: http://localhost:8000/\n")
        
    except Exception as e:
        print(f"\n❌ ERROR AL INICIALIZAR MOTORES: {e}")
        print(traceback.format_exc())
        print("\n⚠️  El servidor continuará pero sin funcionalidad completa\n")

@app.get("/", response_class=HTMLResponse)
async def home():
    """Sirve la página principal del chat"""
    try:
        with open("app/chat_unified.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        try:
            # Fallback a chat.html original
            with open("app/chat.html", "r", encoding="utf-8") as f:
                return HTMLResponse(content=f.read())
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="Archivo HTML no encontrado")

@app.post("/start", response_model=ConversationResponse)
async def start_conversation(request: StartConversationRequest):
    """Inicia una nueva conversación con el sistema unificado"""
    try:
        if orchestrator is None:
            raise HTTPException(status_code=503, detail="Sistema no inicializado. Reinicia el servidor.")
        
        conversation_id = request.conversation_id
        
        # Crear contexto en el orquestador
        context = orchestrator.get_or_create_context(conversation_id)
        context.mode = request.mode
        
        # Iniciar con el modo seleccionado
        if request.mode == "expert":
            result = await orchestrator._handle_expert_flow(conversation_id, "", None, None)
        elif request.mode == "rag":
            result = {
                'type': 'greeting',
                'text': '¡Hola! Soy tu asistente de calefacción. Puedes hacerme cualquier pregunta.',
                'mode': 'rag',
                'mode_label': '💬 Modo Chat'
            }
        else:  # hybrid
            result = await orchestrator._handle_expert_flow(conversation_id, "", None, None)
        
        return _convert_to_response(conversation_id, result)
        
    except Exception as e:
        print(f"❌ Error en /start: {e}")
        print(traceback.format_exc())
        return ConversationResponse(
            conversation_id=request.conversation_id,
            error=f"Error al iniciar conversación: {str(e)}",
            type="error",
            text="Hubo un problema al iniciar. Por favor, recarga la página."
        )

@app.post("/reply", response_model=ConversationResponse)
async def handle_reply(request: ReplyRequest):
    """Maneja las respuestas del usuario usando el orquestador"""
    try:
        if orchestrator is None:
            raise HTTPException(status_code=503, detail="Sistema no inicializado")
        
        conversation_id = request.conversation_id
        message = request.message
        option_index = request.option_index
        input_values = request.input_values or {}
        
        # Procesar mensaje a través del orquestador
        result = await orchestrator.process_message(
            conversation_id=conversation_id,
            message=message,
            option_index=option_index,
            input_values=input_values
        )
        
        return _convert_to_response(conversation_id, result)
        
    except Exception as e:
        print(f"❌ Error en /reply: {e}")
        print(traceback.format_exc())
        return ConversationResponse(
            conversation_id=request.conversation_id,
            error=f"Error al procesar respuesta: {str(e)}",
            type="error",
            text="Hubo un problema. Por favor, intenta nuevamente."
        )

def _convert_to_response(conversation_id: str, result: Dict[str, Any]) -> ConversationResponse:
    """Convierte el resultado del orquestador a ConversationResponse"""
    
    # Manejar suggestion - debe ser dict o None
    suggestion = result.get('suggestion') or result.get('expert_suggestion')
    if suggestion and isinstance(suggestion, str):
        # Si es string, convertir a dict
        suggestion = {'message': suggestion}
    elif suggestion and not isinstance(suggestion, dict):
        suggestion = None
    
    return ConversationResponse(
        conversation_id=conversation_id,
        node_id=result.get('node_id'),
        type=result.get('type'),
        text=result.get('text') or result.get('answer'),
        options=result.get('options'),
        input_type=result.get('input_type'),
        input_label=result.get('input_label'),
        inputs=result.get('inputs'),
        is_final=result.get('is_final', False),
        error=result.get('error'),
        mode=result.get('mode'),
        mode_label=result.get('mode_label'),
        additional_info=result.get('additional_info'),
        suggestion=suggestion,
        products=result.get('products')
    )

@app.get("/health")
async def health_check():
    """Endpoint de verificación de salud del servicio"""
    status = {
        "status": "ok" if orchestrator is not None else "initializing",
        "service": "PEISA - SOLDASUR S.A",
        "expert_engine": "ready" if expert_engine is not None else "not ready",
        "rag_engine": "ready" if rag_engine is not None else "not ready",
        "orchestrator": "ready" if orchestrator is not None else "not ready"
    }
    return status

@app.get("/ask")
async def ask(question: str = Query(..., min_length=5)):
    """Endpoint para consultas directas (compatibilidad con versión anterior)"""
    try:
        if rag_engine is None:
            raise HTTPException(status_code=503, detail="RAG Engine no inicializado")
        
        result = await rag_engine.query(question, expert_context=None)
        return {
            "respuesta": result.get('answer', ''),
            "productos": result.get('products', []),
            "mode": "rag"
        }
    except Exception as e:
        print(f"❌ Error en /ask: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)