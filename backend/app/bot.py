from collections import deque
from dataclasses import dataclass
from typing import Deque, Dict, List, Tuple
from .config import settings


class WhatsEaseBot:
    def __init__(self):
        self.bot_id = settings.BOT_IDENTIFIER
        self.name = "WhatsEase"
        self.intents = {
            "hi": ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"],
            "help": ["help", "support", "assist", "guide", "what can you do"],
            "bye": ["bye", "goodbye", "see you", "farewell", "take care"],
            "thanks": ["thank you", "thanks", "appreciate it", "grateful"],
            "weather": ["weather", "temperature", "forecast", "climate"],
            "joke": ["joke", "funny", "humor", "laugh"],
            "time": ["time", "clock", "hour", "schedule"],
            "name": ["what's your name", "who are you", "your name"],
            "capabilities": ["what can you do", "your features", "capabilities", "skills"]
        }
        
        self.responses = {
            "hi": [
                "Hello! How can I help you today?",
                "Hi there! Welcome to WhatsEase. How may I assist you?",
                "Hey! Great to see you. What can I do for you?",
                "Good day! I'm here to help. What do you need?"
            ],
            "help": [
                "I can answer your questions, chat with you, and help with various topics!",
                "I'm here to assist you with information, conversation, and general help.",
                "I can help with questions, provide information, or just chat with you!",
                "I'm your AI assistant. I can help with queries, chat, and more!"
            ],
            "bye": [
                "Goodbye! Have a great day!",
                "See you later! Take care!",
                "Farewell! It was nice chatting with you!",
                "Bye! Come back anytime!"
            ],
            "thanks": [
                "You're welcome! Happy to help!",
                "No problem at all! Anytime!",
                "My pleasure! Let me know if you need anything else!",
                "Glad I could help! Feel free to ask more questions!"
            ],
            "weather": [
                "I can't check real-time weather, but I can chat about weather in general!",
                "Weather forecasting isn't my specialty, but I'm happy to discuss weather topics!",
                "I don't have access to current weather data, but I can help with other questions!"
            ],
            "joke": [
                "Why don't scientists trust atoms? Because they make up everything! 😄",
                "What do you call a fake noodle? An impasta! 😂",
                "Why did the scarecrow win an award? He was outstanding in his field! 🌾",
                "I told my wife she was drawing her eyebrows too high. She looked surprised! 😲"
            ],
            "time": [
                "I can't tell you the exact time, but I can help you with time-related questions!",
                "I don't have access to real-time clocks, but I can discuss time concepts!",
                "Time management isn't my forte, but I can help with other topics!"
            ],
            "name": [
                f"I'm {self.name}, your AI assistant!",
                f"My name is {self.name}. I'm here to help you!",
                f"I'm called {self.name}. How can I assist you today?",
                f"You can call me {self.name}. What do you need help with?"
            ],
            "capabilities": [
                "I can chat, answer questions, provide information, and assist with various topics!",
                "My skills include conversation, information sharing, and general assistance!",
                "I'm capable of helping with queries, engaging in chat, and providing support!",
                "I can assist with questions, have conversations, and help with information!"
            ]
        }
        
        self.fallback_responses = [
            "I'm not sure I understand that. Could you rephrase or ask something else?",
            "That's beyond my current capabilities. Can I help you with something else?",
            "I didn't quite catch that. Maybe try asking in a different way?",
            "I'm still learning and don't understand that yet. What else can I help you with?"
        ]

    def get_response(self, message: str) -> str:
        """Generate a response based on user input."""
        message_lower = message.lower().strip()
        
        # Check for exact matches first
        for intent, keywords in self.intents.items():
            if message_lower in keywords:
                import random
                return random.choice(self.responses[intent])
        
        # Check for partial matches
        for intent, keywords in self.intents.items():
            for keyword in keywords:
                if keyword in message_lower:
                    import random
                    return random.choice(self.responses[intent])
        
        # Fallback response
        import random
        return random.choice(self.fallback_responses)

    def respond(self, user_email: str, message: str) -> str:
        """Legacy method for backward compatibility."""
        return self.get_response(message)


# Create bot instance
bot = WhatsEaseBot()


