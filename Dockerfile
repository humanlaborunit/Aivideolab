FROM nvidia/cuda:11.7.1-cudnn8-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /workspace

# ------------------------
# Step 1: Basic dependencies (split to avoid failure)
# ------------------------
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg \
        wget \
        unzip && \
    rm -rf /var/lib/apt/lists/*

# ------------------------
# Step 2: System packages
# ------------------------
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git ffmpeg libsm6 libxext6 libgl1 libglib2.0-0 \
        python3 python3-pip libsndfile1 libasound2 && \
    rm -rf /var/lib/apt/lists/*

# ------------------------
# Step 3: Copy everything to working dir
# ------------------------
COPY . .

# ------------------------
# Step 4: Install Python packages
# ------------------------
RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt && \
    pip3 install TTS==0.18.0

# ------------------------
# Step 5: SimSwap model setup
# ------------------------
RUN git clone https://github.com/neuralchen/SimSwap.git SimSwap && \
    mkdir -p SimSwap/checkpoints && \
    curl -L -o SimSwap/checkpoints/arcface_checkpoint.tar \
        https://github.com/neuralchen/SimSwap/releases/download/1.0/arcface_checkpoint.tar && \
    curl -L -o SimSwap/checkpoints/people_model.pth \
        https://github.com/neuralchen/SimSwap/releases/download/1.0/people_model.pth

# ------------------------
# Step 6: Real-ESRGAN setup (binary mirror)
# ------------------------
RUN mkdir -p realesrgan && \
    curl -L -o realesrgan/realesrgan-ncnn-vulkan https://raw.githubusercontent.com/humanlaborunit/video-mirror/main/realesrgan-ncnn-vulkan && \
    chmod +x realesrgan/realesrgan-ncnn-vulkan && \
    curl -L -o realesrgan/realesrgan.param https://raw.githubusercontent.com/humanlaborunit/video-mirror/main/realesrgan.param && \
    curl -L -o realesrgan/realesrgan.bin https://raw.githubusercontent.com/humanlaborunit/video-mirror/main/realesrgan.bin

# ------------------------
# Step 7: RIFE interpolation model
# ------------------------
RUN git clone https://github.com/megvii-research/ECCV2022-RIFE.git rife && \
    curl -L -o rife/RIFE_trained_model_HDv3.pkl https://github.com/megvii-research/ECCV2022-RIFE/releases/download/v1.0/RIFE_trained_model_HDv3.pkl

# ------------------------
# Step 8: Make launch script executable
# ------------------------
RUN chmod +x launch.sh && ls -l launch.sh

# ------------------------
# Step 9: Expose port and launch
# ------------------------
EXPOSE 3000
CMD ["./launch.sh"]
