FROM nvidia/cuda:12.2.0-base-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

RUN apt-get update && apt-get install -y \
    git wget curl ffmpeg python3 python3-pip \
    libgl1 libglib2.0-0 libsm6 libxext6 libxrender1 \
    && apt-get clean

COPY requirements.txt .
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

COPY launch.sh ./launch.sh
COPY run_ui.py ./run_ui.py

RUN chmod +x launch.sh
EXPOSE 7860
CMD ["./launch.sh"]
