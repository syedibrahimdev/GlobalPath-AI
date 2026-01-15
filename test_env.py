from dotenv import load_dotenv
import os

# Try loading from current directory (root)
load_dotenv()

key = os.environ.get("GEMINI_API_KEY")
print(f"Loaded key: {key}")

if not key:
    print("Trying explicit path...")
    load_dotenv(".env")
    key = os.environ.get("GEMINI_API_KEY")
    print(f"Loaded key with explicit path: {key}")
