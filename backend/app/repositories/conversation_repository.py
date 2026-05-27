from sqlalchemy.orm import Session
from app.database.models import Conversation

def save_conversation(
    db: Session,
    session_id: str,
    user_message: str,
    bot_response: str
):
    conversation = Conversation(
        session_id=session_id,
        user_message=user_message,
        bot_response=bot_response
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    
    return conversation