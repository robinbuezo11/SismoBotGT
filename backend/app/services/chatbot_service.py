# app/services/chatbot_service.py
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from app.core.config import settings
from app.core.prompts import base_prompt

_history_store: dict[str, BaseChatMessageHistory] = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in _history_store:
        class InMemoryHistory(BaseChatMessageHistory):
            messages: list = []
            def add_messages(self, msgs):
                self.messages.extend(msgs)
            def clear(self):
                self.messages = []
        _history_store[session_id] = InMemoryHistory()
    return _history_store[session_id]

def get_chatbot():
    llm = ChatGroq(
        model=settings.MODEL_NAME,
        api_key=settings.GROQ_API_KEY,
        temperature=0.7,
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", base_prompt["content"]),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])

    base_chain = prompt | llm

    chatbot = RunnableWithMessageHistory(
        base_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history",
    )

    return chatbot
