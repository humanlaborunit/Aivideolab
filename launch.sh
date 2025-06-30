#!/bin/bash

cd /workspace || cd / || exit

echo "🚀 Launching Aivideolab NSFW AI Video Engine..."
echo "📂 Current files:"
ls -la

echo "🧠 Running interface..."
python3 run_ui.py --host 0.0.0.0 --port 7860 --nsfw --deepfake --script --voice 2>&1 | tee /workspace/logs.txt
