#!/bin/bash

cd /workspace || cd / || exit

echo "Launching Aivideolab NSFW AI Video Engine..."

# Launch the full pipeline: prompt-to-video, face input, voice + script
python3 run_ui.py --host 0.0.0.0 --port 7860 --nsfw --deepfake --script --voice
