# modules/memory.py
import json
import os

PROFILE_FILE = "user_profile.json"
SESSIONS_FILE = "chat_sessions.json"

def load_user_profile():
    if os.path.exists(PROFILE_FILE):
        try:
            with open(PROFILE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("profile", "No personal profile set yet. Use the settings menu to set up your profile.")
        except Exception:
            return "No profile data found."
    return "No profile data found."

def save_user_profile(profile_text):
    data = {"profile": profile_text}
    try:
        with open(PROFILE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Error saving profile: {e}")
        return False

def load_chat_sessions():
    """
    সারাজীবনের চ্যাট হিস্ট্রি লোড করে।
    """
    if os.path.exists(SESSIONS_FILE):
        try:
            with open(SESSIONS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_chat_sessions(sessions):
    """
    সমস্ত চ্যাট সেশন JSON ফাইলে সেভ করে।
    """
    try:
        with open(SESSIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(sessions, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error saving chat sessions: {e}")

def delete_single_session(session_id):
    """
    একটি নির্দিষ্ট সেশন ডিলিট করে।
    """
    sessions = load_chat_sessions()
    if session_id in sessions:
        del sessions[session_id]
        save_chat_sessions(sessions)
        return sessions
    return sessions
