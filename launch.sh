#!/bin/bash

echo "🚀 Launch script initiated."

# Log Python version and path for diagnostics
echo "🐍 Python version:"
python3 --version
echo "📍 Python path:"
which python3

# Log contents of /app (for debugging missing files)
echo "📁 Listing /app directory contents:"
ls -al /app

# Start the UI backend
echo "🎬 Starting Aivideolab app..."
python3 /app/run_ui.py

# If it crashes, keep the container alive to show logs
EXIT_CODE=$?
echo "❌ Application exited with code $EXIT_CODE"
tail -f /dev/null
