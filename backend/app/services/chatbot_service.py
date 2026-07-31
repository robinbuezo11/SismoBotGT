from langchain_groq import ChatGroq

from langchain_core.messages import trim_messages
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

from app.core.config import settings
from app.core.prompts import base_prompt

import tiktoken

encoding = tiktoken.get_encoding("cl100k_base")

def count_tokens(messages):
    return sum(len(encoding.encode(message.content)) for message in messages)

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
        max_tokens=800,
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", base_prompt["content"]),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])

    chain = prompt | llm

    def get_trimmed_history(session_id: str):
        if session_id not in store:
            store[session_id] = ChatMessageHistory()

        history = store[session_id]

        history.messages = trim_messages(
            history.messages,
            max_tokens=3500,
            strategy="last",
            token_counter=count_tokens,
        )

        return history

    chatbot = RunnableWithMessageHistory(
        chain,
        get_trimmed_history,
        input_messages_key="input",
        history_messages_key="history",
    )

    return chatbot
