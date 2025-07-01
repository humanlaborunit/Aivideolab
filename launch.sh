#!/bin/bash

mkdir -p /app/logs

echo "✅ HTTP Fallback launched at $(date)" > /app/logs/fallback_http.txt

# Start basic HTTP server to keep container and port alive
python3 /app/fallback_http_server.py