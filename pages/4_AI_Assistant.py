import streamlit as st
from frontend.styles import apply_styles
from frontend.api import send_chat_message

st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="wide")
apply_styles()

st.title("🤖 AI Assistant")
st.markdown("Ask anything about scholarships, visa processes, or interview preparation.")

# --- Sidebar Controls ---
with st.sidebar:
    st.header("Controls")
    if st.button("Clear Chat History", type="primary"):
        st.session_state.messages = []
        st.rerun()

# --- Initialize chat history ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Suggested Prompts (if chat is empty) ---
if not st.session_state.messages:
    st.info("👋 **Welcome! Try asking one of these:**")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Find fully funded scholarships in UK"):
             prompts_to_send = "Find fully funded scholarships in UK"
             # We need to handle this trigger, simplest way is to auto-submit next run or just pre-fill. 
             # Streamlit buttons reload the script, so we can't easily inject into chat_input directly without session state ticks.
             # For MVP, let's just show text suggestions or use a hack if needed, but standard buttons are safer.
             # Actually, better pattern:
             st.session_state.messages.append({"role": "user", "content": prompts_to_send})
             with st.spinner("Thinking..."):
                response = send_chat_message(prompts_to_send)
             st.session_state.messages.append({"role": "assistant", "content": response})
             st.rerun()
             
    with col2:
        if st.button("How do I apply for a Student Visa?"):
             prompts_to_send = "How do I apply for a Student Visa?"
             st.session_state.messages.append({"role": "user", "content": prompts_to_send})
             # We repeat logic here or refactor. Repeating for MVP speed.
             with st.spinner("Thinking..."):
                response = send_chat_message(prompts_to_send)
             st.session_state.messages.append({"role": "assistant", "content": response})
             st.rerun()

# --- Display Chat ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- User Input ---
if prompt := st.chat_input("How can I help you today?"):
    # Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Get and display AI response
    with st.spinner("Thinking..."):
        response = send_chat_message(prompt)
    
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
