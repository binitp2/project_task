from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from ..schemas import MessageCreate, MessageOut
from ..deps import get_current_user
from ..database import get_db_session
from ..models import Message, MessageStatus, ActivityLog
from ..config import settings
from ..bot import bot
from datetime import datetime, timezone

router = APIRouter()

@router.get("", response_model=List[MessageOut])
async def get_messages(
    peer: str,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    # Get messages between current user and peer
    messages = db.query(Message).filter(
        ((Message.sender == current_user) & (Message.recipient == peer)) |
        ((Message.sender == peer) & (Message.recipient == current_user))
    ).order_by(Message.timestamp.asc()).all()
    
    return messages

@router.post("", response_model=MessageOut)
async def create_message(
    message_data: MessageCreate,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    # Validate recipient
    if message_data.recipient != settings.BOT_IDENTIFIER:
        # Basic email validation
        if "@" not in message_data.recipient:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid recipient email"
            )
    
    # Create user message
    message = Message(
        sender=current_user,
        recipient=message_data.recipient,
        content=message_data.content,
        timestamp=datetime.now(timezone.utc)
    )
    
    db.add(message)
    db.commit()
    db.refresh(message)
    
    # Log activity for message sent
    activity = ActivityLog(
        user_email=current_user,
        action="message_sent",
        details=f"{current_user} sent a message to {message_data.recipient}: {message_data.content[:50]}",
        timestamp=datetime.now(timezone.utc)
    )
    db.add(activity)
    
    # If message is to bot, generate and save bot response
    if message_data.recipient == settings.BOT_IDENTIFIER:
        bot_response = bot.get_response(message_data.content)
        bot_message = Message(
            sender=settings.BOT_IDENTIFIER,
            recipient=current_user,
            content=bot_response,
            timestamp=datetime.now(timezone.utc),
            is_bot_response=True
        )
        db.add(bot_message)
        
        # Log bot activity
        bot_activity = ActivityLog(
            user_email=settings.BOT_IDENTIFIER,
            action="bot_response",
            details=f"Bot responded to {current_user}: {bot_response[:50]}",
            timestamp=datetime.now(timezone.utc)
        )
        db.add(bot_activity)
    
    db.commit()
    
    return message


