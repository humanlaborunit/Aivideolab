#!/bin/bash

echo "✅ Starting Aivideolab backend..."

# Clean up old video output (optional)
mkdir -p /workspace/generated
rm -f /workspace/generated/*.mp4

echo "🔁 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🚀 Launching Gradio app on 0.0.0.0:7860"
python3 run_ui.py
