import json

from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session

from app.services.sismos_service import obtener_sismos_recientes_usgs
from app.services.insivumeh_service import obtener_sismos_recientes_insivumeh
from app.services.chatbot_service import get_chatbot
from app.services.intention_service import detect_intent
from app.services.response_builder import construir_contexto_sismico

from app.database.connection import get_db
from app.repositories.conversation_repository import save_conversation

from app.utils.country_detector import detect_country

router = APIRouter()
chatbot = get_chatbot()

@router.post("/chat")
async def chat(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    
    user_message = data.get("message", "")
    user_id = data.get("user_id", "anonymous")

    if not user_message:
        raise HTTPException(status_code=400, detail="Mensaje no proporcionado")

    intent = detect_intent(user_message)
    if intent == "consulta_sismos":
        pais_detectado = detect_country(user_message)
        
        datos_usgs = obtener_sismos_recientes_usgs(pais_detectado)

        datos_insivumeh = None
        if pais_detectado.lower() == "guatemala":
            datos_insivumeh = obtener_sismos_recientes_insivumeh()

        contexto_sismico = construir_contexto_sismico(datos_usgs, datos_insivumeh)

        prompt_sismico = f"""
            Consulta del usuario:
            "{user_message}"

            Contexto sísmico disponible:
            {contexto_sismico}

            Instrucciones IMPORTANTES:

            - No inventes sismos.
            - No inventes magnitudes.
            - No inventes fechas.
            - No inventes ubicaciones.
            - Si la información no existe en el contexto, dilo claramente.
            - No agregues ejemplos ficticios.
            - No inventes datos faltantes.
            - No repitas eventos.
            - Si es alguna consulta general, respondela pero con bases claras, sin inventar y de forma académica y profesional.

            Responde en Markdown.
        """

        result = await chatbot.ainvoke(
            {"input": prompt_sismico},
            config={"configurable": {"session_id": user_id}}
        )

        content = result.content if hasattr(result, "content") else str(result)

        save_conversation(db, user_id, user_message, content)

        return {
            "answer": content,
            "metadata": {
                "tipo": "sismos",
                "pais": pais_detectado.title(),
                "fuentes": ["USGS", "INSIVUMEH"] if datos_insivumeh else ["USGS"]
            }
        }

    result = await chatbot.ainvoke(
        {"input": user_message},
        config={"configurable": {"session_id": user_id}}
    )
    
    content = result.content if hasattr(result, "content") else str(result)
    save_conversation(db, user_id, user_message, content)
    return {"answer": content}
