import streamlit as st

def apply_styles():
    st.markdown("""
    <style>
    /* Global Styling */
    .stApp {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* Metrics Styling */
    div[data-testid="metric-container"] {
        background-color: #262730;
        border: 1px solid #464b5f;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
    }
    
    /* Card Styling for Scholarships/Agents */
    .card {
        background-color: #1E1E1E;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        border-left: 5px solid #FF4B4B; /* Streamlit Red Accent */
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .card h3 {
        margin-top: 0;
        color: #FAFAFA;
    }
    .card p {
        color: #E0E0E0;
        margin-bottom: 5px;
    }
    .card .badge {
        background-color: #31333F;
        color: #FF4B4B;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.8em;
        font-weight: bold;
        margin-right: 5px;
    }
    
    /* Header Styling */
    h1, h2, h3 {
        color: #FAFAFA;
    }
    
    /* Button Styling */
    .stButton > button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

def card(title, content, badges=None):
    badge_html = ""
    if badges:
        for b in badges:
            badge_html += f'<span class="badge">{b}</span>'
            
    st.markdown(f"""
    <div class="card">
        <h3>{title}</h3>
        <div>{badge_html}</div>
        <div style="margin-top: 10px;">
            {content}
        </div>
    </div>
    """, unsafe_allow_html=True)
