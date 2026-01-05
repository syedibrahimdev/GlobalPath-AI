import streamlit as st
import uuid
from frontend.styles import apply_styles
from frontend.api import get_applications, update_application_status

st.set_page_config(page_title="My Applications", page_icon="📋", layout="wide")
apply_styles()

st.title("📋 Application Tracker")
st.markdown("Track the status of your scholarship applications here.")

# --- SESSION ID LOGIC ---
if 'user_id' not in st.session_state:
    st.info("You haven't started a session yet. Go to 'Find Scholarships' and add an application first!")
    st.stop()
    
user_id = st.session_state['user_id']

# --- FETCH DATA ---
apps = get_applications(user_id)

if not apps:
    st.info("Your tracker is empty. Go and find some scholarships!")
else:
    # --- DASHBOARD METRICS ---
    col1, col2, col3, col4 = st.columns(4)
    status_counts = {}
    for a in apps:
        s = a.get('Status', 'Interested')
        status_counts[s] = status_counts.get(s, 0) + 1
        
    col1.metric("Interested", status_counts.get("Interested", 0))
    col2.metric("Applied", status_counts.get("Applied", 0))
    col3.metric("Shortlisted", status_counts.get("Shortlisted", 0))
    col4.metric("Rejected", status_counts.get("Rejected", 0))
    
    st.markdown("---")
    
    # --- TABLE VIEW ---
    for app in apps:
        app_id = app.get('Application_ID')
        sch_name = app.get('Scholarship_Name', 'Unknown')
        status = app.get('Status', 'Interested')
        notes = app.get('Notes', '')
        date = app.get('Applied_On', '')
        
        # Color Code
        status_color = "#888"
        if status == "Applied": status_color = "#4285F4" # Blue
        elif status == "Shortlisted": status_color = "#0F9D58" # Green
        elif status == "Rejected": status_color = "#DB4437" # Red
        
        with st.container():
            c1, c2, c3 = st.columns([3, 2, 1])
            
            with c1:
                st.subheader(sch_name)
                st.caption(f"Country: {app.get('Country', 'Unknown')}")
                # Visual Badge
                st.markdown(f'<span style="background-color: {status_color}; padding: 4px 8px; border-radius: 4px; color: white; font-weight: bold;">{status}</span>', unsafe_allow_html=True)
                if status == "Applied":
                    st.caption(f"Applied On: {date}")
            
            with c2:
                # Update Form
                with st.expander("Update Status / Notes"):
                    new_status = st.selectbox("Status", ["Interested", "Applied", "Shortlisted", "Rejected"], 
                                             index=["Interested", "Applied", "Shortlisted", "Rejected"].index(status),
                                             key=f"st_{app_id}")
                    new_notes = st.text_area("Notes", value=notes, key=f"nt_{app_id}", height=100)
                    
                    if st.button("Save Changes", key=f"sv_{app_id}"):
                        if update_application_status(app_id, new_status, new_notes):
                            st.success("Saved!")
                            st.rerun()
            
            with c3:
                if status == "Shortlisted":
                    st.balloons()
            
            st.markdown("---")
