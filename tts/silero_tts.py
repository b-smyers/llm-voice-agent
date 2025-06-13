import sounddevice as sd
import numpy as np
import torch

def silero_tts(text, sample_rate=8000):
    model, utils = torch.hub.load(
        repo_or_dir='snakers4/silero-models',
        model='silero_tts',
        language='en',
        speaker='v3_en'
    )
    
    speaker_num = 30 # 103 also sounds good

    audio = model.apply_tts(
        text,
        speaker='en_' + str(speaker_num),
        sample_rate=sample_rate
    )

    # Ensure audio shape is 1D for mono output
    audio = np.squeeze(audio)
    
    # Play audio
    sd.play(audio, samplerate=sample_rate)
    sd.wait()