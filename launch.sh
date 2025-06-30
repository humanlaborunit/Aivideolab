#!/bin/bash

echo "🚀 Starting Aivideolab container..."

# Show environment info
echo "🔍 Python version:"
python3 --version
echo "📦 Installed packages:"
pip3 list

# Launch Gradio app
echo "🌐 Launching app on port 7860..."
python3 run_ui.py --port 7860 --host 0.0.0.0
