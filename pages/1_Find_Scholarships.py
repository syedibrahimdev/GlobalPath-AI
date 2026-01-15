import streamlit as st
from frontend.styles import apply_styles, card, navbar
from frontend.api import get_recommendations

st.set_page_config(page_title="Find Scholarships", page_icon="🎓", layout="wide", initial_sidebar_state="collapsed")
apply_styles()
navbar()

st.title("🎓 Find Scholarships")
st.markdown("Enter your academic details below to find the best matching scholarships.")

# --- INPUT SECTION ---
with st.container():
    st.info("🎓 **Enter your academic details to get personalized scholarship recommendations.**")
    
    col1, col2 = st.columns(2)
    with col1:
        current_education = st.selectbox("Current Education Level", ["High School", "Bachelors", "Masters"], index=1)
        target_degree = st.selectbox("Target Degree", ["Bachelors", "Masters", "PhD"], index=1)
        
    with col2:
        field_of_study = st.text_input("Field of Study", placeholder="e.g. Computer Science, Business")
        cgpa = st.number_input("CGPA / Percentage", min_value=0.0, max_value=100.0, value=3.0, step=0.01, help="Enter CGPA (Scale 4.0) or Percentage")

    preferred_countries = st.multiselect("Preferred Countries", ["USA", "UK", "Germany", "Canada", "Australia", "Any"], default=["Any"])
    
    # IELTS Section with Conditional Logic
    st.write("---")
    st.write("📝 **Language Proficiency**")
    has_ielts = st.radio("Do you have an IELTS score?", ["No", "Yes"], horizontal=True)
    
    ielts_band = 0.0
    if has_ielts == "Yes":
        ielts_band = st.number_input("IELTS Band Score", min_value=1.0, max_value=9.0, value=6.5, step=0.5)
    
    st.write("") # Spacer
    search_btn = st.button("🔍 Find Matching Scholarships", type="primary", use_container_width=True)

# --- RESULTS SECTION ---
if search_btn:
    # Validation
    if not field_of_study.strip():
        st.error("⚠️ **Field of Study** is required.")
    elif cgpa <= 0:
        st.error("⚠️ **CGPA/Percentage** must be greater than 0.")
    elif has_ielts == "Yes" and ielts_band == 0:
        st.error("⚠️ Please enter a valid **IELTS Band Score**.")
    else:
        # Prepare Countries String
        countries_str = ", ".join(preferred_countries) if preferred_countries else "Any"
        
        with st.spinner("Analyzing your profile and matching scholarships..."):
            api_response = get_recommendations(
                target_degree=target_degree, 
                field_of_study=field_of_study, 
                countries=countries_str, 
                cgpa=cgpa, 
                ielts=ielts_band
            )
        
        # Handle API Error
        if api_response and "error" in api_response:
             st.error(f"Error: {api_response.get('detail') or api_response.get('error')}")
             
        # Extract Data
        result = api_response.get('matches', []) if api_response else []
        stats = api_response.get('stats', {}) if api_response else {}
        
        # Determine if we have any ELIGIBLE results
        eligible_matches = [m for m in result if m.get('Eligible', True)]
        eligible_count = len(eligible_matches)
        
        def render_scholarship(match, idx=0):
            """Render a single scholarship card"""
            badges = [match.get('Funding_Type', 'Funded'), match.get('Country', 'Global')]
            score = match.get('Score', 0)
            is_eligible = match.get('Eligible', True)
            issues = match.get('Issues')
            deadline = match.get('Deadline', 'Open')
            
            if is_eligible:
                badges.insert(0, "✅ Eligible")
            else:
                badges.insert(0, "⚠️ Not Eligible")
            
            if score > 80:
                badges.insert(0, "⭐ Top Match")
            
            # Convert comma-separated reasons to bullet points
            raw_reasons = match.get('Why_Matched', '').split(', ')
            bullets_html = "".join([f"<li>{r}</li>" for r in raw_reasons if r])
            
            # Content HTML with eligibility info
            eligibility_note = ""
            if not is_eligible and issues:
                eligibility_note = f'<div style="background: #3d2020; color: white; padding: 8px; border-radius: 4px; margin-top: 8px;"><small>⚠️ {issues}</small></div>'
            
            content = f"""<div>
    <div style="display: flex; justify_content: space-between; margin-bottom: 5px;">
        <b>Match Score: {score}</b>
        <span style="color: #ff4b4b;">⏳ Deadline: {deadline}</span>
    </div>
    <div style="margin-bottom: 5px;">
        <b>Why you are eligible:</b>
        <ul style="margin-top: 5px; margin-bottom: 5px; padding-left: 20px; color: #bbb;">
            {bullets_html}
        </ul>
    </div>
    {eligibility_note}
</div>"""
            
            card(match.get('Scholarship_Name', 'Scholarship'), content, badges)
            
            # ACTIONS ROW
            col_actions, col_details = st.columns([1, 1])
            
            with col_details:
                # Score Breakdown Toggle
                with st.expander("📊 View Score Details"):
                    breakdown = match.get('Score_Breakdown', {})
                    if not breakdown:
                        st.write("No details available.")
                    else:
                        for category, points in breakdown.items():
                            col_name, col_points = st.columns([3, 1])
                            col_name.write(category)
                            if points > 0:
                                col_points.write(f"**+{points}**")
                            else:
                                col_points.write("0")
            
            with col_actions:
                # Add to Applications
                # Use session state to simulate user ID for MVP
                if 'user_id' not in st.session_state:
                    import uuid
                    st.session_state['user_id'] = str(uuid.uuid4())[:8] # Short mock ID
                
                # Checkbox style button or simple button
                # Use a unique key for the button
                btn_key = f"apply_{match.get('Scholarship_ID')}_{idx}"
                if st.button("➕ Add to My Tracker", key=btn_key):
                    from frontend.api import add_application
                    result_msg = add_application(st.session_state['user_id'], match.get('Scholarship_ID'))
                    if "successfully" in result_msg:
                        st.success(result_msg)
                    else:
                        st.info(result_msg)

        if eligible_count > 0:
            # --- SUCCESS STATE ---
            st.success(f"Found {len(result)} scholarships! ({eligible_count} you're fully eligible for)")
            st.markdown("---")
            
            # Show top 3 scholarships
            st.subheader("🏆 Top Recommendations")
            for idx, match in enumerate(result[:3]):
                render_scholarship(match, idx)
            
            # Show more scholarships in expander
            if len(result) > 3:
                with st.expander(f"📋 See {len(result) - 3} More Scholarships"):
                    for idx, match in enumerate(result[3:], start=3):
                        render_scholarship(match, idx)
                        
        else:
            # --- ZERO MATCHES / REJECTION ANALYTICS STATE ---
            st.warning("📋 No scholarships matched your profile perfectly.")
            
            st.markdown("### 🔍 Why didn't I match?")
            st.markdown("Here is a breakdown of why available scholarships didn't fit your profile:")
            
            # Metrics Row
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("CGPA / Grades", f"{stats.get('rejected_cgpa', 0)} Rejects", help="Scholarships requiring higher grades")
            m2.metric("IELTS Score", f"{stats.get('rejected_ielts', 0)} Rejects", help="Scholarships requiring higher English proficiency")
            m3.metric("Country", f"{stats.get('rejected_country', 0)} Rejects", help="Scholarships not in your preferred list")
            m4.metric("Field/Degree", f"{stats.get('rejected_field', 0) + stats.get('rejected_degree', 0)} Rejects", help="Scholarships for other fields/degrees")
            
            st.markdown("---")
            
            # Smart Tips Logic
            st.subheader("💡 Smart Tips to Unlock Opportunities")
            tips_shown = False
            
            unlock_ielts = stats.get('unlock_ielts', 0)
            if unlock_ielts > 0:
                st.info(f"📈 **Impact Opportunity**: Improving your IELTS score (target 6.5 or 7.0) could unlock **{unlock_ielts} additional scholarships** immediately.")
                tips_shown = True
                
            if stats.get('rejected_country', 0) > 0:
                st.info(f"🌍 **Expand Horizons**: You missed out on {stats.get('rejected_country', 0)} scholarships because of country location. Try setting 'Preferred Countries' to **'Any'** to see more options.")
                tips_shown = True
                
            if not tips_shown:
                st.info("🔎 **Broaden Search**: Try checking if your 'Field of Study' name matches common program names (e.g. use 'Computer Science' instead of 'CS').")
                
            # Still show "Partial Matches" if any exist (e.g. not eligible but field matched)
            if len(result) > 0:
                st.markdown("### ⚠️ Partial Matches (Not Eligible)")
                st.markdown("These scholarships matched your degree/field but failed other criteria:")
                for match in result[:3]:
                    render_scholarship(match)
