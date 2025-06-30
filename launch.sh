#!/bin/bash

echo "🚀 Launch script starting..." | tee /app/startup.log

# Print environment info
echo "🖥️ Host: $(hostname)" | tee -a /app/startup.log
echo "📁 CWD: $(pwd)" | tee -a /app/startup.log
echo "📦 Files in /app:" | ls -la /app | tee -a /app/startup.log

# Confirm Python is working
python3 --version | tee -a /app/startup.log

# Run the Gradio app
echo "🎬 Starting Gradio UI on port 3000..." | tee -a /app/startup.log
python3 /app/run_ui.py --port 3000 --host 0.0.0.0 >> /app/startup.log 2>&1 || {
    echo "❌ Failed to start app. Check /app/startup.log for error output." | tee -a /app/startup.log
    exit 1
}