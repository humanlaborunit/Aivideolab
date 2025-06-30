#!/bin/bash

echo "🚀 Starting launch script..." | tee /app/startup.log

# Print environment info
echo "🧠 Host: $(hostname)" | tee -a /app/startup.log
echo "📦 Current dir: $(pwd)" | tee -a /app/startup.log
echo "📁 Files in /app:" | ls -la /app | tee -a /app/startup.log

# Confirm Python
python3 --version | tee -a /app/startup.log

# Launch the Gradio app and write all logs
echo "🎬 Launching Gradio app..." | tee -a /app/startup.log
python3 /app/run_ui.py --port 3000 --host 0.0.0.0 >> /app/startup.log 2>&1 || {
  echo "❌ App crashed. Check /app/startup.log" | tee -a /app/startup.log
  exit 1
}