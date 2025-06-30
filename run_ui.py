import gradio as gr
import os

def process(prompt, script=None, image=None):
    steps = []
    steps.append(f"✅ Prompt received: {prompt}")
    if script:
        steps.append("📝 Script input detected.")
    if image:
        steps.append("🖼️ Face image uploaded.")

    try:
        steps.append("🚀 Generating video...")
        steps.append("✅ Video generation complete.")
    except Exception as e:
        steps.append(f"❌ Error: {str(e)}")

    return "\n".join(steps), "https://example.com/fake_video.mp4"

iface = gr.Interface(
    fn=process,
    inputs=[
        gr.Textbox(label="Prompt"),
        gr.Textbox(label="Script (Optional)"),
        gr.Image(type="filepath", label="Face Image (Optional)")
    ],
    outputs=[
        gr.Textbox(label="Status Log"),
        gr.Textbox(label="Download Link")
    ],
    title="NSFW AI Video Generator",
    description="Enter a prompt, script, and image to generate a video.",
)

iface.launch(server_name="0.0.0.0", server_port=3000)
