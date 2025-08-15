from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, users, messages, activity
from .database import engine, Base
from .sio import sio
import socketio

app = FastAPI(title="WhatsEase API", version="1.0.0")

# Create database tables
Base.metadata.create_all(bind=engine)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(messages.router, prefix="/messages", tags=["messages"])
app.include_router(activity.router, prefix="/activity", tags=["activity"])

# Socket.IO app
sio_app = socketio.ASGIApp(sio, app)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "WhatsEase API is running!"}

# Favicon endpoint to prevent 404 errors
@app.get("/favicon.ico")
async def favicon():
    return {"message": "No favicon"}


