import streamlit as st
from frontend.styles import apply_styles, card, navbar
from frontend.api import get_interview_prep

st.set_page_config(page_title="Interview Prep", page_icon="🎤", layout="wide", initial_sidebar_state="collapsed")
apply_styles()
navbar()

st.title("🎤 Interview Preparation")
st.markdown("Practice with official questions and master your scholarship interview.")

# --- SESSION STATE ---
if 'practiced' not in st.session_state:
    st.session_state['practiced'] = set()
if 'saved' not in st.session_state:
    st.session_state['saved'] = set()

# --- FETCH DATA ---
# Fetch ALL questions to handle client-side filtering and stats
with st.spinner("Loading questions..."):
    all_questions = get_interview_prep()

if not all_questions:
    st.warning("No interview questions available at the moment.")
    st.stop()

# --- PROGRESS STATS (Moved from Sidebar) ---
total_q = len(all_questions)
practiced_count = len(st.session_state['practiced'])
saved_count = len(st.session_state['saved'])

with st.container():
    c1, c2, c3 = st.columns(3)
    c1.metric("Questions Practiced", f"{practiced_count} / {total_q}")
    c2.progress(min(practiced_count / total_q if total_q > 0 else 0, 1.0))
    c3.metric("Saved for Later", saved_count)
st.write("---")

# --- FILTERS ---
# Extract unique categories dynamically
unique_cats = sorted(list(set(q.get('Category', 'General') for q in all_questions)))
filter_options = ["All Categories"] + unique_cats + ["🔖 Saved Questions"]

selected_filter = st.selectbox("Filter by Category", filter_options)

# --- FILTERING LOGIC ---
display_questions = []
if selected_filter == "🔖 Saved Questions":
    display_questions = [q for q in all_questions if q['Question'] in st.session_state['saved']]
elif selected_filter == "All Categories":
    display_questions = all_questions
else:
    display_questions = [q for q in all_questions if q.get('Category') == selected_filter]

# --- RENDER QUESTIONS ---
st.markdown(f"### {len(display_questions)} Questions")

for i, q in enumerate(display_questions):
    q_text = q.get('Question', 'Unknown Question')
    guidance = q.get('Official_Guidance', 'No guidance available.')
    category = q.get('Category', 'General')
    
    # Card Content
    result_card = st.container()
    
    with result_card:
        # Custom styling for the "card" look
        colA, colB = st.columns([0.85, 0.15])
        
        with colA:
            st.markdown(f"#### {q_text}")
            st.caption(f"Category: {category}")
            with st.expander("👁️ Show Official Guidance"):
                st.info(guidance)
        
        with colB:
            st.write("Actions:")
            
            # STATE SYNC Logic
            is_practiced = q_text in st.session_state['practiced']
            is_saved = q_text in st.session_state['saved']
            
            # Checkboxes
            # Note: We use the question text hash for unique keys
            k_hash = abs(hash(q_text))
            
            check_p = st.checkbox("✅ Done", value=is_practiced, key=f"p_{k_hash}")
            check_s = st.checkbox("🔖 Save", value=is_saved, key=f"s_{k_hash}")
            
            # Update State based on interaction
            if check_p:
                st.session_state['practiced'].add(q_text)
            else:
                st.session_state['practiced'].discard(q_text)
                
            if check_s:
                st.session_state['saved'].add(q_text)
            else:
                st.session_state['saved'].discard(q_text)
    
    st.markdown("---")

if len(display_questions) == 0:
    st.info("No questions found for this filter.")
