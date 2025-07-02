#!/bin/bash
set -e

echo "[launch.sh] Starting container at $(date)"
echo "[launch.sh] Working directory: $(pwd)"
echo "[launch.sh] Listing files:"
ls -l

# Install all Python dependencies with logging
echo "[launch.sh] Installing Python packages from requirements.txt..."
pip install --no-cache-dir -r requirements.txt | tee install.log

# Print Python version for debugging
echo "[launch.sh] Python version:"
python --version

# Log installed packages
echo "[launch.sh] Checking installed packages..."
pip freeze | tee pip-freeze.log

# Launch the Gradio app (don't pass --port unless your Python file parses it)
echo "[launch.sh] Starting app..."
python run_ui.py | tee gradio-launch.log

echo "[launch.sh] App should now be running."