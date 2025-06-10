import sounddevice as sd
import numpy as np
import torch
import os
from elevenlabs.client import ElevenLabs
from elevenlabs import play, stream

elevenlabs = ElevenLabs(
  api_key=os.getenv("ELEVENLABS_API_KEY"),
)

voice_id = os.getenv('ELEVENLABS_VOICE_ID')
model_id = os.getenv('ELEVENLABS_MODEL_ID')

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

def eleven_tts(text):
    audio = elevenlabs.text_to_speech.convert(
        text=text,
        voice_id=voice_id,
        model_id=model_id,
        output_format="mp3_44100_128",
    )
    play(audio)

def eleven_tts_stream(text):
    audio_stream = elevenlabs.text_to_speech.stream(
        text=text,
        voice_id=voice_id,
        model_id=model_id,
        output_format="mp3_44100_128",
    )
    stream(audio_stream)