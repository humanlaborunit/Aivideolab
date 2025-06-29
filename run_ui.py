import gradio as gr
import os
import traceback

def generate_video(prompt, script=None, face_image=None):
    log = []
    output_path = "/workspace/generated/fake_video.mp4"

    log.append("✅ UI function started.")

    try:
        log.append(f"📥 Prompt received: {prompt}")
        log.append(f"🧾 Script: {script or 'None'}")
        log.append(f"🖼️ Face image: {'Yes' if face_image is not None else 'No'}")

        os.makedirs("/workspace/generated", exist_ok=True)
        log.append("📂 Output directory ensured.")

        with open(output_path, "wb") as f:
            f.write(b"FAKE VIDEO CONTENT")
        log.append(f"✅ Dummy video created at: {output_path}")

        return "\n".join(log), output_path

    except Exception as e:
        log.append("❌ ERROR ENCOUNTERED:")
        log.append(traceback.format_exc())
        return "\n".join(log), None


def startup_confirmation():
    return "✅ Startup check successful. UI is running."


# 🧠 Interfaces
main_ui = gr.Interface(
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
)

startup_ui = gr.Interface(
    fn=startup_confirmation,
    inputs=[],
    outputs=gr.Textbox(label="Startup Status")
)

# 🗂️ Combined view with tabs
app = gr.TabbedInterface(
    [main_ui, startup_ui],
    tab_names=["Generate", "Startup Check"]
)

app.launch(server_name="0.0.0.0", server_port=7860)

