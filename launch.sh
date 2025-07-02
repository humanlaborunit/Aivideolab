#!/bin/bash
set -e

echo "[launch.sh] Starting container at $(date)"
echo "[launch.sh] Working directory: $(pwd)"
ls -l

echo "[launch.sh] Installing Python packages from requirements.txt..."
pip install --no-cache-dir -r requirements.txt | tee install.log

echo "[launch.sh] Python version:"
python3 --version
pip freeze | tee pip-freeze.log

echo "[launch.sh] Starting app..."
python3 run_ui.py | tee gradio-launch.log

echo "[launch.sh] App should now be running."