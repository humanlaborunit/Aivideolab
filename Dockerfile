# Base image with Python
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

# Make launch script executable
RUN chmod +x /app/launch.sh

# Expose Gradio default port
EXPOSE 7860

# Start the container using launch.sh
CMD ["/app/launch.sh"]
