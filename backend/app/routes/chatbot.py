from fastapi import APIRouter
from pydantic import BaseModel
from app.services.langchain_engine import obtener_respuesta
from app.services.sismos_service import obtener_sismos_recientes

router = APIRouter(tags=["Chatbot"])

class Consulta(BaseModel):
  mensaje: str

@router.post("/chat")
def chat_endpoint(consulta: Consulta):
  mensaje = consulta.mensaje.lower()

  if "sismo" in mensaje or "temblor" in mensaje:
    datos = obtener_sismos_recientes()
    return {"respuesta": datos}

  respuesta = obtener_respuesta(mensaje)
  return {"respuesta": respuesta}