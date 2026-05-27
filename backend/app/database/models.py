from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from sqlalchemy.sql import func

from app.database.connection import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(255), index=True)
    user_message = Column(Text, nullable=False)
    bot_response = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class CachedEarthquake(Base):
    __tablename__ = "cached_earthquakes"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(100))
    magnitude = Column(Float)
    location = Column(String(255))
    depth_km = Column(Float)
    event_time = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())