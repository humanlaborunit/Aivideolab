#!/bin/bash

mkdir -p /app/logs

echo "Launching AI Video App..." | tee /app/logs/launch_log.txt

# Run main app and capture all logs
python3 run_ui.py >> /app/logs/launch_log.txt 2>&1