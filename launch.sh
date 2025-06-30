#!/bin/bash

cd /workspace || cd / || exit

echo "🚀 Launching Aivideolab – NSFW AI Video Engine..."

# Force logs to flush to screen
export PYTHONUNBUFFERED=1

# Explicitly call the main script with forced Gradio HTTP config
python3 run_ui.py --host 0.0.0.0 --port 7860 --nsfw --deepfake --script --voice