#!/bin/bash

# Launch script for RunPod container
echo "🌐 Launching Aivideolab..."

# Make sure output folder exists
mkdir -p /workspace/generated

# Run the Gradio app
python3 /workspace/run_ui.py --share --port 7860 --server-name 0.0.0.0