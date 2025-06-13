import sounddevice as sd
import numpy as np
import torch

from tts.base_tts import BaseTTS

class SileroTTSClient(BaseTTS):
    def __init__(self):
        self.sample_rate = 8000
        self.speaker_id = 30

        self.model, self.utils = torch.hub.load(
            repo_or_dir='snakers4/silero-models',
            model='silero_tts',
            language='en',
            speaker='v3_en'
        )

    def speak(self, text: str):
        speaker_tag = f'en_{self.speaker_id}'

        audio = self.model.apply_tts(
            text,
            speaker=speaker_tag,
            sample_rate=self.sample_rate
        )

        # Ensure audio is 1D
        audio = np.squeeze(audio)

        # Play the generated audio
        sd.play(audio, samplerate=self.sample_rate)
        sd.wait()