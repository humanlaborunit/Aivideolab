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
# Download Real-ESRGAN binary (for enhancement)
# ------------------------
RUN pip3 install gdown && \
    gdown https://drive.google.com/uc?id=1vPghGnVaTX-iY5N_8MdXQ70I9ib7KU84 -O /app/realesrgan.zip && \
    unzip /app/realesrgan.zip -d /app/realesrgan && \
    chmod +x /app/realesrgan/realesrgan-ncnn-vulkan

# ------------------------
# Clone RIFE for frame interpolation
# ------------------------
RUN git clone https://github.com/megvii-research/ECCV2022-RIFE.git /app/rife && \
    cd /app/rife && \
    wget https://github.com/megvii-research/ECCV2022-RIFE/releases/download/v1.0/RIFE_trained_model_HDv3.pkl

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