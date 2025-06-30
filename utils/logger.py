import time

LOG_FILE = "log.txt"

def log_step(message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {message}\n"

    # Print to terminal (if available)
    print(entry.strip())

    # Save to log file
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(entry)
    except Exception as e:
        print(f"Error writing log: {e}")