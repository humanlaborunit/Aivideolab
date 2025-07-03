#!/bin/bash
set -e

echo "[launch.sh] Starting container at $(date)"
echo "[launch.sh] Working directory: $(pwd)"
echo "[launch.sh] Listing files:"
ls -l

echo "[launch.sh] Installing Python packages from requirements.txt..."
pip install --no-cache-dir -r requirements.txt | tee install.log

echo "[launch.sh] Python version:"
python --version

echo "[launch.sh] Checking installed packages..."
pip freeze | tee pip-freeze.log

echo "[launch.sh] Starting Gradio app on 0.0.0.0:3000..."
python3 run_ui.py | tee gradio-launch.log

echo "[launch.sh] App should now be running."