import soundfile as sf
import tempfile
import whisper

# Audio params
SAMPLE_RATE = 16000

def whisper_stt(audio_np) -> str:
    # Save numpy audio to temp WAV file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_wav:
        sf.write(tmp_wav.name, audio_np, SAMPLE_RATE)
        tmp_filename = tmp_wav.name

    model = whisper.load_model("tiny")
    result = model.transcribe(tmp_filename)
    return result["text"]
