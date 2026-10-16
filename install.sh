#!/data/data/com.termux/files/usr/bin/bash

echo "=========================================="
echo "  Setting up Personal AI Agent..."
echo "=========================================="

# টার্মাক্স আপডেট এবং প্রয়োজনীয় টুলস ইনস্টল
pkg update -y
pkg install python git -y

# পাইথন প্যাকেজগুলো pip দিয়ে দ্রুত ইনস্টল করা
pip install --upgrade pip --break-system-packages 2>/dev/null || true
pip install -r requirements.txt --break-system-packages 2>/dev/null || pip install -r requirements.txt

# কারেন্ট ডিরেক্টরি মনে রেখে runai শর্টকাট তৈরি
CURRENT_DIR=$(pwd)

cat << RUNEOF > $PREFIX/bin/runai
#!/data/data/com.termux/files/usr/bin/bash
cd "$CURRENT_DIR"
streamlit run main.py
RUNEOF

chmod +x $PREFIX/bin/runai

echo "=========================================="
echo "  Setup Complete! Enjoy your AI. 🚀"
echo "  Just type: runai"
echo "=========================================="
