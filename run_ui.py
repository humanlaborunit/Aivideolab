import gradio as gr
import os

# --- Deepfake Mode (from image) ---
def generate_deepfake(face_image, script_text, voice_sample=None):
    # Placeholder function for deepfake logic
    return f"✅ Deepfake video generated with script: {script_text[:30]}..."

# --- Prompt-to-Video Mode ---
def generate_from_prompt(prompt_text):
    # Placeholder for prompt-to-video logic
    return f"✅ Generated video from prompt: {prompt_text[:30]}..."

with gr.Blocks(css=".gradio-container { max-width: 800px !important; }") as app:
    gr.Markdown("## 🎥 Aivideolab NSFW Video Generator")

    with gr.Tab("📸 Deepfake from Image"):
        face = gr.Image(type="filepath", label="Upload Face Image")
        script = gr.Textbox(lines=4, label="Custom Script")
        voice = gr.Audio(source="upload", type="filepath", label="Optional Voice Clone")
        deepfake_btn = gr.Button("Generate Deepfake")
        deepfake_output = gr.Textbox(label="Output")
        deepfake_btn.click(fn=generate_deepfake, inputs=[face, script, voice], outputs=deepfake_output)

    with gr.Tab("✍️ Prompt to Video"):
        prompt_input = gr.Textbox(lines=4, label="Describe the Scene")
        prompt_btn = gr.Button("Generate")
        prompt_output = gr.Textbox(label="Output")
        prompt_btn.click(fn=generate_from_prompt, inputs=prompt_input, outputs=prompt_output)

app.launch(server_name="0.0.0.0", server_port=7860)
