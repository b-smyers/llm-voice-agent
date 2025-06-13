import torch
import soundfile as sf
import tempfile
import os

from stt.base_stt import BaseSTT

# Audio params
SAMPLE_RATE = 16000

class SileroSTTClient(BaseSTT):
    def __init__(self, device: str = 'cpu'):
        self.device = torch.device(device)

        # Load Silero STT model from torch.hub
        self.stt_model, self.stt_decoder, stt_utils = torch.hub.load(
            repo_or_dir='snakers4/silero-models',
            model='silero_stt',
            language='en',
            device=self.device
        )
        self.read_batch, self.split_into_batches, self.read_audio, self.prepare_model_input = stt_utils

        # Load Silero Text Enhancer (punctuation + capitalization)
        _, _, _, _, self.apply_te = torch.hub.load(
            repo_or_dir='snakers4/silero-models',
            model='silero_te'
        )

    def transcribe(self, audio_np) -> str:
        # Save numpy audio to temp WAV file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_wav:
            sf.write(tmp_wav.name, audio_np, SAMPLE_RATE)
            tmp_filename = tmp_wav.name

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

        return transcript