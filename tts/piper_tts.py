import os
import numpy as np
from piper.voice import PiperVoice
from utils.audio import play, temp_wave_file, resample

from tts.base_tts import BaseTTS

class PiperTTSClient(BaseTTS):
    def __init__(self, model_path: str = f"voice.onnx"):
        self.voice = PiperVoice.load(model_path)

    def speak(self, text: str):
        # Concatenate all audio chunks into a single buffer
        audio_chunks = []
        for audio_bytes in self.voice.synthesize_stream_raw(text):
            int_data = np.frombuffer(audio_bytes, dtype=np.int16)
            audio_chunks.append(int_data)

        # Flatten the list into a numpy array
        audio_np = np.concatenate(audio_chunks)
        
        audio_np = audio_np.astype(np.float32) / 32768.0

        audio_np = resample(audio_np=audio_np, original_rate=self.voice.config.sample_rate, target_rate=16000)

        tmp_filename = temp_wave_file(audio_np=audio_np)

        play(tmp_filename)
        os.remove(tmp_filename)