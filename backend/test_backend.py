from fastapi.testclient import TestClient
from main import app
import functions
import sys
import os

# Add backend directory to path so we can import from main
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Explicitly load data to ensure shared state is populated
functions.load_data()

client = TestClient(app)

def test_trusted_agents():
    print("\nTesting GET /trusted-agents...")
    response = client.get("/trusted-agents")
    assert response.status_code == 200
    agents = response.json()
    print(f"Received {len(agents)} agents.")
    if agents:
        print(f"Sample Agent: {agents[0]['Name']} (Trust Score: {agents[0]['Trust_Score']})")
        assert agents[0]['Trust_Score'] >= 70
    print("Passed.")

def test_interview_prep():
    print("\nTesting GET /interview-prep...")
    response = client.get("/interview-prep?category=Visa Interview")
    assert response.status_code == 200
    questions = response.json()
    print(f"Received {len(questions)} questions.")
    if questions:
        print(f"Sample Question: {questions[0]['Question']}")
    print("Passed.")

def test_recommendations():
    print("\nTesting POST /recommendations...")
    payload = {"Profile_ID": "PROF-001"}
    response = client.post("/recommendations", json=payload)
    
    if response.status_code != 200:
        print(f"Failed: {response.text}")
        
    assert response.status_code == 200
    recs = response.json()
    print(f"Received {len(recs)} recommendations.")
    if recs:
        top_rec = recs[0]
        print(f"Top Match: {top_rec['Scholarship_Name']}")
        print(f"Score: {top_rec['Score']}")
        print(f"Reason: {top_rec['Why_Matched']}")
        
        # Validation checks
        assert "Score" in top_rec
        assert "Why_Matched" in top_rec
    print("Passed.")

if __name__ == "__main__":
    try:
        test_trusted_agents()
        test_interview_prep()
        test_recommendations()
        print("\nAll Backend Tests Passed Successfully!")
    except Exception as e:
        print(f"\nTest Failed: {e}")
        exit(1)
