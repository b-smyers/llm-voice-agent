import os
from elevenlabs.client import ElevenLabs
from elevenlabs import play, stream

from tts.base_tts import BaseTTS

class ElevenLabsTTSClient(BaseTTS):
    def __init__(self):
        api_key = os.getenv("ELEVENLABS_API_KEY")
        self.voice_id = os.getenv("ELEVENLABS_VOICE_ID")
        self.model_id = os.getenv("ELEVENLABS_MODEL_ID")
        
        assert api_key, "ELEVENLABS_API_KEY environment variable not set."
        assert self.voice_id, "ELEVENLABS_VOICE_ID environment variable not set."
        assert self.model_id, "ELEVENLABS_MODEL_ID environment variable not set."

        self.client = ElevenLabs(api_key=api_key)

    # TTS stream
    def speak(self, text: str):
        audio_stream = self.client.text_to_speech.stream(
            text=text,
            voice_id=self.voice_id,
            model_id=self.model_id,
            output_format="mp3_44100_128",
        )
        stream(audio_stream)

    # TTS non-stream
    # def speak(self, text: str):
    #     audio = self.client.text_to_speech.convert(
    #         text=text,
    #         voice_id=self.voice_id,
    #         model_id=self.model_id,
    #         output_format="mp3_44100_128",
    #     )
    #     play(audio)