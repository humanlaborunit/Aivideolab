FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    GRADIO_SERVER_NAME=0.0.0.0 \
    GRADIO_SERVER_PORT=7860

# Create working directory
WORKDIR /app

# Install OS-level dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    curl \
    libgl1 \
    libglib2.0-0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy full app code into container
COPY . /app

# Expose port for Gradio
EXPOSE 7860

# Launch script on container start
CMD ["/app/launch.sh"]
