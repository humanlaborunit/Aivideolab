FROM nvidia/cuda:12.2.0-base-ubuntu20.04

# --- ENV + system prep ---
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /workspace

# --- System dependencies ---
RUN apt-get update && apt-get install -y \
    git wget curl ffmpeg python3 python3-pip python3-venv \
    libgl1 libglib2.0-0 libsm6 libxext6 libxrender-dev \
    && apt-get clean

# --- Python dependencies ---
COPY requirements.txt .
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

# --- App files ---
COPY launch.sh /workspace/launch.sh
COPY run_ui.py /workspace/run_ui.py

# --- Permissions & startup ---
RUN chmod +x /workspace/launch.sh
EXPOSE 7860
CMD ["/workspace/launch.sh"]
