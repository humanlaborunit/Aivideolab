FROM nvidia/cuda:11.7.1-cudnn8-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Install base packages
RUN apt-get update && apt-get install -y \
    git ffmpeg libsm6 libxext6 curl wget unzip python3 python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt .
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

# Copy app code
COPY . /app

# Make launch script executable
RUN chmod +x /app/launch.sh

# Expose port for Gradio
EXPOSE 3000

CMD ["/app/launch.sh"]