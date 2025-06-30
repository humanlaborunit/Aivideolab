import os
import uuid
import torchaudio
import tempfile
from pathlib import Path
from TTS.api import TTS

Path("cloned_voices").mkdir(exist_ok=True)

# Load voice cloning model (Tortoise TTS / Coqui TTS)
tts = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts", progress_bar=False)

def preprocess_voice(voice_sample_path):
    wav, sr = torchaudio.load(voice_sample_path)
    if wav.shape[0] > 1:
        wav = wav.mean(dim=0, keepdim=True)  # Convert to mono
    tmp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    torchaudio.save(tmp_file.name, wav, sample_rate=sr)
    return tmp_file.name

def clone_voice(script_text, voice_sample_path):
    try:
        clean_sample = preprocess_voice(voice_sample_path)
        output_path = f"cloned_voices/cloned_{uuid.uuid4()}.wav"
        tts.tts_to_file(
            text=script_text,
            speaker_wav=clean_sample,
            file_path=output_path
        )
        return output_path
    except Exception as e:
        raise RuntimeError(f"Voice cloning failed: {e}")