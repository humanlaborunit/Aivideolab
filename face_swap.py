import os
import uuid
import subprocess
from pathlib import Path

Path("swapped_videos").mkdir(exist_ok=True)

def run_face_swap(video_path, face_image_path):
    try:
        output_path = f"swapped_videos/swapped_{uuid.uuid4()}.mp4"

        # Assumes SimSwap CLI installed and configured inside container
        command = [
            "python3", "inference_simSwap.py",
            "--target_video", video_path,
            "--source_image", face_image_path,
            "--output_path", output_path
        ]

        subprocess.run(command, check=True)
        return output_path
    except Exception as e:
        raise RuntimeError(f"Face swap failed: {e}")