import os
import whisper

from utils.audio import temp_wave_file
from stt.base_stt import BaseSTT

class WhisperSTTClient(BaseSTT):
    def __init__(self, model_size: str = "tiny"):
        self.model = whisper.load_model(model_size)

    def transcribe(self, audio_np) -> str:
        tmp_filename = temp_wave_file(audio_np)

        try:
            result = self.model.transcribe(tmp_filename)
            transcript = result["text"]
        finally:
            os.remove(tmp_filename)

        return transcript
