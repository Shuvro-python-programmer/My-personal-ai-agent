# 🤖 Personal AI Agent

An advanced, lightweight personal AI assistant built for Termux and Python environments, featuring multi-model support (OpenRouter & Groq), real-time web search capabilities, dynamic personal profile memory ("Tell About You"), and lifetime chat session management.

---

## ✨ Features

- **Lifetime Chat History:** Your conversations are permanently saved and never auto-deleted. Manage or delete individual or all chat sessions easily.
- **Dynamic Personal Profile:** Customize your profile ("Tell About You") so the AI always remembers who you are, your preferences, and your work.
- **Multi-API Fallback:** Automatically switches between OpenRouter and Groq to ensure uninterrupted responses.
- **Real-time Web Search:** Automatically fetches live web snippets when needed using DuckDuckGo.
- **One-Command Setup:** Automated installer designed specifically for Termux users.

---
*First you need minimum 1 API key , collect API key free from openrouter & groq . then paste API keys on config.py file*

## 🚀 One-Click Installation for Termux

Open your Termux app and run **just this single command**. It will automatically update packages, install Python & Git, clone the project, install all requirements, and set up the `runai` shortcut:
pkg update -y && pkg install python git -y && git clone [https://github.com/Shuvro-python-programmer/Personal-AI-.git](https://github.com/Shuvro-python-programmer/Personal-AI-.git) && cd Personal-AI- && bash install.sh

💡 How to Use
 * After installation, open Termux and simply type:
   runai

 * The local server will start, and it will automatically open the app in your browser at http://localhost:8501.
 * Go to the sidebar settings (Tell About You) to set up your profile and configure your API keys in config.py.
🛠️ Configuration (config.py)
if you have your own API key paste hero if not no problem 
Open config.py and add your API keys:
OPENROUTER_API_KEY = "your_openrouter_api_key_here"
GROQ_API_KEY = "your_groq_api_key_here"


