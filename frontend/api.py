import requests
import streamlit as st

BASE_URL = "http://127.0.0.1:8002"

def get_recommendations(target_degree: str, field_of_study: str, countries: str, cgpa: float, ielts: float):
    """Fetches scholarship recommendations and stats for a profile."""
    try:
        payload = {
            "Target_Degree": target_degree,
            "Field_of_Study": field_of_study,
            "Preferred_Countries": countries,
            "CGPA": cgpa,
            "IELTS_Band": ielts
        }
        response = requests.post(f"{BASE_URL}/recommendations", json=payload)
        response.raise_for_status()
        return response.json() # Returns {'matches': [], 'stats': {}}
    except requests.exceptions.HTTPError as e:
        st.error(f"Error connecting to backend: {e}")
        return []
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to backend: {e}")
        return []

def get_trusted_agents():
    """Fetches list of trusted agents."""
    try:
        response = requests.get(f"{BASE_URL}/trusted-agents")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to backend: {e}")
        return []

def get_interview_prep(category: str = None):
    """Fetches interview preparation questions."""
    params = {}
    if category and category != "All":
        params["category"] = category
        
    try:
        response = requests.get(f"{BASE_URL}/interview-prep", params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to backend: {e}")
        return []

def send_chat_message(message: str) -> str:
    """Sends a user message to the AI Assistant backend and returns the response."""
    try:
        response = requests.post(f"{BASE_URL}/chat", json={"message": message})
        response.raise_for_status()
        return response.json().get("response", "No response from AI.")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to AI service: {e}")
        return "I am having trouble connecting to the server right now. Please try again later."

# --- APPLICATION TRACKING ---

def add_application(profile_id: str, scholarship_id: str):
    """Adds a scholarship to the user's application tracker."""
    try:
        response = requests.post(f"{BASE_URL}/applications/add", json={
            "Profile_ID": str(profile_id),
            "Scholarship_ID": str(scholarship_id)
        })
        response.raise_for_status()
        return response.json().get("message", "Success")
    except requests.exceptions.RequestException as e:
        st.error(f"Error adding application: {e}")
        return "Failed to add application."

def get_applications(profile_id: str):
    """Fetches user's tracked applications."""
    try:
        response = requests.get(f"{BASE_URL}/applications/{profile_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching applications: {e}")
        return []

def update_application_status(app_id: str, status: str, notes: str):
    """Updates status and notes for an application."""
    try:
        payload = {
            "Application_ID": str(app_id),
            "Status": status,
            "Notes": notes
        }
        response = requests.put(f"{BASE_URL}/applications/update", json=payload)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"Error updating application: {e}")
        return False
