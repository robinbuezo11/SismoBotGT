# app/routes/chatbot_routes.py
from fastapi import APIRouter, Request, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session

from app.services.sismos_service import obtener_sismos_recientes_usgs
from app.services.insivumeh_service import obtener_sismos_recientes_insivumeh
from app.services.chatbot_service import get_chatbot
from app.database.connection import get_db
from app.repositories.conversation_repository import save_conversation

import re

router = APIRouter()
chatbot = get_chatbot()

@router.post("/chat")
async def chat(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    user_message = data.get("message", "")
    user_id = data.get("user_id", "anonymous")

    if not user_message:
        raise HTTPException(status_code=400, detail="Mensaje no proporcionado")

    msg_lower = user_message.lower()

    # patrón: usuario pide sismos en Guatemala
    if re.search(r"\bsismos\b|\bstremor\b|\btemblor\b|\bactividad sísmica\b", msg_lower) and "guatemala" in msg_lower:
        # consultar USGS
        datos_usgs = obtener_sismos_recientes_usgs()
        # consultar INSIVUMEH
        datos_insivumeh = obtener_sismos_recientes_insivumeh()
        
        respuesta_sismos = {
            "usgs": datos_usgs,
            "insivumeh": datos_insivumeh
        }

        save_conversation(db, user_id, user_message, str(respuesta_sismos))
        return {
            "answer": respuesta_sismos
        }

    # para otras preguntas generamos conversación con memoria
    result = await chatbot.ainvoke(
        {"input": user_message},
        config={"configurable": {"session_id": user_id}}
    )
    # extraer sólo el texto
    content = result.content if hasattr(result, "content") else str(result)
    save_conversation(db, user_id, user_message, content)
    return {"answer": content}
