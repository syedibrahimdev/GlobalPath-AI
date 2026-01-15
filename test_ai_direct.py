from backend.ai_engine import get_chat_response
import sys

try:
    print("Testing AI Engine...")
    response = get_chat_response("Batao UK ka visa kaise milega?")
    print("-" * 20)
    print(f"AI Response: {response}")
    print("-" * 20)
except Exception as e:
    print(f"Test Failed: {e}")
