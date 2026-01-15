import pandas as pd
import os
import uuid
from typing import List, Dict, Optional

# Global Data Store
DATA_STORE = {}
# Use absolute path relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')

def load_data():
    """Loads all Excel datasets into the global DATA_STORE."""
    global DATA_STORE
    files = {
        'scholarships': 'scholarships.xlsx',
        'students': 'student_profiles.xlsx',
        'recommendations': 'recommendations.xlsx',
        'agents': 'agents.xlsx',
        'interview_prep': 'interview_prep.xlsx',
        'applications': 'applications.xlsx',
        'faqs': 'faq_knowledgebase.xlsx'
    }
    
    print(f"Loading data from: {os.path.abspath(DATA_DIR)}")
    for key, filename in files.items():
        try:
            path = os.path.join(DATA_DIR, filename)
            if os.path.exists(path):
                DATA_STORE[key] = pd.read_excel(path)
                print(f"Loaded {key}: {len(DATA_STORE[key])} records")
            else:
                print(f"Warning: {filename} not found at {path}")
                DATA_STORE[key] = pd.DataFrame()
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            DATA_STORE[key] = pd.DataFrame()

def save_data(key: str, df: pd.DataFrame):
    """Saves a specific dataframe back to its Excel file."""
    files = {
        'recommendations': 'recommendations.xlsx'
    }
    if key in files:
        path = os.path.join(DATA_DIR, files[key])
        df.to_excel(path, index=False)
        DATA_STORE[key] = df # Update memory
        print(f"Saved {key} to {path}")

def get_student_profile(profile_id: str) -> Optional[pd.Series]:
    """Fetches a student profile by ID."""
    students = DATA_STORE.get('students')
    if students is None or students.empty:
        return None
    
    student = students[students['Profile_ID'] == profile_id]
    if student.empty:
        return None
    return student.iloc[0]

def match_and_score(student: pd.Series) -> Dict:
    """
    Matches student to scholarships and calculates scores & stats.
    Returns: Dict containing 'matches' (list) and 'stats' (dict).
    """
    scholarships = DATA_STORE.get('scholarships')
    if scholarships is None or scholarships.empty:
        return {"matches": [], "stats": {}}

    matches = []
    
    # Stats Counters
    stats = {
        "rejected_cgpa": 0,
        "rejected_ielts": 0,
        "rejected_country": 0,
        "rejected_field": 0,
        "rejected_degree": 0,
        "unlock_ielts": 0
    }

    # Pre-process student attributes
    target_degree = str(student.get('Target_Degree', '')).strip().lower()
    field_of_study = str(student.get('Field_of_Study', '')).strip().lower()
    preferred_countries = str(student.get('Preferred_Countries', '')).lower()
    student_cgpa = float(student.get('CGPA', 0))
    student_ielts = float(student.get('IELTS_Band', 0))

    for _, sch in scholarships.iterrows():
        score = 0
        breakdown = {
            "Degree Match": 0,
            "Field Match": 0,
            "Country Preference": 0,
            "CGPA": 0,
            "IELTS": 0,
            "Funding Type": 0
        }
        reasons = []
        eligibility_issues = []
        
        # --- SCORING (not filtering) ---
        
        # 1. Degree Level Match (+30)
        sch_degree = str(sch.get('Degree_Level', '')).strip().lower()
        if sch_degree == target_degree:
            score += 30
            breakdown["Degree Match"] = 30
            reasons.append("Degree Match")
        else:
            stats["rejected_degree"] += 1
            continue 
        
        # 2. Field Match (+25)
        sch_field = str(sch.get('Field', '')).strip().lower()
        if field_of_study in sch_field or sch_field in field_of_study:
            score += 25
            breakdown["Field Match"] = 25
            reasons.append("Field Match")
        else:
            score += 5  # Partial score for same degree level
            breakdown["Field Match"] = 5
            eligibility_issues.append(f"Field mismatch (requires {sch.get('Field', 'N/A')})")
            stats["rejected_field"] += 1
        
        # 3. Country Preference (+15)
        sch_country = str(sch.get('Country', '')).strip().lower()
        if 'any' in preferred_countries or sch_country in preferred_countries:
            score += 15
            breakdown["Country Preference"] = 15
            reasons.append(f"Country: {sch.get('Country')}")
        else:
            eligibility_issues.append(f"Country mismatch (requires {sch.get('Country')})")
            stats["rejected_country"] += 1
        
        # 4. CGPA Check (+20 if met, flag if not)
        min_cgpa = float(sch.get('Min_CGPA', 0))
        if min_cgpa > 0:
            if student_cgpa >= min_cgpa:
                score += 20
                breakdown["CGPA"] = 20
                reasons.append("CGPA Qualified")
            else:
                eligibility_issues.append(f"CGPA below {min_cgpa} (yours: {student_cgpa})")
                stats["rejected_cgpa"] += 1
        else:
            score += 10
            breakdown["CGPA"] = 10 # No requirement bonus
        
        # 5. IELTS Check (+10 if met or not required)
        ielts_req = str(sch.get('IELTS_Required', 'No')).strip()
        min_ielts = float(sch.get('Min_IELTS_Band', 0))
        
        passed_ielts = False
        if ielts_req.lower() == 'no':
            score += 10
            breakdown["IELTS"] = 10
            reasons.append("No IELTS Required")
            passed_ielts = True
        elif student_ielts >= min_ielts:
            score += 10
            breakdown["IELTS"] = 10
            reasons.append("IELTS Qualified")
            passed_ielts = True
        else:
            eligibility_issues.append(f"IELTS below {min_ielts} (yours: {student_ielts})")
            stats["rejected_ielts"] += 1
            
            # Check Potential: If only IELTS failed, this is an Unlock opportunity
            # Assuming strictly that if they improve IELTS they might get it (ignoring other fails for simple heuristic)
            if min_ielts <= 7.5: # Realistic improvement target
                stats["unlock_ielts"] += 1

        # 6. Funding Type Bonus (+10)
        funding = str(sch.get('Funding_Type', '')).lower()
        if 'fully funded' in funding:
            score += 10
            breakdown["Funding Type"] = 10
            reasons.append("Fully Funded")
        
        # Determine eligibility status
        is_eligible = len(eligibility_issues) == 0
        
        matches.append({
            "Scholarship_ID": sch['Scholarship_ID'],
            "Scholarship_Name": sch['Scholarship_Name'],
            "Country": sch['Country'],
            "Funding_Type": sch['Funding_Type'],
            "Deadline": sch.get('Deadline', 'Open'),
            "Score": score,
            "Score_Breakdown": breakdown,
            "Reason": ", ".join(reasons) if reasons else "Potential match",
            "Eligible": is_eligible,
            "Issues": "; ".join(eligibility_issues) if eligibility_issues else None
        })

    # Sort by Score Descending
    matches.sort(key=lambda x: x['Score'], reverse=True)
    
    return {"matches": matches[:10], "stats": stats}

def save_recommendations(profile_id: str, matches: List[Dict]):
    """Saves matched scholarships to recommendations.xlsx"""
    if not matches:
        return

    existing_recs = DATA_STORE.get('recommendations')
    new_rows = []
    
    for rank, match in enumerate(matches, 1):
        new_rows.append({
            'Match_ID': str(uuid.uuid4()),
            'Profile_ID': profile_id,
            'Scholarship_ID': match['Scholarship_ID'],
            'Score': match['Score'],
            'Rank': rank,
            'Matched_On': pd.Timestamp.now(),
            'Reasoning': match['Reason'],
            'Sent_To_User': False,
            'User_Feedback': ''
        })
    
    new_df = pd.DataFrame(new_rows)
    updated_df = pd.concat([existing_recs, new_df], ignore_index=True)
    save_data('recommendations', updated_df)

def get_trusted_agents():
    """Fetches verified agents with high trust scores."""
    df = DATA_STORE.get('agents')
    if df is None or df.empty:
        return []

    # Logic: Status == 'Active' or 'Verified' AND Trust_Score >= 70
    mask = (df['Status'].isin(['Active', 'Verified'])) & (df['Trust_Score'] >= 70)
    filtered = df[mask].copy()

    # Sort: Trust_Score DESC, Rating DESC
    filtered.sort_values(by=['Trust_Score', 'Rating'], ascending=[False, False], inplace=True)
    
    # Return specific columns
    result = filtered[['Name', 'License', 'Rating', 'Trust_Score', 'Complaints', 'Details']]
    return result.to_dict(orient='records')

def get_interview_prep(category: Optional[str] = None):
    """Fetches interview preparation questions."""
    df = DATA_STORE.get('interview_prep')
    if df is None or df.empty:
        return []

    if category:
        filtered = df[df['Category'].str.lower() == category.lower()]
    else:
        filtered = df

    return filtered[['Category', 'Question', 'Official_Guidance']].to_dict(orient='records')

def chat_with_ai(user_message: str):
    """
    Sends message to Google Gemini API with robust error handling.
    """
    try:
        # Note: We are now using backend/ai_engine.py for chat
        from .ai_engine import get_chat_response
        return get_chat_response(user_message)
        
        api_key = os.environ.get("GEMINI_API_KEY")
        
        if not api_key or "YOUR_API_KEY" in api_key:
            return "⚠️ System Alert: GEMINI_API_KEY is missing or invalid. Please update the .env file."

        client = genai.Client(api_key=api_key)
        
        # 1. Prepare Context from FAQs
        faqs_df = DATA_STORE.get('faqs')
        context_str = ""
        if faqs_df is not None and not faqs_df.empty:
            context_list = []
            for _, row in faqs_df.iterrows():
                q = str(row.get('Question', ''))
                a = str(row.get('Answer', ''))
                if q and a:
                    context_list.append(f"Q: {q}\nA: {a}")
            context_str = "\n\n".join(context_list[:50]) # Limit context
        
        # 2. Construct System Prompt
        system_instruction = f"""
You are GlobalPath AI, an expert education consultant engine.
Your goal is to assist students with accurate, official information.

RULES:
1. STRICTLY answer based ONLY on the provided Knowledge Base below.
2. If the answer is not in the Knowledge Base, you MUST say: "I don't have verified information for that."
3. DO NOT hallucinate or invent scholarships, deadlines, or requirements.
4. DO NOT offer legal or visa guarantees.
5. Provide clear, concise, and empathetic responses.

KNOWLEDGE BASE:
{context_str}
"""
        
        # 3. Generate Content
        # Using a simple prompt structure for maximum compatibility
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"{system_instruction}\n\nSTUDENT QUESTION: {user_message}"
        )
        
        if response.text:
            return response.text
        else:
            return "I received an empty response from the AI server."
        
    except ImportError:
        return "Critical Error: 'google-genai' library not found. Please run `pip install google-genai`."
    except Exception as e:
        print(f"AI Error details: {e}")
        return f"I am unable to connect to the AI service right now. Error: {str(e)}"

# --- APPLICATION TRACKING ---

def add_application(profile_id: str, scholarship_id: str) -> str:
    """Adds a new application record if it doesn't exist."""
    df = DATA_STORE.get('applications')
    if df is None:
        df = pd.DataFrame(columns=['Application_ID', 'Profile_ID', 'Scholarship_ID', 'Status', 'Applied_On', 'Notes'])

    # Check for duplicates
    # Convert IDs to string to ensure matching works
    df['Profile_ID'] = df['Profile_ID'].astype(str)
    df['Scholarship_ID'] = df['Scholarship_ID'].astype(str)
    
    duplicate = df[(df['Profile_ID'] == str(profile_id)) & (df['Scholarship_ID'] == str(scholarship_id))]
    
    if not duplicate.empty:
        return "Already added to your tracker."

    # Create new record
    new_app = {
        'Application_ID': str(uuid.uuid4()),
        'Profile_ID': str(profile_id),
        'Scholarship_ID': str(scholarship_id),
        'Status': 'Interested',
        'Applied_On': pd.Timestamp.now().strftime('%Y-%m-%d'), 
        'Notes': ''
    }
    
    print(f"DEBUG: Adding application for {profile_id} - {scholarship_id}")
    
    # Append safely
    updated_df = pd.concat([df, pd.DataFrame([new_app])], ignore_index=True)
    DATA_STORE['applications'] = updated_df
    
    # Save to file
    path = os.path.join(DATA_DIR, 'applications.xlsx')
    print(f"DEBUG: Saving to {path}. Total rows: {len(updated_df)}")
    
    try:
        updated_df.to_excel(path, index=False)
        print("DEBUG: Save success.")
    except Exception as e:
        print(f"DEBUG: Save failed: {e}")
    
    return "Scholarship added to your tracker successfully."

def get_applications(profile_id: str):
    """Fetches applications for a profile, joined with Scholarship details."""
    apps_df = DATA_STORE.get('applications')
    sch_df = DATA_STORE.get('scholarships')
    
    if apps_df is None or apps_df.empty:
        return []
    
    # Filter by user
    user_apps = apps_df[apps_df['Profile_ID'] == str(profile_id)].copy()
    
    if user_apps.empty:
        return []
    
    # Merge with Scholarships to get Name/Country
    # Ensure Scholarship_ID types match
    user_apps['Scholarship_ID'] = user_apps['Scholarship_ID'].astype(str)
    sch_df['Scholarship_ID'] = sch_df['Scholarship_ID'].astype(str)
    
    merged = pd.merge(user_apps, sch_df[['Scholarship_ID', 'Scholarship_Name', 'Country']], 
                      on='Scholarship_ID', how='left')
    
    # Fill N/A for display
    merged['Scholarship_Name'] = merged['Scholarship_Name'].fillna('Unknown Scholarship')
    merged['Country'] = merged['Country'].fillna('Unknown')
    merged['Notes'] = merged['Notes'].fillna('')
    
    return merged.to_dict(orient='records')

def update_application_status(app_id: str, status: str, notes: str):
    """Updates status and notes of an application."""
    df = DATA_STORE.get('applications')
    if df is None or df.empty:
        return False
        
    mask = df['Application_ID'] == str(app_id)
    if not df[mask].any():
        return False
        
    # Update Status
    df.loc[mask, 'Status'] = status
    df.loc[mask, 'Notes'] = notes
    
    # Update Date if Applied
    if status == 'Applied':
        df.loc[mask, 'Applied_On'] = pd.Timestamp.now().strftime('%Y-%m-%d')
        
    # Save
    DATA_STORE['applications'] = df
    path = os.path.join(DATA_DIR, 'applications.xlsx')
    df.to_excel(path, index=False)
    
    return True

