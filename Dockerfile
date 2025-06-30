FROM nvidia/cuda:11.7.1-cudnn8-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# ------------------------
# Install system packages
# ------------------------
RUN apt-get update && apt-get install -y \
    git ffmpeg libsm6 libxext6 libgl1 libglib2.0-0 \
    curl wget unzip python3 python3-pip \
    libsndfile1 libasound2 libavcodec-dev libavformat-dev libavdevice-dev \
    && rm -rf /var/lib/apt/lists/*

# ------------------------
# Copy requirements and install Python packages
# ------------------------
COPY requirements.txt .
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt && pip3 install TTS==0.18.0

# ------------------------
# Clone SimSwap (Face Swap - CLI callable)
# ------------------------
RUN git clone https://github.com/neuralchen/SimSwap.git /app/SimSwap && \
    mkdir -p /app/SimSwap/checkpoints && \
    curl -L -o /app/SimSwap/checkpoints/arcface_checkpoint.tar \
        https://github.com/neuralchen/SimSwap/releases/download/1.0/arcface_checkpoint.tar && \
    curl -L -o /app/SimSwap/checkpoints/people_model.pth \
        https://github.com/neuralchen/SimSwap/releases/download/1.0/people_model.pth

# ------------------------
# Download ESRGAN binary from reliable mirror
RUN mkdir -p /app/realesrgan && \
    curl -L -o /app/realesrgan/realesrgan-ncnn-vulkan https://raw.githubusercontent.com/humanlaborunit/video-mirror/main/realesrgan-ncnn-vulkan && \
    chmod +x /app/realesrgan/realesrgan-ncnn-vulkan && \
    curl -L -o /app/realesrgan/realesrgan.param https://raw.githubusercontent.com/humanlaborunit/video-mirror/main/realesrgan.param && \
    curl -L -o /app/realesrgan/realesrgan.bin https://raw.githubusercontent.com/humanlaborunit/video-mirror/main/realesrgan.bin

# ------------------------
# Clone RIFE for frame interpolation
# ------------------------
RUN git clone https://github.com/megvii-research/ECCV2022-RIFE.git /app/rife && \
    cd /app/rife && \
    curl -L -o RIFE_trained_model_HDv3.pkl https://github.com/megvii-research/ECCV2022-RIFE/releases/download/v1.0/RIFE_trained_model_HDv3.pkl

# ------------------------
# Copy your application files
# ------------------------
COPY . /app

# ------------------------
# Make launch script executable
# ------------------------
RUN chmod +x /app/launch.sh

# ------------------------
# Expose Gradio port
# ------------------------
EXPOSE 3000

# ------------------------
# Launch the app
# ------------------------
CMD ["/app/launch.sh"]