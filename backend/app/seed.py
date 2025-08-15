from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .models import Base, User, Message, ActivityLog, MessageStatus
from .security import get_password_hash
from datetime import datetime, timedelta, timezone

def seed_database():
    """Seed the database with initial data."""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Clear existing data
        db.query(ActivityLog).delete()
        db.query(Message).delete()
        db.query(User).delete()
        
        # Create demo users
        users_data = [
            {
                "email": "alice@example.com",
                "password": "Password@123"
            },
            {
                "email": "bob@example.com", 
                "password": "Password@123"
            },
            {
                "email": "charlie@example.com",
                "password": "Password@123"
            }
        ]
        
        users = []
        for user_data in users_data:
            try:
                hashed_password = get_password_hash(user_data["password"])
                user = User(
                    email=user_data["email"],
                    hashed_password=hashed_password
                )
                db.add(user)
                users.append(user)
            except Exception as e:
                print(f"Warning: Could not create user {user_data['email']}: {e}")
                continue
        
        db.commit()
        
        # Create sample messages
        messages_data = [
            {
                "sender": "alice@example.com",
                "recipient": "bob@example.com",
                "content": "Hey Bob! How are you doing?",
                "status": MessageStatus.READ,
                "is_bot_response": False
            },
            {
                "sender": "bob@example.com",
                "recipient": "alice@example.com", 
                "content": "Hi Alice! I'm doing great, thanks for asking!",
                "status": MessageStatus.DELIVERED,
                "is_bot_response": False
            },
            {
                "sender": "alice@example.com",
                "recipient": "whatsease_bot",
                "content": "Hello bot!",
                "status": MessageStatus.READ,
                "is_bot_response": False
            },
            {
                "sender": "whatsease_bot",
                "recipient": "alice@example.com",
                "content": "Hello! How can I help you today?",
                "status": MessageStatus.READ,
                "is_bot_response": True
            }
        ]
        
        for msg_data in messages_data:
            message = Message(
                sender=msg_data["sender"],
                recipient=msg_data["recipient"],
                content=msg_data["content"],
                status=msg_data["status"],
                is_bot_response=msg_data["is_bot_response"],
                timestamp=datetime.now(timezone.utc) - timedelta(hours=1)
            )
            db.add(message)
        
        # Create activity logs
        activities_data = [
            {
                "user_email": "alice@example.com",
                "action": "user_registered",
                "details": "Alice registered for the first time"
            },
            {
                "user_email": "bob@example.com",
                "action": "user_registered", 
                "details": "Bob registered for the first time"
            },
            {
                "user_email": "alice@example.com",
                "action": "message_sent",
                "details": "Alice sent a message to Bob"
            },
            {
                "user_email": "bob@example.com",
                "action": "message_sent",
                "details": "Bob replied to Alice"
            },
            {
                "user_email": "alice@example.com",
                "action": "bot_interaction",
                "details": "Alice started a conversation with WhatsEase bot"
            }
        ]
        
        for activity_data in activities_data:
            activity = ActivityLog(
                user_email=activity_data["user_email"],
                action=activity_data["action"],
                details=activity_data["details"],
                timestamp=datetime.now(timezone.utc) - timedelta(hours=1)
            )
            db.add(activity)
        
        db.commit()
        print("Database seeded successfully!")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()


