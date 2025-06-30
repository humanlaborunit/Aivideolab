#!/bin/bash

echo "🚀 Starting AI Video Generator..."

# Optional: Print GPU info
nvidia-smi || echo "⚠️ No NVIDIA GPU detected or nvidia-smi not installed"

# Run the Gradio app on port 3000
python3 /app/run_ui.py --port 3000 --host 0.0.0.0 || {
    echo "❌ Failed to start Gradio app. Check logs above for details."
    exit 1
}