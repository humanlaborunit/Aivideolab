#!/bin/bash
cd /app || exit

echo "============== STARTING Aivideolab CONTAINER =============="
echo "PWD: $(pwd)"
echo "Contents of /app:"
ls -la /app

echo "==================== RUNNING APP ==========================="
python3 run_ui.py --host 0.0.0.0 --port 7860

