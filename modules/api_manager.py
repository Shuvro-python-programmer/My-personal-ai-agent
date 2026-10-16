# modules/api_manager.py
import requests
from bs4 import BeautifulSoup
from config import OPENROUTER_API_KEY, GROQ_API_KEY
from modules.memory import load_user_profile

def should_search(prompt: str) -> bool:
    prompt_lower = prompt.lower().strip()
    skip_keywords = [
        "hi", "hello", "hey", "assalamualikum", "salam", "kemon aso", "kemon achen",
        "apni ki", "tomar nam", "apnar nam", "who are you", "what are you doing",
        "আপনি কে", "আপনার নাম", "কে আপনি", "হাই", "হ্যালো", "কেমন আছেন", "কি করছেন",
        "memory on", "memory off"
    ]
    if len(prompt_lower.split()) <= 3 and any(k in prompt_lower for k in skip_keywords):
        return False
    return True

def web_search(query: str) -> str:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        }
        url = f"https://html.duckduckgo.com/html/?q={query}"
        response = requests.get(url, headers=headers, timeout=10)

        soup = BeautifulSoup(response.text, 'html.parser')
        snippets = soup.find_all('a', class_='result__snippet')
        if not snippets:
            snippets = soup.find_all('div', class_='result__snippet')

        if not snippets:
            return f"No search results found for '{query}'."

        results_list = []
        for snip in snippets[:4]:
            text = snip.text.strip()
            if text and text not in results_list:
                results_list.append(text)

        return "\n".join(results_list) if results_list else "No direct snippet found."
    except Exception as e:
        return f"Search Error: {str(e)}"

def generate_ai_response(prompt, chat_history=None, session_summary=""):
    if chat_history is None:
        chat_history = []

    search_context = ""
    needs_search = should_search(prompt)
    
    if needs_search:
        print(f"Searching internet for: '{prompt}'...")
        search_context = web_search(prompt)

    # ইউজারের নিজস্ব পার্সোনাল প্রোফাইল ডাইনামিক্যালি লোড হবে
    current_user_profile = load_user_profile()

    system_prompt = f"""You are an advanced, helpful personal AI assistant. Current year is 2026.

USER'S PERSONAL PROFILE (Learned from user input):
{current_user_profile}

Previous Conversation Summary:
{session_summary if session_summary else "No prior summary yet."}

Real-time Web Search Results:
{search_context if needs_search else "No search performed."}

Instructions:
1. Act as a dedicated personal assistant to the user based on their profile.
2. Maintain continuity with ongoing chat history.
3. Keep the tone natural, polite, helpful, and direct.
"""

    messages = [{"role": "system", "content": system_prompt}]
    
    for msg in chat_history[-10:]:
        if "role" in msg and "content" in msg:
            messages.append({"role": msg["role"], "content": msg["content"]})
            
    messages.append({"role": "user", "content": prompt})

    # 1. Try OpenRouter First
    if OPENROUTER_API_KEY and OPENROUTER_API_KEY != "YOUR_OPENROUTER_API_KEY":
        try:
            url = "https://openrouter.ai/api/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "deepseek/deepseek-chat",
                "messages": messages
            }

            response = requests.post(url, headers=headers, json=payload, timeout=20)
            if response.status_code == 200:
                res_data = response.json()
                answer = res_data["choices"][0]["message"]["content"]
                return answer, "OpenRouter (Personal AI)"
            else:
                print(f"[Debug] OpenRouter Error: {response.text}")
        except Exception as e:
            print(f"[Debug] OpenRouter Exception: {e}")

    # 2. Fallback to Groq
    if GROQ_API_KEY and GROQ_API_KEY != "YOUR_GROQ_API_KEY":
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "openai/gpt-oss-120b",
                "messages": messages
            }

            response = requests.post(url, headers=headers, json=payload, timeout=20)
            if response.status_code == 200:
                res_data = response.json()
                answer = res_data["choices"][0]["message"]["content"]
                return answer, "Groq AI (Fallback)"
            else:
                print(f"[Debug] Groq Error: {response.text}")
        except Exception as e:
            print(f"[Debug] Groq Exception: {e}")

    return "দুঃখিত, কোনো এপিআই থেকে রেসপন্স পাওয়া যায়নি।", "Error"
