import gradio as gr
import os
import uuid
import traceback

OUTPUT_DIR = "/workspace/generated"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_video(prompt, script=None, face_image=None, voice_audio=None):
    log = []
    log.append("📥 Prompt received.")
    session_id = str(uuid.uuid4())[:8]
    video_path = os.path.join(OUTPUT_DIR, f"{session_id}_output.mp4")

    try:
        if script:
            log.append("✍️ Custom script provided.")
        else:
            log.append("🗣️ No custom script. Using auto-generated.")

        if face_image is not None:
            log.append("🧑 Face image uploaded. Deepfake mode ON.")
            # TODO: Insert face-swapping logic here
        else:
            log.append("🧑 No face image provided. Using default model.")

        if voice_audio is not None:
            log.append("🔊 Voice audio uploaded. Cloning voice.")
            # TODO: Insert voice cloning logic here
        else:
            log.append("🔊 No voice provided. Using default voice.")

        # Simulate video generation
        log.append("🎞️ Generating video (placeholder in current build)...")
        with open(video_path, "wb") as f:
            f.write(b"FAKE VIDEO CONTENT")

        log.append("✅ Generation complete.")
        return "\n".join(log), video_path

    except Exception as e:
        log.append("❌ ERROR:")
        log.append(traceback.format_exc())
        return "\n".join(log), None


with gr.Blocks(title="Aivideolab – NSFW AI Video Generator") as demo:
    gr.Markdown("## 🧪 Aivideolab – AI Video Generator (NSFW Capable)")
    prompt = gr.Textbox(label="Prompt", placeholder="Enter your video prompt here")
    script = gr.Textbox(label="Optional Script", placeholder="Type a custom script...")
    face_image = gr.Image(label="Optional Face Image", type="numpy", optional=True)
    voice_audio = gr.Audio(label="Optional Voice Audio", type="filepath", optional=True)

    with gr.Row():
        submit_btn = gr.Button("Generate")
        clear_btn = gr.Button("Clear")

    log_output = gr.Textbox(label="Process Log")
    video_output = gr.File(label="Download Generated Video")

    submit_btn.click(
        generate_video,
        inputs=[prompt, script, face_image, voice_audio],
        outputs=[log_output, video_output],
    )

    clear_btn.click(
        lambda: ("", None),
        outputs=[log_output, video_output]
    )

demo.launch(server_name="0.0.0.0", server_port=7860)
