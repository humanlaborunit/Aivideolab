#!/bin/bash
cd /app || exit
echo "Launching Aivideolab NSFW AI Video Engine..."
python3 run_ui.py --host 0.0.0.0 --port 7860
