#!/bin/bash

echo "=== Starting launch.sh ==="

cd /app || {
    echo "❌ ERROR: /app not found"
    exit 1
}

echo "Installing Python dependencies..."
pip3 install --upgrade pip
pip3 install -r requirements.txt

echo "Starting the NSFW Video App..."
python3 run_ui.py

