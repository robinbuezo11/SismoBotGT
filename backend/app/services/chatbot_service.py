from langchain_groq import ChatGroq

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

from app.core.config import settings
from app.core.prompts import base_prompt

MAX_HISTORY_MODEL = settings.MAX_HISTORY_MODEL

store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()

    history = store[session_id]

    if len(history.messages) > MAX_HISTORY_MODEL:
        history.messages = history.messages[-MAX_HISTORY_MODEL:]

    return history

def get_chatbot():
    llm = ChatGroq(
        model=settings.MODEL_NAME,
        api_key=settings.GROQ_API_KEY,
        temperature=0.5,
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", base_prompt["content"]),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])

    chain = prompt | llm

    chatbot = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history",
    )

    return chatbot
