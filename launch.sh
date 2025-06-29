#!/bin/bash

cd /workspace || cd / || exit

echo "Launching Aivideolab NSFW AI Video Engine..."

# Force expose Gradio UI the way RunPod expects
python3 run_ui.py --host 0.0.0.0 --port 7860 --deepfake --script --voice --nsfw \
  --share 2>&1 | tee /tmp/web.out
