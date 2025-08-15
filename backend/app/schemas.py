from pydantic import BaseModel, ConfigDict, validator
from typing import Optional, List
from datetime import datetime
from .models import MessageStatus

class Token(BaseModel):
    access_token: str
    token_type: str

class UserCreate(BaseModel):
    email: str
    password: str
    
    model_config = ConfigDict(extra="forbid")
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least 1 number')
        # More comprehensive special character check
        special_chars = '!@#$%^&*()_+-=[]{}|;:,.<>?'
        if not any(c in special_chars for c in v):
            raise ValueError(f'Password must contain at least 1 special character from: {special_chars}')
        return v

class UserLogin(BaseModel):
    email: str
    password: str
    
    model_config = ConfigDict(extra="forbid")

class UserOut(BaseModel):
    id: int
    email: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Lightweight user for inbox with unread counts
class UserInbox(BaseModel):
    email: str
    unread: int

class MessageCreate(BaseModel):
    recipient: str
    content: str
    
    model_config = ConfigDict(extra="forbid")
    
    @validator('recipient')
    def validate_recipient(cls, v):
        if not v or v.strip() == "":
            raise ValueError('Recipient cannot be empty')
        return v

class MessageOut(BaseModel):
    id: int
    sender: str
    recipient: str
    content: str
    timestamp: datetime
    status: MessageStatus
    is_bot_response: bool
    
    model_config = ConfigDict(from_attributes=True)

class ActivityOut(BaseModel):
    id: int
    user_email: str
    action: str
    details: str
    timestamp: datetime
    
    model_config = ConfigDict(from_attributes=True)

class MessagesResponse(BaseModel):
    messages: List[MessageOut]
    total: int


