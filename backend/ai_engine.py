import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_chat_response(user_message):
    """
    Get AI response using Gemini 1.5 Flash.
    Optimized for speed and intelligence.
    """
    api_key = "AIzaSyB8KpVDEjZ-QMcyAiLsPcVr2WMj6Z0DyDA" # Provided by user
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-flash-latest')
        
        system_instruction = """
        You are GlobalPath AI, an expert study abroad consultant. 
        Your goal is to provide detailed, helpful, and conversational responses to student queries regarding admissions, visas (UK, USA, Canada, Germany, Europe), and scholarships.
        
        - Respond in the language used by the student (English or Roman Urdu).
        - Provide comprehensive information like ChatGPT.
        - Be proactive in offering advice, but don't force specific data collection (like CGPA) unless it's necessary to answer the user's specific question.
        - Focus on being a useful consultant who answers questions directly.
        """
        
        # Combine system instruction with user message
        prompt = f"{system_instruction}\n\nUser: {user_message}\nAssistant:"
        
        response = model.generate_content(prompt)
        return response.text.strip()
        
    except Exception as e:
        print(f"AI Error: {e}")
        return get_expert_fallback(user_message)

def get_expert_fallback(message):
    """
    Highly detailed fallback that doesn't feel static.
    """
    msg = message.lower()
    is_urdu = any(word in msg for word in ["kya", "hai", "kaise", "mein", "kab", "may", "batein"])
    
    # Extract keywords
    target_country = "UK" if "uk" in msg else "Canada" if "canada" in msg else "Germany" if "germany" in msg else "the USA" if "usa" in msg else "abroad"
    
    if is_urdu:
        return f"Maine aapka sawal '{message}' samajh liya hai. UK ke visa aur admission ke liye aapka academic background kafi matter karta hai. Aap mazeed kya janna chahte hain?"
    
    return f"I understand your query about '{message}'. For {target_country}, you need specific documents like CAS or I-20. How can I assist you further with your study abroad application?"
