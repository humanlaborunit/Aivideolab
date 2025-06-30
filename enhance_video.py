import os
import uuid
import subprocess
from pathlib import Path

Path("enhanced_videos").mkdir(exist_ok=True)

def enhance_video(input_video_path):
    try:
        # Intermediate upscale
        upscaled_path = f"enhanced_videos/upscaled_{uuid.uuid4()}.mp4"
        subprocess.run([
            "realesrgan-ncnn-vulkan",
            "-i", input_video_path,
            "-o", upscaled_path,
            "-n", "realesrgan-x4plus",
            "-s", "4"
        ], check=True)

        # Optional: Smooth with RIFE
        smoothed_path = f"enhanced_videos/smoothed_{uuid.uuid4()}.mp4"
        subprocess.run([
            "python3", "rife/infer.py",
            "--input", upscaled_path,
            "--output", smoothed_path,
            "--scale", "2"
        ], check=True)

        return smoothed_path
    except Exception as e:
        raise RuntimeError(f"Video enhancement failed: {e}")