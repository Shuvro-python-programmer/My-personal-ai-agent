# main.py
import streamlit as st
import time
from modules.api_manager import generate_ai_response
from modules.memory import (
    load_chat_sessions, 
    save_chat_sessions, 
    load_user_profile, 
    save_user_profile,
    delete_single_session
)

st.set_page_config(page_title="Personal AI Agent", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stTextInput textarea { color: #ffffff; }
    .api-badge { font-size: 11px; color: #888888; background-color: #1e2530; padding: 2px 6px; border-radius: 4px; display: inline-block; margin-top: 4px; }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 Personal AI Agent")

# Sidebar UI
st.sidebar.title("💬 Chat Sessions")

if st.sidebar.button("➕ New Chat", use_container_width=True):
    new_id = f"Chat {int(time.time())}"
    if "sessions" not in st.session_state:
        st.session_state.sessions = load_chat_sessions()
    st.session_state.sessions[new_id] = {"summary": "", "messages": []}
    st.session_state.current_session = new_id
    save_chat_sessions(st.session_state.sessions)
    st.rerun()

st.sidebar.markdown("---")

# Settings: Tell About You
with st.sidebar.expander("⚙️ Tell About You (Settings)"):
    current_profile_val = load_user_profile()
    user_input_profile = st.text_area("আপনার সম্পর্কে (নাম, পেশা, পছন্দ ইত্যাদি) এখানে লিখুন:", value=current_profile_val if current_profile_val != "No profile data found." else "")
    if st.button("Save Profile", use_container_width=True):
        if save_user_profile(user_input_profile):
            st.success("প্রোফাইল সফলভাবে সেভ হয়েছে!")
            time.sleep(1)
            st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("🗂️ All Chat History")

# Load sessions
if "sessions" not in st.session_state:
    st.session_state.sessions = load_chat_sessions()

if not st.session_state.sessions:
    unique_id = f"Chat {int(time.time())}"
    st.session_state.sessions = {unique_id: {"summary": "", "messages": []}}
    st.session_state.current_session = unique_id
    save_chat_sessions(st.session_state.sessions)

if "current_session" not in st.session_state or st.session_state.current_session not in st.session_state.sessions:
    st.session_state.current_session = list(st.session_state.sessions.keys())[-1]

session_keys = list(st.session_state.sessions.keys())

# প্রতিটি সেশনের জন্য লিস্ট এবং আলাদা ডিলিট বাটন
for s_name in reversed(session_keys):
    display_name = s_name if not s_name.startswith("Chat ") else "New Conversation"
    if len(display_name) > 20:
        display_name = display_name[:20] + "..."

    col1, col2 = st.sidebar.columns([4, 1])
    
    with col1:
        # চ্যাট সিলেক্ট বাটন
        if st.button(display_name, use_container_width=True, key=f"sess_{s_name}"):
            st.session_state.current_session = s_name
            st.rerun()
            
    with col2:
        # প্রতিটি চ্যাটের জন্য আলাদা ডিলিট বাটন
        if st.button("🗑️", key=f"del_{s_name}"):
            updated_sessions = delete_single_session(s_name)
            st.session_state.sessions = updated_sessions
            if st.session_state.current_session == s_name:
                if updated_sessions:
                    st.session_state.current_session = list(updated_sessions.keys())[-1]
                else:
                    fresh_id = f"Chat {int(time.time())}"
                    st.session_state.sessions = {fresh_id: {"summary": "", "messages": []}}
                    st.session_state.current_session = fresh_id
                    save_chat_sessions(st.session_state.sessions)
            st.rerun()

st.sidebar.markdown("---")

# একসাথে সব হিস্ট্রি ডিলিট বাটন
if st.sidebar.button("🗑️ Clear All History", use_container_width=True):
    fresh_id = f"Chat {int(time.time())}"
    st.session_state.sessions = {fresh_id: {"summary": "", "messages": []}}
    st.session_state.current_session = fresh_id
    save_chat_sessions(st.session_state.sessions)
    st.rerun()

# বর্তমান সেশনের ডেটা
current_session_data = st.session_state.sessions[st.session_state.current_session]
current_messages = current_session_data.get("messages", [])
current_summary = current_session_data.get("summary", "")

# মেসেজ রেন্ডার করা
for message in current_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and "api_source" in message:
            st.markdown(f'<span class="api-badge">⚡ Powered by: {message["api_source"]}</span>', unsafe_allow_html=True)

# ইউজার ইনপুট হ্যান্ডলার
if prompt := st.chat_input("আপনার মেসেজ এখানে লিখুন..."):
    if len(current_messages) == 0:
        new_title = prompt[:30] + "..." if len(prompt) > 30 else prompt
        st.session_state.sessions[new_title] = st.session_state.sessions.pop(st.session_state.current_session)
        st.session_state.current_session = new_title
        current_session_data = st.session_state.sessions[st.session_state.current_session]
        current_messages = current_session_data.get("messages", [])

    user_msg = {"role": "user", "content": prompt}
    current_messages.append(user_msg)

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("চিন্তা করছে..."):
            reply, active_model = generate_ai_response(prompt, current_messages, current_summary)
            st.markdown(reply)
            st.markdown(f'<span class="api-badge">⚡ Powered by: {active_model}</span>', unsafe_allow_html=True)

            assistant_msg = {
                "role": "assistant",
                "content": reply,
                "api_source": active_model
            }
            current_messages.append(assistant_msg)

    st.session_state.sessions[st.session_state.current_session]["messages"] = current_messages
    save_chat_sessions(st.session_state.sessions)
