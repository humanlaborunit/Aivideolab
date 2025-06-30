import gradio as gr
import os
import traceback
import uuid
from PIL import Image
import numpy as np

# Directory to save generated videos
OUTPUT_DIR = "/workspace/generated"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_video(prompt, script=None, face_image=None, voice_audio=None):
    log = []
    output_filename = f"{uuid.uuid4()}.mp4"
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    try:
        log.append("📥 Step 1: Received input.")
        log.append(f"Prompt: {prompt}")

        if script:
            log.append("✍️ Step 2: Custom script received.")
        else:
            log.append("✍️ Step 2: No custom script provided, will autogenerate.")

        if face_image is not None:
            log.append("🧑 Step 3: Face image uploaded and validated.")
            assert isinstance(face_image, np.ndarray)
        else:
            log.append("⚠️ Step 3: No face image provided.")

        if voice_audio is not None:
            log.append("🎤 Step 4: Voice audio uploaded.")
        else:
            log.append("⚠️ Step 4: No voice audio provided.")

        # Simulate generation process (to be replaced with real model calls)
        log.append("🎞️ Step 5: Starting video generation simulation...")
        with open(output_path, "wb") as f:
            f.write(b"FAKE_VIDEO_CONTENT")
        log.append("✅ Step 6: Video successfully generated and saved.")

        return "\n".join(log), output_path

    except Exception as e:
        log.append("❌ ERROR during generation:")
        log.append(str(e))
        log.append(traceback.format_exc())
        return "\n".join(log), None

iface = gr.Interface(
    fn=generate_video,
    inputs=[
        gr.Textbox(label="Prompt (Required)"),
        gr.Textbox(label="Optional Script"),
        gr.Image(label="Optional Face Image", type="numpy", optional=True),
        gr.Audio(label="Optional Voice Audio", type="filepath", optional=True)
    ],
    outputs=[
        gr.Textbox(label="Process Log"),
        gr.File(label="Download Generated Video")
    ],
    title="Aivideolab – NSFW AI Video Generator",
    description="Upload a prompt, script, face image, or voice to generate a deepfake-style video. NSFW always enabled. Status logged clearly at each step."
)

iface.launch(server_name="0.0.0.0", server_port=7860)
