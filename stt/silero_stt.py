import torch
import os

from utils.audio import temp_wave_file
from stt.base_stt import BaseSTT

class SileroSTTClient(BaseSTT):
    def __init__(self, device: str = 'cpu'):
        self.device = torch.device(device)

        # Load Silero STT model from torch.hub
        self.stt_model, self.stt_decoder, stt_utils = torch.hub.load(
            repo_or_dir='snakers4/silero-models',
            model='silero_stt',
            language='en',
            device=self.device,
            verbose=False
        )
        self.read_batch, self.split_into_batches, self.read_audio, self.prepare_model_input = stt_utils

        # Load Silero Text Enhancer (punctuation + capitalization)
        _, _, _, _, self.apply_te = torch.hub.load(
            repo_or_dir='snakers4/silero-models',
            model='silero_te',
            verbose=False
        )

    def transcribe(self, audio_np) -> str:
        tmp_filename = temp_wave_file(audio_np)

        try:
            batches = self.split_into_batches([tmp_filename], batch_size=1)
            input_tensor = self.prepare_model_input(self.read_batch(batches[0]), device=self.device)

            output = self.stt_model(input_tensor)
            transcripts = [self.stt_decoder(out.cpu()) for out in output]
            transcript = " ".join(transcripts)

            # Apply text enhancement (punctuation, capitalization)
            transcript = self.apply_te(transcript, lan='en')

        finally:
            os.remove(tmp_filename)

        return transcript.strip()