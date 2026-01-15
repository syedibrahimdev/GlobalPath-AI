import streamlit as st

def apply_styles():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    /* Global Settings */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Background Gradient */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }

    /* Navbar Styling (Simulated) */
    .nav-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 2rem;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 2rem;
        border-radius: 0 0 16px 16px;
    }
    .nav-logo {
        font-size: 1.5rem;
        font-weight: 700;
        color: #38bdf8; /* Sky Blue */
    }
    .nav-links {
        display: flex;
        gap: 20px;
    }
    .nav-link {
        color: #e2e8f0;
        text-decoration: none;
        font-weight: 500;
        transition: color 0.3s;
    }
    .nav-link:hover {
        color: #38bdf8;
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        margin-bottom: 24px;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
        border-color: rgba(56, 189, 248, 0.5);
    }

    /* Metrics */
    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 16px;
        transition: all 0.3s ease;
    }
    div[data-testid="metric-container"]:hover {
        background: rgba(255, 255, 255, 0.08);
        border-color: #38bdf8;
    }
    label[data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
    }
    div[data-testid="stMetricValue"] {
        color: #f8fafc !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #0ea5e9 0%, #38bdf8 100%);
        color: white;
        border: none;
        padding: 0.6rem 1.2rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s;
        box-shadow: 0 4px 14px rgba(14, 165, 233, 0.4);
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #0284c7 0%, #0ea5e9 100%);
        box-shadow: 0 6px 20px rgba(14, 165, 233, 0.6);
        transform: scale(1.02);
    }
    .stButton > button:active {
        transform: scale(0.98);
    }

    /* Footer */
    .footer {
        text-align: center;
        margin-top: 4rem;
        padding: 2rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        color: #64748b;
        font-size: 0.9rem;
    }
    
    /* Utility */
    .text-gradient {
        background: linear-gradient(to right, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    input {
        background-color: rgba(255,255,255,0.05) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
    }
    
    /* HIDE SIDEBAR */
    [data-testid="stSidebar"] {
        display: none;
    }
    [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)

import base64
import os

def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception:
        return ""

def carousel(image_files):
    # CSS based infinite slider
    # We need to construct the HTML dynamically based on images
    
    slides_html = ""
    for img_file in image_files:
        if os.path.exists(img_file):
            b64_str = get_base64_image(img_file)
            slides_html += f'<div class="slide"><img src="data:image/png;base64,{b64_str}" alt="Study Abroad"></div>'
            
    # If no images, return empty
    if not slides_html:
        return

    # CSS for Slider
    # Keyframes for 5 images: 0%->20% (1), 20%->25% (move), 25%->45% (2)...
    # Simple continuous scroll or fading? Continuous scroll is easier for "Slider" feel.
    # Let's do a cross-fade or simple horizontal scroll.
    # Horizontal scroll involves duplication of slides for seamless loop.
    
    st.markdown("""
    <style>
    .slider-container {
        width: 100%;
        overflow: hidden;
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        margin-bottom: 2rem;
        position: relative;
    }
    
    .slider-track {
        display: flex;
        width: calc(100% * 5); /* 5 slides */
        animation: scroll 20s linear infinite;
    }
    
    .slide {
        width: 100%;
        flex-shrink: 0;
    }
    
    .slide img {
        width: 100%;
        height: 400px; /* Fixed height for consistency */
        object-fit: cover;
        display: block;
    }
    
    @keyframes scroll {
        0% { transform: translateX(0); }
        15% { transform: translateX(0); }
        20% { transform: translateX(-100%); }
        35% { transform: translateX(-100%); }
        40% { transform: translateX(-200%); }
        55% { transform: translateX(-200%); }
        60% { transform: translateX(-300%); }
        75% { transform: translateX(-300%); }
        80% { transform: translateX(-400%); }
        95% { transform: translateX(-400%); }
        100% { transform: translateX(0); } 
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="slider-container">
        <div class="slider-track">
            {slides_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

def navbar():
    # Functional Navbar with Streamlit Buttons
    # Force a container with explicit background to ensure visibility
    st.markdown("""
    <style>
    div[data-testid="stHorizontalBlock"] {
        align_items: center;
    }
    </style>
    """, unsafe_allow_html=True)
    
    with st.container():
        # Add a subtle border bottom manually in the layout
        c1, c2 = st.columns([1, 4])
        with c1:
             st.markdown('<div class="nav-logo" style="font-size: 24px;">🌍 GlobalPath AI</div>', unsafe_allow_html=True)
        with c2:
            # We use columns for buttons to simulate a navbar
            if 'user' in st.session_state and st.session_state['user']:
                # User Logged In
                b1, b2, b3, b4, b5, b6 = st.columns(6)
                if b1.button("Home", key="nav_home"): st.switch_page("Home.py")
                if b2.button("Scholarships", key="nav_sch"): st.switch_page("pages/1_Find_Scholarships.py")
                if b3.button("Agents", key="nav_agt"): st.switch_page("pages/2_Trusted_Agents.py")
                if b4.button("Interview", key="nav_int"): st.switch_page("pages/3_Interview_Preparation.py")
                if b5.button("AI Chat", key="nav_chat"): st.switch_page("pages/4_AI_Assistant.py")
                if b6.button("Tracker", key="nav_trac"): st.switch_page("pages/5_My_Applications.py")
            else:
                # User Logged Out - Explicitly show Home / Login button
                col_spacer, col_btn = st.columns([3, 1])
                with col_btn:
                    # Using a primary button to make it pop
                    if st.button("🏠 Home / Login", type="primary", key="nav_login_Main"):
                        st.switch_page("Home.py")
        
        st.markdown("<hr style='margin-top: 5px; margin-bottom: 20px; border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)

def glass_card(title, content, badges=None):
    st.markdown(f"""
    <div class="glass-card">
        <h3 style="color: #38bdf8; margin-bottom: 10px;">{title}</h3>
        <p style="color: #cbd5e1; line-height: 1.6;">{content}</p>
    </div>
    """, unsafe_allow_html=True)
