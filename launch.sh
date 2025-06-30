#!/bin/bash
set -e

echo "🚀 Launching Aivideolab..."

# Optional: update pip and install dependencies again in case of dynamic pods
pip install --upgrade pip
pip install -r requirements.txt

echo "📁 Starting server from run_ui.py..."
python3 /app/run_ui.py
