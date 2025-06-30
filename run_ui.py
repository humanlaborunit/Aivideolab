import os
import gradio as gr
import traceback
import time
from utils.video_generator import generate_video_from_prompt
from utils.deepfake_face_swap import swap_face
from utils.voice_cloner import clone_and_generate_voice
from utils.logger import log_step

def generate_all(prompt, face_image, audio_file, script_text):
    try:
        log_step("🟡 Starting generation process...")

        # Step 1: Generate video from prompt
        log_step("🟡 Generating base video from prompt...")
        base_video_path = generate_video_from_prompt(prompt)
        log_step(f"🟢 Prompt video generated: {base_video_path}")

        # Step 2: Swap face if image provided
        if face_image:
            log_step("🟡 Performing face swap...")
            base_video_path = swap_face(base_video_path, face_image)
            log_step(f"🟢 Face swapped: {base_video_path}")

        # Step 3: Generate audio from script or use uploaded audio
        if script_text:
            log_step("🟡 Generating voice from script...")
            audio_path = clone_and_generate_voice(script_text=script_text)
            log_step(f"🟢 Voice generated: {audio_path}")
        elif audio_file:
            log_step("🟡 Using uploaded voice file...")
            audio_path = audio_file
            log_step(f"🟢 Voice file selected: {audio_path}")
        else:
            log_step("🟡 No audio provided. Using silent video.")
            audio_path = None

        # Step 4: Merge audio and video
        log_step("🟡 Finalizing video output...")
        output_path = f"outputs/final_{int(time.time())}.mp4"
        cmd = f"ffmpeg -y -i {base_video_path} {'-i ' + audio_path + ' -c:v copy -c:a aac' if audio_path else '-c copy'} {output_path}"
        os.system(cmd)
        log_step(f"🟢 Final video created: {output_path}")

        return output_path, open("log.txt").read()
    
    except Exception as e:
        error_msg = f"🔴 Error occurred:\n{traceback.format_exc()}"
        log_step(error_msg)
        return None, error_msg

# Gradio UI
with gr.Blocks(title="AI Video Generator") as demo:
    gr.Markdown("# 🎬 AI Video Generator (NSFW-Enabled)")
    with gr.Row():
        prompt = gr.Textbox(label="Enter Video Prompt", placeholder="A hyper-realistic scene...")
        face_image = gr.Image(type="filepath", label="Optional: Face Image (for deepfake)")
    with gr.Row():
        audio_file = gr.Audio(type="filepath", label="Optional: Upload voice audio (MP3/WAV)")
        script_text = gr.Textbox(label="Optional: Script text (will be converted to voice)", lines=3)

    btn = gr.Button("Generate Video")
    output_video = gr.Video(label="Generated Video")
    logs = gr.Textbox(label="Process Log", lines=15)

    btn.click(fn=generate_all, inputs=[prompt, face_image, audio_file, script_text], outputs=[output_video, logs])

demo.launch(server_name="0.0.0.0", server_port=7860)