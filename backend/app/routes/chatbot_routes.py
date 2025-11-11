from pyexpat.errors import messages
from urllib import response
from fastapi import APIRouter, Request
from app.services.chatbot_service import get_chatbot
from app.services.sismos_service import obtener_sismos_recientes
from app.core.prompts import base_prompt

router = APIRouter()
chatbot = get_chatbot()

@router.post("/chat")
async def chat(request: Request):
  data = await request.json()
  user_message = data.get("message", "")

  if "sismo" in user_message.lower() or "temblor" in user_message.lower():
    datos = obtener_sismos_recientes()
    return {"answer": datos}

  messages = [
    ("system", base_prompt["content"]),
    ("user", user_message)
  ]
  
  ai_msg = chatbot.invoke(messages)
  content = ai_msg.content if hasattr(ai_msg, "content") else str(ai_msg)

  return {
    "answer": (
      content
    )
  }