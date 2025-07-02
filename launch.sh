#!/bin/bash

echo "🔁 Launch script starting..."

# Ensure Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found! Exiting."
    exit 1
fi

# Activate virtual environment if one exists
if [ -d ".venv" ]; then
    echo "📦 Activating virtual environment..."
    source .venv/bin/activate
fi

# Check for log directory
mkdir -p /app/logs

# Run the Gradio UI and log everything
echo "🚀 Launching Gradio UI at http://0.0.0.0:3000..." | tee /app/logs/boot.log

python3 /app/run_ui.py >> /app/logs/boot.log 2>&1 || {
    echo "❌ Gradio UI crashed. Dumping traceback..." | tee -a /app/logs/boot.log
    echo "----------------------------------------" >> /app/logs/boot.log
    python3 -c 'import traceback; traceback.print_exc()' >> /app/logs/boot.log 2>&1
    echo "❌ Fatal crash logged to /app/logs/boot.log"
}

# Keep container alive if Gradio fails
while true; do
    sleep 30
done