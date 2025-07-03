import gradio as gr
import os
from video_gen import generate_full_video
from voice_clone import clone_voice
from face_swap import run_face_swap

LOGS = []

def log(msg):
    print(msg, flush=True)
    LOGS.append(msg)
    return "\n".join(LOGS[-100:])

def generate_video_ui(prompt, script, face_image, voice_sample):
    LOGS.clear()
    try:
        log("🧠 Starting generation process...")

        voice_path = None
        if voice_sample:
            log("📜 Step 1: Cloning voice...")
            voice_path = clone_voice(script, voice_sample)
            if voice_path and os.path.exists(voice_path):
                log(f"✅ Voice cloned: {voice_path}")
            else:
                log("⚠️ Voice cloning skipped or failed.")
        else:
            log("⚠️ No voice sample provided — skipping voice cloning.")

        log("🎞 Step 2: Generating video from prompt...")
        base_video = generate_full_video(prompt, voice_path)
        if not os.path.exists(base_video):
            raise Exception("Generated video file not found.")
        log(f"✅ Base video generated: {base_video}")

        if face_image:
            log("😶 Step 3: Running face swap...")
            swapped_video = run_face_swap(base_video, face_image)
            if not os.path.exists(swapped_video):
                raise Exception("Face swap output missing.")
            log(f"✅ Face-swapped video created: {swapped_video}")
        else:
            swapped_video = base_video
            log("⚠️ No face image provided — skipping face swap.")

        log("🎉 All steps completed successfully.")
        return swapped_video, log("✅ Done!")
    except Exception as e:
        return None, log(f"❌ Error: {e}")

with gr.Blocks(css=".gradio-container { max-width: 100% !important; }") as demo:
    gr.Markdown("## 🎬 AI Video Generator (NSFW Enabled by Default)")

    with gr.Row():
        prompt = gr.Textbox(label="Text Prompt (Scene/Setting)", placeholder="A realistic scene of...")
        script = gr.Textbox(label="Script (Spoken in Video)", placeholder="Enter the spoken dialogue")

    with gr.Row():
        face_image = gr.Image(label="Optional Face Image (for Deepfake)", type="filepath")
        voice_sample = gr.Audio(label="Optional Voice Sample (for cloning)", type="filepath")

    with gr.Row():
        generate_btn = gr.Button("Generate Video")
        output_video = gr.Video(label="📤 Final Video Output")

    logs_output = gr.Textbox(label="🔍 Logs / Progress", lines=20)

    generate_btn.click(
        fn=generate_video_ui,
        inputs=[prompt, script, face_image, voice_sample],
        outputs=[output_video, logs_output]
    )

if __name__ == "__main__":
    try:
        demo.queue(concurrency_count=3).launch(
            server_name="0.0.0.0",
            server_port=3000,
            share=False,
            inbrowser=False,
            show_error=True,
            show_tips=True,
            prevent_thread_lock=True
        )
    except Exception as e:
        import traceback
        os.makedirs("/app/logs", exist_ok=True)
        with open("/app/logs/fatal_ui_crash.txt", "w") as f:
            traceback.print_exc(file=f)
        print("❌ Fatal crash in Gradio UI launch. Check /app/logs/fatal_ui_crash.txt")
        while True:
            pass