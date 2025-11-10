import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

def obtener_respuesta(pregunta: str):
  llm = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), model="gpt-3.5-turbo")
  prompt = ChatPromptTemplate.from_template(
    "Eres un asistente informativo sobre sismos en Guatemala. "
    "Responde de forma clara, educativa y breve. Pregunta: {pregunta}"
  )
  chain = prompt | llm
  respuesta = chain.invoke({"pregunta": pregunta})
  return respuesta.content