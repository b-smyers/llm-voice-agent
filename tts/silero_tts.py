from utils.audio import play, temp_wave_file, resample
import numpy as np
import torch
import os

from tts.base_tts import BaseTTS

class SileroTTSClient(BaseTTS):
    def __init__(self,
                 language: str = 'en',
                 speaker: str = 'v3_en',
                 speaker_id: int = 30):
        self.sample_rate = 8000
        self.language = language
        self.speaker_id = speaker_id

        self.model, self.utils = torch.hub.load(
            repo_or_dir='snakers4/silero-models',
            model='silero_tts',
            language=language,
            speaker=speaker,
            verbose=False
        )

    def speak(self, text: str):
        if len(text) > 1000:
            print("[WARN] Text too long to process.")
            text = "The text was too long to process"
        
        speaker_tag = f'{self.language}_{self.speaker_id}'

        audio_np = self.model.apply_tts(
            text,
            speaker=speaker_tag,
            sample_rate=self.sample_rate
        )

        # Ensure audio is 1D
        audio_np = np.squeeze(audio_np)

        # Resample audio
        audio_np = resample(audio_np=audio_np, original_rate=self.sample_rate, target_rate=16000)

        tmp_filename = temp_wave_file(audio_np)
        play(tmp_filename)
        os.remove(tmp_filename)