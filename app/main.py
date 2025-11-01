# app/main.py
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import json
import math
import time
from math import ceil
from bisect import bisect_left
from pathlib import Path
import os
from app.models import RADIATOR_MODELS
from query.query import search_filtered
from app.modules.chatbot.llm_wrapper import answer
from app.modules.expertSystem.expert_engine import ExpertEngine

app = FastAPI(title="PEISA - SOLDASUR S.A", description="Asistente para cálculos de calefacción")

# Obtener el directorio raíz del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Modelos Pydantic para request/response
class StartConversationRequest(BaseModel):
    conversation_id: str

class ReplyRequest(BaseModel):
    conversation_id: str
    option_index: Optional[int] = None
    input_values: Optional[Dict[str, Any]] = {}

class ConversationResponse(BaseModel):
    conversation_id: str
    node_id: str
    type: Optional[str] = None
    text: Optional[str] = None
    options: Optional[List[str]] = None
    input_type: Optional[str] = None
    input_label: Optional[str] = None
    inputs: Optional[List[Dict[str, Any]]] = None
    is_final: Optional[bool] = None
    error: Optional[str] = None

# Instanciar el motor del sistema experto
expert_engine = ExpertEngine()

# Contexto de la conversación
conversations: Dict[str, Dict[str, Any]] = {}

# Directorios para archivos estáticos (rutas absolutas)
STATIC_DIRECTORIES = [
    BASE_DIR / "app",
    BASE_DIR / "images", 
    BASE_DIR / "data"
]

@app.get("/", response_class=HTMLResponse)
async def home():
    """Sirve la página principal del chat"""
    html_path = BASE_DIR / "app" / "soldasur2025.html"
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Archivo {html_path} no encontrado")

@app.post("/start", response_model=ConversationResponse)
async def start_conversation(request: StartConversationRequest):
    """Inicia una nueva conversación"""
    conversation_id = request.conversation_id
    
    # Estado inicial para el motor experto
    expert_state = {
        'current_node': 'inicio',
        'variables': {}
    }
    conversations[conversation_id] = expert_state
    
    # Procesar el nodo inicial a través del motor experto
    response_data = await expert_engine.process(conversation_id, expert_state)
    
    # Guardar el estado actualizado
    conversations[conversation_id] = response_data.get('expert_state', expert_state)

    return ConversationResponse(
        conversation_id=conversation_id,
        node_id=response_data.get('node_id'),
        type=response_data.get('type'),
        text=response_data.get('text'),
        options=response_data.get('options'),
        input_type=response_data.get('input_type'),
        input_label=response_data.get('input_label'),
        inputs=response_data.get('inputs'),
        is_final=response_data.get('is_final', False),
        error=response_data.get('error')
    )

@app.post("/reply", response_model=ConversationResponse)
async def handle_reply(request: ReplyRequest):
    """Maneja las respuestas del usuario"""
    conversation_id = request.conversation_id
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversación no encontrada")
    
    expert_state = conversations[conversation_id]
    
    # Procesar la respuesta a través del motor experto
    response_data = await expert_engine.process(
        conversation_id,
        expert_state,
        option_index=request.option_index,
        input_values=request.input_values
    )
    
    # Guardar el estado actualizado
    conversations[conversation_id] = response_data.get('expert_state', expert_state)

    return ConversationResponse(
        conversation_id=conversation_id,
        node_id=response_data.get('node_id'),
        type=response_data.get('type'),
        text=response_data.get('text'),
        options=response_data.get('options'),
        input_type=response_data.get('input_type'),
        input_label=response_data.get('input_label'),
        inputs=response_data.get('inputs'),
        is_final=response_data.get('is_final', False),
        error=response_data.get('error')
    )

# Modelos para chatbot
class ChatRequest(BaseModel):
    question: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    products: Optional[List[Dict[str, Any]]] = None
    conversation_id: str

# Endpoint de chatbot con RAG
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chatbot con RAG - busca productos relevantes y genera respuesta"""
    try:
        print(f"[DEBUG] Chatbot - Pregunta recibida: {request.question}")
        
        # Generar ID de conversación si no existe
        conversation_id = request.conversation_id or f"chat_{int(time.time() * 1000)}"
        
        top_items = []
        respuesta = ""
        
        # Intentar buscar productos con RAG
        try:
            print(f"[DEBUG] Buscando productos con RAG...")
            top_items = search_filtered(request.question, top_k=3)
            print(f"[DEBUG] Productos encontrados: {len(top_items)}")
        except Exception as rag_error:
            print(f"[WARNING] Error en RAG: {rag_error}")
            import traceback
            traceback.print_exc()
        
        # Intentar usar LLM si está disponible (con timeout)
        try:
            print(f"[DEBUG] Intentando generar respuesta con LLM...")
            import asyncio
            
            # Ejecutar con timeout de 8 segundos
            try:
                respuesta = await asyncio.wait_for(
                    asyncio.to_thread(answer, request.question, top_items),
                    timeout=8.0
                )
                print(f"[DEBUG] Respuesta generada con LLM: {respuesta[:100]}...")
            except asyncio.TimeoutError:
                print(f"[WARNING] LLM timeout (>8s), usando respuesta automática rápida")
                raise Exception("LLM timeout")
                
        except Exception as llm_error:
            print(f"[WARNING] LLM no disponible, usando respuesta automática: {llm_error}")
            # Fallback: respuesta automática basada en productos encontrados
            if top_items and len(top_items) > 0:
                primer_producto = top_items[0]
                nombre = primer_producto.get('model', 'producto')
                familia = primer_producto.get('family', '')
                potencia = primer_producto.get('power', '')
                
                # Generar respuesta natural según el contexto
                if 'frio' in request.question.lower() or 'calefacción' in request.question.lower():
                    respuesta = f"Te recomiendo el {nombre}"
                    if familia:
                        respuesta += f" ({familia})"
                    if potencia:
                        respuesta += f", con {potencia} de potencia"
                    respuesta += ". ¿Querés más detalles?"
                elif 'caldera' in request.question.lower():
                    respuesta = f"Para calderas, te recomiendo el {nombre}. Es ideal para calefacción completa. ¿Te interesa?"
                elif 'radiador' in request.question.lower():
                    respuesta = f"Tengo el {nombre} que puede servirte. ¿Querés saber más?"
                else:
                    respuesta = f"Encontré el {nombre} que puede interesarte. ¿Querés más información?"
                    
                if len(top_items) > 1:
                    respuesta += f" También tengo otras {len(top_items)-1} opciones."
            else:
                respuesta = "¿Qué necesitás? ¿Calefacción para tu casa, radiadores, calderas, o piso radiante?"
        
        return ChatResponse(
            answer=respuesta,
            products=top_items if top_items else [],
            conversation_id=conversation_id
        )
    except Exception as e:
        print(f"[ERROR] Error crítico en chatbot: {e}")
        import traceback
        traceback.print_exc()
        # No lanzar error, devolver respuesta de fallback
        return ChatResponse(
            answer="Lo siento, estoy teniendo problemas técnicos. Por favor, intentá usar el sistema experto de cálculos o consultá con nuestro equipo de ventas.",
            products=[],
            conversation_id=request.conversation_id or f"chat_{int(time.time() * 1000)}"
        )

# Endpoint adicional para salud del servicio
@app.get("/health")
async def health_check():
    """Endpoint de verificación de salud del servicio"""
    return {"status": "ok", "service": "PEISA - SOLDASUR S.A"}

@app.get("/ask")
def ask(question: str = Query(..., min_length=5)):
    """Endpoint GET legacy para compatibilidad"""
    top_items = search_filtered(question, top_k=3)
    respuesta = answer(question, top_items)
    return {"respuesta": respuesta, "productos": top_items}


@app.get("/{resource_path:path}")
async def serve_static(resource_path: str):
    """Sirve archivos estáticos desde los directorios permitidos"""
    if not resource_path:
        raise HTTPException(status_code=404, detail="Not Found")
    
    # Primero, buscar en app/ (para CSS, JS, módulos, etc.)
    app_file = BASE_DIR / "app" / resource_path
    if app_file.is_file():
        return FileResponse(app_file)
    
    # Si empieza con /images/, buscar en la carpeta images de la raíz
    if resource_path.startswith("images/"):
        image_file = BASE_DIR / resource_path
        if image_file.is_file():
            return FileResponse(image_file)
    
    # Si empieza con /data/, buscar en la carpeta data de la raíz
    if resource_path.startswith("data/"):
        data_file = BASE_DIR / resource_path
        if data_file.is_file():
            return FileResponse(data_file)
    
    # Buscar en todas las carpetas como fallback
    for base_dir in STATIC_DIRECTORIES:
        candidate = base_dir / resource_path
        if candidate.is_file():
            return FileResponse(candidate)
    
    raise HTTPException(status_code=404, detail="Not Found")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)