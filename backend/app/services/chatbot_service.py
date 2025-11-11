from langchain_groq import ChatGroq
from app.core.config import settings

def get_chatbot():
    llm = ChatGroq(
        model=settings.MODEL_NAME,
        api_key=settings.GROQ_API_KEY,
    )

    return llm