import gradio as gr
import os
import traceback
from modules.video_gen import generate_video_from_prompt
from modules.deepfake import generate_deepfake_video
from modules.voice_clone import clone_voice
from modules.logger import log_message

RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)

def handle_prompt_to_video(prompt, script_text):
    try:
        log_message("Prompt received", prompt)
        video_path = generate_video_from_prompt(prompt, script_text)
        log_message("Video generated at", video_path)
        return video_path, "Video created successfully!"
    except Exception as e:
        error = traceback.format_exc()
        log_message("ERROR", error)
        return None, f"Failed: {e}"

def handle_deepfake(face_image, script_text):
    try:
        log_message("Deepfake requested", face_image.name)
        video_path = generate_deepfake_video(face_image, script_text)
        log_message("Deepfake complete", video_path)
        return video_path, "Deepfake video created."
    except Exception as e:
        error = traceback.format_exc()
        log_message("ERROR", error)
        return None, f"Failed: {e}"

def handle_voice_clone(audio_file):
    try:
        log_message("Cloning voice from", audio_file.name)
        output_path = clone_voice(audio_file)
        log_message("Voice cloned", output_path)
        return output_path
    except Exception as e:
        error = traceback.format_exc()
        log_message("ERROR", error)
        return None

with gr.Blocks(title="Aivideolab") as demo:
    gr.Markdown("## 🎬 Aivideolab - NSFW AI Video Generator")
    with gr.Tab("Prompt to Video"):
        prompt = gr.Textbox(label="Enter your video prompt")
        script = gr.Textbox(label="Optional: Add script for voice")
        gen_btn = gr.Button("Generate Video")
        gen_output = gr.Video()
        gen_status = gr.Textbox()
        gen_btn.click(handle_prompt_to_video, inputs=[prompt, script], outputs=[gen_output, gen_status])

    with gr.Tab("Deepfake from Image"):
        face = gr.Image(label="Upload face image")
        script2 = gr.Textbox(label="Script for deepfake video")
        fake_btn = gr.Button("Generate Deepfake")
        fake_output = gr.Video()
        fake_status = gr.Textbox()
        fake_btn.click(handle_deepfake, inputs=[face, script2], outputs=[fake_output, fake_status])

    with gr.Tab("Voice Clone"):
        audio = gr.Audio(label="Upload voice to clone", type="filepath")
        voice_btn = gr.Button("Clone Voice")
        voice_output = gr.Audio()
        voice_btn.click(handle_voice_clone, inputs=[audio], outputs=voice_output)

    with gr.Accordion("📜 Logs"):
        gr.Textbox(label="System Logs (check RunPod logs for full detail)", value="Logs output will stream to backend logs.")

demo.launch()