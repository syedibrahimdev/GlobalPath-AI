from backend.ai_engine import get_chat_response
import sys

msg = "Uk ka vise kb milta hay?"
print(f"User: {msg}")
reply = get_chat_response(msg)
print(f"AI: {reply}")
