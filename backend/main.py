from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
from dotenv import load_dotenv
from . import functions

load_dotenv()

app = FastAPI(title="GlobalPath AI MVP Backend")

@app.on_event("startup")
def startup_event():
    functions.load_data()

# --- DATA MODELS ---
class ProfileRequest(BaseModel):
    Target_Degree: str
    Field_of_Study: str
    Preferred_Countries: str = "Any"
    CGPA: float
    IELTS_Band: float = 0.0

class ScholarshipResponse(BaseModel):
    Scholarship_ID: str
    Scholarship_Name: str
    Country: str
    Funding_Type: str
    Deadline: Optional[str] = None
    Score: float
    Score_Breakdown: Dict[str, int] = {}
    Why_Matched: str
    Eligible: bool = True
    Issues: Optional[str] = None

class AgentResponse(BaseModel):
    Name: str
    License: str
    Rating: float
    Trust_Score: int
    Complaints: int
    Details: str

class ApplicationRequest(BaseModel):
    Profile_ID: str
    Scholarship_ID: str

class ApplicationUpdate(BaseModel):
    Application_ID: str
    Status: str
    Notes: Optional[str] = ""

class SearchStats(BaseModel):
    rejected_cgpa: int = 0
    rejected_ielts: int = 0
    rejected_country: int = 0
    rejected_field: int = 0
    rejected_degree: int = 0
    unlock_ielts: int = 0  # Potential matches if IELTS is improved

class RecommendationsResponse(BaseModel):
    matches: List[ScholarshipResponse]
    stats: SearchStats

class InterviewPrepResponse(BaseModel):
    Category: str
    Question: str
    Official_Guidance: str

# --- STARTUP ---
@app.on_event("startup")
def startup_event():
    functions.load_data()

# --- ENDPOINTS ---

@app.get("/recommendations", response_model=List[ScholarshipResponse])
def get_recommendations_legacy(profile_id: str):
    """Legacy endpoint required for path /recommendations if mistakenly used as GET"""
    return []

@app.post("/recommendations", response_model=RecommendationsResponse)
def get_recommendations(request: ProfileRequest):
    """
    Generates scholarship recommendations based on provided profile data.
    Returns matches + search statistics.
    """
    
    # 1. Create Student Profile Dictionary
    # Construct student profile from request
    student = {
        "Target_Degree": request.Target_Degree, # Assuming user enters CGPA on 4.0 scale or %
        "Field_of_Study": request.Field_of_Study,
        "Preferred_Countries": request.Preferred_Countries,
        "CGPA": request.CGPA,
        "IELTS_Band": request.IELTS_Band
    }
    
    # 2. Match & Score (Now returns dict with 'matches' and 'stats')
    result = functions.match_and_score(student)
    matches = result.get('matches', [])
    stats = result.get('stats', {})
    
    # 3. Format Response
    formatted_matches = []
    for m in matches:
        formatted_matches.append(ScholarshipResponse(
            Scholarship_ID=str(m.get('Scholarship_ID', 'N/A')),
            Scholarship_Name=m['Scholarship_Name'],
            Country=m['Country'],
            Funding_Type=m['Funding_Type'],
            Deadline=m.get('Deadline'),
            Score=m['Score'],
            Score_Breakdown=m.get('Score_Breakdown', {}),
            Why_Matched=m['Reason'],
            Eligible=m.get('Eligible', True),
            Issues=m.get('Issues')
        ))
    
    return RecommendationsResponse(
        matches=formatted_matches,
        stats=SearchStats(**stats)
    )


@app.post("/applications/add")
def add_application_endpoint(app: ApplicationRequest):
    result = functions.add_application(app.Profile_ID, app.Scholarship_ID)
    return {"message": result}

@app.get("/applications/{profile_id}")
def get_applications_endpoint(profile_id: str):
    apps = functions.get_applications(profile_id)
    return apps

@app.put("/applications/update")
def update_application_endpoint(update: ApplicationUpdate):
    success = functions.update_application_status(update.Application_ID, update.Status, update.Notes)
    if success:
        return {"message": "Updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Application not found")

@app.get("/trusted-agents", response_model=List[AgentResponse])
def get_agents():
    """
    Returns list of trusted education agents.
    Filters: Status='Verified' AND Trust_Score >= 70.
    """
    agents = functions.get_trusted_agents()
    return agents

@app.get("/interview-prep", response_model=List[InterviewPrepResponse])
def get_interview_prep(category: Optional[str] = None):
    """
    Returns interview preparation questions.
    Optional Query Param: ?category=General
    """
    questions = functions.get_interview_prep(category)
    return questions

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    """
    Interacts with AI Assistant.
    """
    ai_response = functions.chat_with_ai(request.message)
    return ChatResponse(response=ai_response)
