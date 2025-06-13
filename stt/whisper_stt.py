import soundfile as sf
import tempfile
import os
import whisper

from stt.base_stt import BaseSTT

# Audio params
SAMPLE_RATE = 16000

class WhisperSTTClient(BaseSTT):
    def __init__(self, model_size: str = "tiny"):
        self.model = whisper.load_model(model_size)

    def transcribe(self, audio_np) -> str:
        # Save numpy audio to temp WAV file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_wav:
            sf.write(tmp_wav.name, audio_np, SAMPLE_RATE)
            tmp_filename = tmp_wav.name

        try:
            result = self.model.transcribe(tmp_filename)
            transcript = result["text"]
        finally:
            os.remove(tmp_filename)

        return transcript
