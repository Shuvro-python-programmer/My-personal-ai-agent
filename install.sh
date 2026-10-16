#!/data/data/com.termux/files/usr/bin/bash
echo "Setting up Personal AI Agent..."
pkg update -y && pkg install python git -y
pip install --upgrade pip
pip install -r requirements.txt

cat << 'RUNEOF' > start_agent.sh
#!/data/data/com.termux/files/usr/bin/bash
cd $(dirname "$0")
python -m streamlit run main.py &
sleep 3
termux-open-url http://localhost:8501
RUNEOF

chmod +x start_agent.sh
mkdir -p $PREFIX/bin
ln -sf $(pwd)/start_agent.sh $PREFIX/bin/runai
echo "Setup Complete! Just type: runai"
