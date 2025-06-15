import os
from elevenlabs.client import ElevenLabs
from elevenlabs import play, stream

from tts.base_tts import BaseTTS

# Model IDs
# eleven_multilingual_v2 - Highest quality, Larger latency
# eleven_flash_v2_5 - Lower quality, Super low latency
# eleven_turbo_v2_5 - Mixed quality, Mixed latency

# Example Voice IDs (more on ElevenLabs website)
# Daniel - onwK4e9ZLuTAKqWW03F9 (deep voice narrator)
# Elli - MF3mGyEYCl7XYWbV9V6O (riled up, can be agressive)
# Jessica - cgSgspJ2msm6clMCkdW9 (more cheery)
# Racheal - 21m00Tcm4TlvDq8ikWAM (laid back)

class ElevenLabsTTSClient(BaseTTS):
    def __init__(self,
                 api_key: str,
                 model_id: str = "21m00Tcm4TlvDq8ikWAM",
                 voice_id: str = "eleven_flash_v2_5"):
        self.model_id = model_id
        self.voice_id = voice_id
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