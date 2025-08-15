from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas import UserOut, UserInbox
from ..deps import get_current_user
from ..database import get_db_session
from ..models import User, Message, MessageStatus
from typing import List

router = APIRouter()

@router.get("/me", response_model=UserOut)
async def get_current_user_info(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    user = db.query(User).filter(User.email == current_user).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@router.get("", response_model=List[UserInbox])
async def get_users(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    """Get all users for the inbox (excluding current user) with unread counts"""
    users = db.query(User).filter(User.email != current_user).all()
    result: List[UserInbox] = []
    for u in users:
        unread = db.query(Message).filter(
            Message.sender == u.email,
            Message.recipient == current_user,
            Message.status != MessageStatus.READ
        ).count()
        result.append(UserInbox(email=u.email, unread=unread))
    return result


