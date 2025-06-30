import gradio as gr
import os
import traceback

print("✅ Starting Aivideolab Interface...")

def generate_video(prompt, script=None, face_image=None):
    log = []
    output_path = "/workspace/generated/fake_video.mp4"

    try:
        log.append("📥 Received prompt.")
        if script:
            log.append("✍️ Script received.")
        if face_image is not None:
            log.append("🧑 Face image received and processed.")
        else:
            log.append("⚠️ No face image provided.")

        log.append("🎞️ Simulating video generation...")
        os.makedirs("/workspace/generated", exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(b"FAKE VIDEO CONTENT")

        log.append("✅ Video generation complete.")
        return "\n".join(log), output_path

    except Exception as e:
        log.append("❌ ERROR:")
        log.append(traceback.format_exc())
        return "\n".join(log), None

iface = gr.Interface(
    fn=generate_video,
    inputs=[
        gr.Textbox(label="Prompt"),
        gr.Textbox(label="Optional Script"),
        gr.Image(label="Optional Face Image", type="numpy", optional=True)
    ],
    outputs=[
        gr.Textbox(label="Process Log"),
        gr.File(label="Download Video")
    ],
    title="Aivideolab – NSFW AI Video Generator"
)

iface.launch(server_name="0.0.0.0", server_port=7860)
