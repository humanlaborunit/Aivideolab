import os
import uuid
import tempfile
import traceback
import subprocess
from datetime import datetime

import gradio as gr

LOG_FILE = "generation_log.txt"
os.makedirs("outputs", exist_ok=True)

def log_event(message):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    full_message = f"{timestamp} {message}\n"
    with open(LOG_FILE, "a") as f:
        f.write(full_message)
    return full_message

def generate_video(prompt, face_image=None, voice_audio=None, script_text=None):
    session_id = str(uuid.uuid4())[:8]
    output_path = f"outputs/video_{session_id}.mp4"
    status = ""

    try:
        status += log_event("📌 Starting generation pipeline...")

        # Save uploaded image (if any)
        face_path = None
        if face_image is not None:
            face_path = f"/tmp/face_{session_id}.png"
            face_image.save(face_path)
            status += log_event("🖼️ Face image uploaded.")

        # Save uploaded audio (if any)
        voice_path = None
        if voice_audio is not None:
            voice_path = f"/tmp/audio_{session_id}.wav"
            with open(voice_path, "wb") as f:
                f.write(voice_audio.read())
            status += log_event("🎤 Voice audio uploaded.")

        # Save script (if any)
        script_path = None
        if script_text:
            script_path = f"/tmp/script_{session_id}.txt"
            with open(script_path, "w") as f:
                f.write(script_text)
            status += log_event("📜 Script input saved.")

        # Build generation command
        command = ["python3", "core/generate.py", "--prompt", prompt, "--output", output_path]

        if face_path:
            command += ["--face", face_path]
        if voice_path:
            command += ["--voice", voice_path]
        if script_path:
            command += ["--script", script_path]

        status += log_event("⚙️ Running generation command...")
        subprocess.run(command, check=True)

        status += log_event(f"✅ Video generated at {output_path}")
        return output_path, status

    except subprocess.CalledProcessError as e:
        error_msg = log_event(f"❌ Generation failed: {str(e)}")
        return None, status + error_msg

    except Exception as e:
        error_msg = log_event(f"❌ Unexpected error: {traceback.format_exc()}")
        return None, status + error_msg

### Gradio UI

with gr.Blocks() as demo:
    gr.Markdown("# 🔥 Aivideolab — AI Video Generator (NSFW-enabled)")
    prompt = gr.Textbox(label="🎯 Prompt", placeholder="Enter your prompt here...")
    face = gr.Image(type="pil", label="🖼️ Upload Face (optional)")
    voice = gr.Audio(type="binary", label="🎤 Upload Voice Audio (optional)")
    script = gr.Textbox(lines=5, label="📜 Custom Script (optional)", placeholder="Optional: script for syncing")

    generate_btn = gr.Button("🚀 Generate Video")

    video_output = gr.Video(label="📽️ Generated Video Output")
    log_output = gr.Textbox(lines=20, label="📝 Generation Logs")

    def wrapper(prompt, face, voice, script):
        return generate_video(prompt, face, voice, script)

    generate_btn.click(fn=wrapper, inputs=[prompt, face, voice, script], outputs=[video_output, log_output])

demo.launch(server_name="0.0.0.0", server_port=7860)