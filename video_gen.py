import os
import uuid
import subprocess
from moviepy.editor import VideoFileClip, AudioFileClip
from pathlib import Path

# Directory setup
Path("outputs").mkdir(exist_ok=True)
Path("temp").mkdir(exist_ok=True)

def generate_t2v_video(prompt):
    out_path = f"temp/{uuid.uuid4()}.mp4"
    try:
        # Using ModelScope text-to-video pretrained model
        subprocess.run([
            "python3", "-m", "modelscope.tools.cli", "infer",
            "--model_id=damo/text-to-video-synthesis",
            f"--text={prompt}",
            f"--output={out_path}"
        ], check=True)
        return out_path
    except Exception as e:
        raise RuntimeError(f"T2V generation failed: {e}")

def combine_audio(video_path, audio_path):
    output_path = f"outputs/final_{uuid.uuid4()}.mp4"
    try:
        video_clip = VideoFileClip(video_path)
        audio_clip = AudioFileClip(audio_path).set_duration(video_clip.duration)
        final = video_clip.set_audio(audio_clip)
        final.write_videofile(output_path, codec="libx264", audio_codec="aac")
        return output_path
    except Exception as e:
        raise RuntimeError(f"Audio-video sync failed: {e}")

def generate_full_video(prompt, voice_path):
    video_path = generate_t2v_video(prompt)
    final_video_path = combine_audio(video_path, voice_path)
    return final_video_path