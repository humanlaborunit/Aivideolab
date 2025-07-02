#!/bin/bash
set -e

echo "[launch.sh] Starting container at $(date)"
echo "[launch.sh] Working directory: $(pwd)"
echo "[launch.sh] Listing files:"
ls -l

# Force install all dependencies with log
echo "[launch.sh] Installing Python packages from requirements.txt..."
pip install --no-cache-dir -r requirements.txt | tee install.log

# Diagnostic - Check Python version and installed packages
echo "[launch.sh] Python version:"
python --version

echo "[launch.sh] Checking installed packages..."
pip freeze | tee pip-freeze.log

# Start the Gradio app (DO NOT override port or server_name)
echo "[launch.sh] Starting app using Python default settings..."
python run_ui.py | tee gradio-launch.log

echo "[launch.sh] App should now be running."