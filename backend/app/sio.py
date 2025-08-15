import socketio
from sqlalchemy.orm import Session
from .database import SessionLocal
from .security import decode_access_token
from .bot import bot
from .models import Message, MessageStatus, ActivityLog
from .config import settings

sio = socketio.AsyncServer(
    cors_allowed_origins="*",
    async_mode="asgi"
)

def get_db():
    db = SessionLocal()
    try:
        return db
    except Exception:
        db.close()
        raise

class AuthServerNamespace(socketio.AsyncNamespace):
    async def on_connect(self, sid, environ, auth=None):
        token = None
        # 1) Prefer Socket.IO auth payload
        if isinstance(auth, dict):
            token = auth.get("token")
        # 2) Fallback to query string token
        if not token:
            query = environ.get("QUERY_STRING", "")
            for part in query.split("&"):
                if part.startswith("token="):
                    token = part.split("=", 1)[1]
                    break
        user_email = decode_access_token(token) if token else None
        if not user_email:
            return False  # reject
        self.server.save_session(sid, {"user": user_email})
        await self.enter_room(sid, f"user:{user_email}")
        print(f"User {user_email} connected")
        return True

    async def on_disconnect(self, sid):
        session = self.server.get_session(sid)
        if session and "user" in session:
            user_email = session["user"]
            await self.leave_room(sid, f"user:{user_email}")
            print(f"User {user_email} disconnected")

    async def on_send_message(self, sid, data):
        session = self.server.get_session(sid)
        if not session or "user" not in session:
            return
        
        sender_email = session["user"]
        recipient = data.get("recipient")
        content = data.get("content")
        
        if not recipient or not content:
            return
        
        # Save message to SQLite
        db = get_db()
        try:
            message = Message(
                sender=sender_email,
                recipient=recipient,
                content=content
            )
            
            db.add(message)
            db.commit()
            db.refresh(message)
            
            # Log activity
            activity = ActivityLog(
                user_email=sender_email,
                action="message_sent",
                details=f"{sender_email} -> {recipient}: {content[:50]}"
            )
            db.add(activity)
            db.commit()
            
            # Echo message back to sender
            await self.emit("message", {
                "id": message.id,
                "sender": message.sender,
                "recipient": message.recipient,
                "content": message.content,
                "timestamp": message.timestamp.isoformat(),
                "status": message.status.value,
                "is_bot_response": message.is_bot_response
            }, room=f"user:{sender_email}")
            
            # Check if recipient is online
            recipient_room = f"user:{recipient}"
            if recipient_room in self.server.rooms:
                # Recipient is online, send message and mark as delivered
                await self.emit("message", {
                    "id": message.id,
                    "sender": message.sender,
                    "recipient": message.recipient,
                    "content": message.content,
                    "timestamp": message.timestamp.isoformat(),
                    "status": "Delivered",
                    "is_bot_response": message.is_bot_response
                }, room=recipient_room)
                
                # Update status to delivered
                message.status = MessageStatus.DELIVERED
                db.commit()

            # Emit updated unread count to recipient
            try:
                unread_count = db.query(Message).filter(
                    Message.sender == sender_email,
                    Message.recipient == recipient,
                    Message.status != MessageStatus.READ
                ).count()
                await self.emit("unread", {
                    "peer": sender_email,
                    "unread": unread_count,
                }, room=recipient_room)
            except Exception:
                pass
            
            # Check if recipient is bot
            if recipient == settings.BOT_IDENTIFIER:
                await self.handle_bot_response(sender_email, content, message.id)
                
        finally:
            db.close()

    async def handle_bot_response(self, user_email: str, user_message: str, message_id: int):
        """Handle bot responses to user messages."""
        bot_response = bot.get_response(user_message)
        
        db = get_db()
        try:
            # Create bot response message
            bot_message = Message(
                sender=settings.BOT_IDENTIFIER,
                recipient=user_email,
                content=bot_response,
                is_bot_response=True
            )
            
            db.add(bot_message)
            db.commit()
            db.refresh(bot_message)
            
            # Log bot activity
            activity = ActivityLog(
                user_email=settings.BOT_IDENTIFIER,
                action="bot_response",
                details=f"Bot responded to {user_email}: {bot_response[:50]}"
            )
            db.add(activity)
            db.commit()
            
            # Send bot response to user
            await self.emit("message", {
                "id": bot_message.id,
                "sender": bot_message.sender,
                "recipient": bot_message.recipient,
                "content": bot_message.content,
                "timestamp": bot_message.timestamp.isoformat(),
                "status": bot_message.status.value,
                "is_bot_response": bot_message.is_bot_response
            }, room=f"user:{user_email}")
            
        finally:
            db.close()

    async def on_mark_read(self, sid, data):
        """Mark messages as read."""
        session = self.server.get_session(sid)
        if not session or "user" not in session:
            return
        
        user_email = session["user"]
        message_id = data.get("message_id")
        
        if not message_id:
            return
        
        db = get_db()
        try:
            # Find and update message status
            message = db.query(Message).filter(
                Message.id == message_id,
                Message.recipient == user_email
            ).first()
            
            if message:
                message.status = MessageStatus.READ
                db.commit()
                
                # Notify sender that message was read
                await self.emit("status", {
                    "message_id": message_id,
                    "status": "Read"
                }, room=f"user:{message.sender}")

                # Notify recipient (the reader) with updated unread count for this peer
                unread_remaining = db.query(Message).filter(
                    Message.sender == message.sender,
                    Message.recipient == user_email,
                    Message.status != MessageStatus.READ
                ).count()
                await self.emit("unread", {
                    "peer": message.sender,
                    "unread": unread_remaining,
                }, room=f"user:{user_email}")
                
        finally:
            db.close()

# Register namespace
sio.register_namespace(AuthServerNamespace("/"))


