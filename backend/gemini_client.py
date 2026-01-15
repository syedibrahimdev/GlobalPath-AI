import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
API_KEY = os.getenv("GOOGLE_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)
    print(f"✅ Gemini API configured successfully")
else:
    print("⚠️ GOOGLE_API_KEY not found in .env file")

def get_chat_response(user_message):
    """
    Get AI response using Google Gemini Pro
    Works like ChatGPT - conversational and intelligent
    """
    
    if not API_KEY:
        return     
    try:
        # Create model
        model = genai.GenerativeModel('gemini-pro')
        
        # System context
        system_context = """You are a friendly and knowledgeable Study Abroad Assistant helping students from Pakistan, India, and Bangladesh.

**Your Expertise:**
- Student visas (UK, USA, Canada, Germany, Australia)
- University admissions and requirements
- Scholarships based on CGPA and budget
- IELTS/TOEFL preparation
- Cost estimates and financial planning
- Application processes

**How to Respond:**
- Be conversational like ChatGPT
- Understand both English and Roman Urdu
- If asked in Roman Urdu, respond in Roman Urdu
- Ask follow-up questions to give better advice
- Give specific, detailed answers
- Never guarantee visa approval
- Warn about fake consultants

**Examples:**
User: "Mera CGPA 3.0 hai, kaunsi scholarship mil sakti hai?"
You: "CGPA 3.0 ke saath aapko ye scholarships mil sakti hain:
- Commonwealth Scholarship (UK)
- Erasmus Mundus (Europe)
- University-specific scholarships

Aap kis country mein jaana chahte hain? Aur aapka IELTS score kya hai?"

User: "UK ka visa kab milta hai?"
You: "UK student visa (Tier 4) milne mein usually 3-4 weeks lagte hain. Process:
1. University se CAS letter lo
2. Online application bharo
3. Biometrics appointment
4. Documents submit karo
5. 15-20 working days mein decision

Aapne university mein admission le liya hai?"""

        # Create chat with context
        chat = model.start_chat(history=[])
        
        # Send message with context
        full_prompt = f"{system_context}\n\nUser: {user_message}\nAssistant:"
        response = chat.send_message(full_prompt)
        
        return response.text
        
    except Exception as e:
        error_str = str(e)
        print(f"❌ Gemini Error: {error_str}")
        
        # Handle specific errors
        if "API" in error_str or "key" in error_str.lower():
            return """⚠️ API key issue detected.

Get a free Google API key:
1. Visit: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key
4. Add to .env file: GOOGLE_API_KEY=your_key_here
5. Restart the server

The key is 100% free with 60 requests per minute!"""
        
        elif "quota" in error_str.lower():
            return "⏳ API limit reached. Please wait a minute and try again."
        
        else:
            return f"""I'm having trouble connecting to the AI service right now.

Error: {error_str[:100]}

Please try again in a moment, or ask a basic question about:
- Visa requirements
- Scholarships
- University costs"""
