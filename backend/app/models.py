from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
import enum

class MessageStatus(str, enum.Enum):
    SENT = "Sent"
    DELIVERED = "Delivered"
    READ = "Read"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String, nullable=False, index=True)
    recipient = Column(String, nullable=False, index=True)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(Enum(MessageStatus), default=MessageStatus.SENT)
    is_bot_response = Column(Boolean, default=False)

class ActivityLog(Base):
    __tablename__ = "activity_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, nullable=False, index=True)
    action = Column(String, nullable=False)
    details = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


