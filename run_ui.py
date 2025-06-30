import os
import gradio as gr
import subprocess
import uuid
import shutil

# Directories for all outputs
os.makedirs("outputs", exist_ok=True)
os.makedirs("logs", exist_ok=True)

def log_step(step_msg):
    with open("logs/latest_log.txt", "a") as f:
        f.write(f"{step_msg}\n")

def reset_logs():
    with open("logs/latest_log.txt", "w") as f:
        f.write("== GENERATION START ==\n")

def generate_video(prompt, script, face_image, audio_file):
    reset_logs()
    job_id = str(uuid.uuid4())[:8]
    output_dir = f"outputs/{job_id}"
    os.makedirs(output_dir, exist_ok=True)

    log_step(f"Step 1: Prompt received: {prompt}")
    log_step(f"Step 2: Script received: {script[:60]}...")

    face_path = "input_face.png"
    if face_image:
        face_image.save(face_path)
        log_step("Step 3: Face image saved.")
    else:
        return "Error: No face image provided.", None, "logs/latest_log.txt"

    if script:
        with open(f"{output_dir}/script.txt", "w") as f:
            f.write(script)

    audio_path = ""
    if audio_file:
        audio_path = os.path.join(output_dir, "voice.wav")
        shutil.copy(audio_file, audio_path)
        log_step("Step 4: Uploaded voice cloned.")
    else:
        audio_path = os.path.join(output_dir, "voice_bark.wav")
        log_step("Step 4: Generating voice with Bark...")
        subprocess.run([
            "python3", "modules/bark_gen.py",
            "--text", script,
            "--output", audio_path
        ])
        log_step("✓ Voice generation complete.")

    log_step("Step 5: Generating face motion with SadTalker...")
    subprocess.run([
        "python3", "modules/sadtalker_gen.py",
        "--face", face_path,
        "--audio", audio_path,
        "--output_dir", output_dir
    ])
    log_step("✓ Face animation complete.")

    log_step("Step 6: Running Wav2Lip sync...")
    subprocess.run([
        "python3", "modules/wav2lip_sync.py",
        "--video", f"{output_dir}/sadtalker_output.mp4",
        "--audio", audio_path,
        "--output", f"{output_dir}/final_lipsync.mp4"
    ])
    log_step("✓ Wav2Lip processing complete.")

    log_step("Step 7: Running AnimateDiff video from prompt...")
    subprocess.run([
        "python3", "modules/animatediff_gen.py",
        "--prompt", prompt,
        "--output", f"{output_dir}/prompt2vid.mp4"
    ])
    log_step("✓ Prompt-to-video complete.")

    log_step("Step 8: Merging all elements...")
    final_path = f"{output_dir}/final_output.mp4"
    subprocess.run([
        "ffmpeg", "-y",
        "-i", f"{output_dir}/prompt2vid.mp4",
        "-i", f"{output_dir}/final_lipsync.mp4",
        "-filter_complex", "[0:v][1:v]hstack=inputs=2[v]",
        "-map", "[v]", "-map", "1:a",
        "-c:v", "libx264", "-c:a", "aac",
        final_path
    ])
    log_step("✓ Final video rendered.")

    return "✓ Generation complete", final_path, "logs/latest_log.txt"

with gr.Blocks() as demo:
    gr.Markdown("## 🎬 AI Video Lab — NSFW Video Generator")
    with gr.Row():
        with gr.Column():
            prompt = gr.Textbox(label="Prompt (e.g. 'Realistic female model doing yoga')")
            script = gr.Textbox(label="Spoken Script", lines=3)
            face_image = gr.Image(label="Upload Face Image", type="pil")
            audio_file = gr.Audio(label="Upload Voice Audio (Optional)", type="filepath")
            submit_btn = gr.Button("Generate Video 🔥")
        with gr.Column():
            status = gr.Textbox(label="Status")
            final_video = gr.Video(label="Generated Video", format="mp4")
            log_output = gr.File(label="View Generation Log")

    submit_btn.click(
        generate_video,
        inputs=[prompt, script, face_image, audio_file],
        outputs=[status, final_video, log_output]
    )

demo.launch(server_name="0.0.0.0", server_port=7860)
