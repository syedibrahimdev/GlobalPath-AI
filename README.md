# 🌍 GlobalPath AI

**Your Intelligent Companion for Study Abroad Success.**

GlobalPath AI is a student-centric platform designed to simplify the complex journey of studying abroad. From finding the perfect scholarship to tracking applications and verifying agents, we provide AI-powered guidance every step of the way.

## 🚀 Key Features

### 1. 🎓 Smart Scholarship Matching
- **Personalized Search**: Matches students based on Degree, Field, CGPA, and IELTS score.
- **Strict Eligibility**: Filters out scholarships you don't qualify for.
- **Score Breakdown**: Transparently shows why a scholarship matched (e.g., "Degree Match: +30", "Field Match: +25").
- **Zero-Match Analytics**: Provides reasons for rejection and "Smart Tips" to improve your profile.

### 2. 📋 Application Tracker (Kanban Style)
- **One-Click Add**: Easily add scholarships from search results to your tracker.
- **Visual Dashboard**: Track status (Interested, Applied, Shortlisted, Rejected).
- **Deadlines & Notes**: Keep all your application details in one place.

### 3. 🤝 Trusted Agents Directory
- **Safety First**: Strictly filters for **Active** agents with a **Trust Score ≥ 70**.
- **Transparency**: High-visibility warnings for agents with complaints.
- **Verification**: Check license numbers and read service details before contacting.
- **Dashboard**: Search, Sort (by Rating/Trust), and Filter verified agents.

### 4. 🎤 AI Interview Coach
- **Official Questions**: Practice real visa and admission interview questions.
- **Category Filters**: General, Visa, Academic, Financial.
- **Progress Tracking**: Mark questions as "Practiced" or "Save for Later".

### 5. 🤖 AI Assistant (Gemini Powered)
- **24/7 Support**: Ask questions about scholarships, visas, and documentation.
- **No Hallucinations**: Strictly grounded in our knowledge base.
- **Safe & Ethical**: Does not offer legal guarantees or biased agent recommendations.

---

## 🛠️ Technology Stack

- **Frontend**: [Streamlit](https://streamlit.io/) - For a responsive, interactive student dashboard.
- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) - High-performance API for logistics and data handling.
- **AI Engine**: [Google Gemini](https://deepmind.google/technologies/gemini/) - For intelligent chat and guidance.
- **Data**: Pandas & Excel-based lightweight database (MVP).

---

## 📦 Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/syedibrahimdev/GlobalPath-AI.git
    cd GlobalPath-AI
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set Up Environment Variables**
    Create a `.env` file in the root directory and add your Gemini API Key:
    ```env
    GEMINI_API_KEY=your_api_key_here
    ```

4.  **Run the Application**
    Start both the Backend and Frontend:
    
    **Terminal 1 (Backend):**
    ```bash
    python -m uvicorn backend.main:app --host 127.0.0.1 --port 8002 --reload
    ```

    **Terminal 2 (Frontend):**
    ```bash
    streamlit run Home.py --server.port 8502
    ```

5.  **Access the App**
    Open your browser and navigate to: `http://localhost:8502`

---

## 🛡️ Disclaimer

*GlobalPath AI is a guidance tool. We do not guarantee admission or visa approval. All scholarship data and agent details should be verified with official sources.*

---

© 2026 GlobalPath AI. Built for the Future of Education.
