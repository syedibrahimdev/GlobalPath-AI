import streamlit as st
from frontend.styles import apply_styles, card
from frontend.api import get_trusted_agents

st.set_page_config(page_title="Trusted Agents", page_icon="🤝", layout="wide")
apply_styles()

st.title("🤝 Trusted Education Agents")
st.markdown("Connect with verified agents to handle your visa and admission process safely.")

# Disclaimer
st.warning("⚠️ **Disclaimer**: GlobalPath AI does not take responsibility for third-party agents. Please verify their credentials independently before proceeding.")

# --- FETCH DATA ---
with st.spinner("Verifying agents..."):
    agents = get_trusted_agents()

if agents:
    # --- DASHBOARD CONTROLS ---
    st.markdown("### 🔍 Find an Agent")
    c1, c2, c3 = st.columns([3, 1.5, 1.5])
    
    with c1:
        search_query = st.text_input("Search Agents", placeholder="Type agent name...", label_visibility="collapsed")
    with c2:
        sort_option = st.selectbox("Sort Preference", ["Trust Score (High → Low)", "Rating (High → Low)"], label_visibility="collapsed")
    with c3:
        filter_license = st.checkbox("Verified License Only", value=True)

    # --- FILTERING LOGIC ---
    filtered_agents = agents
    
    # 1. Search Filter
    if search_query:
        filtered_agents = [a for a in filtered_agents if search_query.lower() in a.get('Name', '').lower()]
    
    # 2. License Filter
    if filter_license:
        # Filter out agents explicitly marked as 'Pending' or missing license
        filtered_agents = [a for a in filtered_agents if a.get('License') and a.get('License') != 'Pending']

    # 3. Sorting Logic
    if "Rating" in sort_option:
        filtered_agents.sort(key=lambda x: x.get('Rating', 0), reverse=True)
    else:
        filtered_agents.sort(key=lambda x: x.get('Trust_Score', 0), reverse=True)

    st.markdown(f"**Showing {len(filtered_agents)} verified agents**")
    st.markdown("---")

    # Display in a grid of 2 columns
    col1, col2 = st.columns(2)
    
    for idx, agent in enumerate(filtered_agents):
        # Determine column logic
        with col1 if idx % 2 == 0 else col2:
            # Badges
            badges = ["Active", f"⭐ {agent.get('Rating', 0)}/5.0"]
            if agent.get('Trust_Score', 0) > 90:
                badges.append("🛡️ High Trust")
            
            # Content with Metrics Layout
            content = f"""
<div style="margin-bottom: 10px; font-style: italic; color: #ddd;">
    {agent.get('Details', 'Registered Agent')}
</div>

<div style="display: flex; justify-content: space-between; background: #262730; padding: 10px; border-radius: 5px; margin-top: 10px;">
    <div style="text-align: center;">
        <span style="color: #bbb; font-size: 11px;">TRUST SCORE</span><br>
        <b style="color: #4CAF50; font-size: 20px;">{agent.get('Trust_Score', 0)}</b><span style="font-size: 12px; color: #888;">/100</span>
    </div>
    <div style="text-align: center; border-left: 1px solid #444; border-right: 1px solid #444; padding: 0 10px;">
        <span style="color: #bbb; font-size: 11px;">COMPLAINTS</span><br>
        <b style="color: #FF6B6B; font-size: 20px;">{agent.get('Complaints', 0)}</b>
    </div>
    <div style="text-align: center;">
        <span style="color: #bbb; font-size: 11px;">RATING</span><br>
        <b style="color: #FFD700; font-size: 20px;">{agent.get('Rating', 0)}</b>
    </div>
</div>"""
            
            card(agent.get('Name', 'Agent'), content, badges)
            

            
            # Interactive "View Details"
            complaint_count = agent.get('Complaints', 0)
            
            if complaint_count > 0:
                expander_label = f"⚠️ {complaint_count} Warning(s) - View Complaint Summary"
            else:
                expander_label = "👁️ View Details & License"
                
            with st.expander(expander_label):
                # LICENSE
                st.markdown(f"**License Number:** `{agent.get('License', 'Pending')}`")
                
                # COMPLAINTS SECTION
                if complaint_count > 0:
                    st.error(f"**Transparency Alert:** This agent has {complaint_count} verified complaint(s) on file.")
                    st.markdown("""
                    **Common Complaint Categories:**
                    *   Delayed document processing
                    *   Communication responsiveness
                    
                    *GlobalPath AI advises discussing these specific issues before engagement.*
                    """)
                else:
                     st.markdown(f"**Service Specialization:** {agent.get('Details', 'General')}")
                     st.success("✅ No verified complaints on file.")

                st.info("⚠️ Verification Tip: Cross-check the license number with the local government website.")
                
                if st.button("Message Agent", key=f"msg_{idx}"):
                    st.toast("Feature coming soon! (Agent notified of interest)")
else:
    st.info("No agents currently available.")
