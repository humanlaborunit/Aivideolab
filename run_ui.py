import gradio as gr
import os

def generate(prompt, script=None, face_image=None):
    # Stub output
    return f"Prompt received: {prompt}\nScript: {script or 'None'}\nFace: {bool(face_image)}"

iface = gr.Interface(
    fn=generate,
    inputs=[
        gr.Textbox(label="Prompt", placeholder="Describe your video..."),
        gr.Textbox(label="Optional Script", placeholder="Type dialog here..."),
        gr.Image(label="Optional Face Image")
    ],
    outputs="text",
    title="Aivideolab NSFW AI Video Generator",
    allow_flagging="never"
)

iface.launch(server_name="0.0.0.0", server_port=7860)

