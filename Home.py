import streamlit as st
from frontend.styles import apply_styles, card
import pandas as pd

# Page Config
st.set_page_config(
    page_title="GlobalPath AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed" 
)

apply_styles()

# --- HEADER SECTION ---
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🎓 GlobalPath AI</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #FAFAFA; font-weight: normal;'>Your Intelligent Companion for Study Abroad Success</h3>", unsafe_allow_html=True)
st.markdown("---")

# --- VISITOR STATE LOGIC ---
# We check if user has 'user_id' (assigned in Find Scholarships) to determine if they are new or returning
is_returning = 'user_id' in st.session_state

# --- HERO / ACTION SECTION ---
col_hero_L, col_hero_M, col_hero_R = st.columns([1, 2, 1])

with col_hero_M:
    if not is_returning:
        # NEW USER VIEW
        st.markdown(
            """
            <div style="text-align: center; padding: 20px; background: #262730; border-radius: 10px; border: 1px solid #4CAF50;">
                <h2 style="color: #FAFAFA;">Where do you want to study?</h2>
                <p style="color: #DDD;">Our AI analyzes 1000+ scholarships to find your perfect match in seconds.</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        st.write("") # Spacer
        # Primary CTA
        if st.button("🚀 Find My Scholarship Matches", use_container_width=True, type="primary"):
            st.switch_page("pages/1_Find_Scholarships.py")
            
        st.markdown("<div style='text-align: center; font-size: 12px; color: #888; margin-top: 10px;'>Free assessment • No login required • Instant results</div>", unsafe_allow_html=True)
        
    else:
        # RETURNING USER VIEW (DASHBOARD)
        st.markdown(
            """
            <div style="text-align: center; padding: 20px; background: #1E1E1E; border-radius: 10px; border-left: 5px solid #FFD700;">
                <h2 style="color: #FFD700;">Welcome Back! 🎓</h2>
                <p style="color: #DDD;">Here is the progress of your application journey.</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # Dashboard Metrics
        m1, m2, m3 = st.columns(3)
        
        # Get actual counts if possible, else mock or session state
        app_count = 0
        if 'user_id' in st.session_state:
             # Logic to fetch could go here, but for MVP Home we keep it simple or fetch
             pass

        m1.metric("Scholarships Found", "Checking...", delta="Active")
        m2.metric("Applications Tracked", "View", delta="In Progress")
        m3.metric("Interview Prep", "Level 1", delta="Beginner")
        
        if st.button("📊 Go to My Tracker", use_container_width=True):
            st.switch_page("pages/5_My_Applications.py")

st.write("")
st.write("")

# --- FEATURE PREVIEW SECTION ---
st.markdown("### 🛠️ Everything You Need in One Place")
f1, f2, f3, f4 = st.columns(4)

with f1:
    st.markdown("#### 🎯 Smart Matching")
    st.caption("Custom algorithm directly matches your CGPA & IELTS to strict scholarship requirements.")
    if st.button("Find Scholarships"):
         st.switch_page("pages/1_Find_Scholarships.py")

with f2:
    st.markdown("#### 🤝 Trusted Agents")
    st.caption("Verify education consultants. Check ratings, trust scores, and hidden complaints.")
    if st.button("Verify Agents"):
         st.switch_page("pages/2_Trusted_Agents.py")

with f3:
    st.markdown("#### 🎤 Interview Coach")
    st.caption("Practice real visa & admission questions. Get model answers and tips.")
    if st.button("Start Practicing"):
         st.switch_page("pages/3_Interview_Preparation.py")

with f4:
    st.markdown("#### 📋 App Tracker")
    st.caption("Kanban-style board to manage deadlines, statuses, and documents.")
    if st.button("Manage Apps"):
         st.switch_page("pages/5_My_Applications.py")

st.markdown("---")

# --- TRUST & TRANSPARENCY SECTION ---
with st.container():
    st.markdown("### 🛡️ Trust & Transparency")
    t1, t2 = st.columns([3, 1])
    
    with t1:
        st.info("""
        **Our Commitment to You:**
        *   **Zero-Bias Recommendations**: We do not accept payments to rank scholarships higher.
        *   **Data Privacy**: All profile data is processed locally for the session. We do not sell your data.
        *   **No Guarantees**: GlobalPath AI provides guidance based on official data, but admission and visa decisions are solely up to the respective authorities.
        """)
    
    with t2:
        # Chatbot entry point
        with st.expander("💬 Need Help?"):
            st.write("Our AI Assistant can answer FAQs about scholarships and process.")
            if st.button("Chat with AI"):
                st.switch_page("pages/4_AI_Assistant.py")

# --- FOOTER ---
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 12px; margin-top: 50px;'>
        GlobalPath AI MVP • Built for Students • Non-Binding Advice
    </div>
    """,
    unsafe_allow_html=True
)
