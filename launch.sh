#!/bin/bash
set -e

echo "🔧 Updating pip and installing requirements..."
pip install --upgrade pip
pip install -r /app/requirements.txt

echo "🚀 Launching Aivideolab UI..."
python3 /app/run_ui.py --port 7860 --host 0.0.0.0
