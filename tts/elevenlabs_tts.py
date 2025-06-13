import os
from elevenlabs.client import ElevenLabs
from elevenlabs import play, stream

elevenlabs = ElevenLabs(
  api_key=os.getenv("ELEVENLABS_API_KEY"),
)

voice_id = os.getenv('ELEVENLABS_VOICE_ID')
model_id = os.getenv('ELEVENLABS_MODEL_ID')

def elevenlabs_tts(text):
    audio = elevenlabs.text_to_speech.convert(
        text=text,
        voice_id=voice_id,
        model_id=model_id,
        output_format="mp3_44100_128",
    )
    play(audio)

def elevenlabs_tts_stream(text):
    audio_stream = elevenlabs.text_to_speech.stream(
        text=text,
        voice_id=voice_id,
        model_id=model_id,
        output_format="mp3_44100_128",
    )
    stream(audio_stream)