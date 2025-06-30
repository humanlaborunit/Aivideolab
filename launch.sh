#!/bin/bash

echo "🚀 Starting launch script..." | tee /app/startup.log

python3 --version | tee -a /app/startup.log

echo "📁 Checking contents of /app:" | tee -a /app/startup.log
ls -la /app >> /app/startup.log

echo "🎬 Attempting to run run_ui.py..." | tee -a /app/startup.log

python3 /app/run_ui.py --port 3000 --host 0.0.0.0 >> /app/startup.log 2>&1 || {
  echo "❌ Python app failed!" | tee -a /app/startup.log
}

# Stay alive even if the app crashes so we can read logs
while true; do sleep 5; done