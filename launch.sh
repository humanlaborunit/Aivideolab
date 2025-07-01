#!/bin/bash

mkdir -p /app/logs

LOGFILE="/app/logs/startup_$(date +%Y%m%d_%H%M%S).log"

echo "⏳ Launching AI Video App..." > "$LOGFILE"
date >> "$LOGFILE"

# Attempt to run full app
python3 run_ui.py >> "$LOGFILE" 2>&1 || {
    echo "❌ Main app failed. Launching fallback server." >> "$LOGFILE"
    python3 fallback_http_server.py >> "$LOGFILE" 2>&1
}

# Keep container alive
echo "🛑 App exited or failed at $(date)" >> "$LOGFILE"
sleep infinity