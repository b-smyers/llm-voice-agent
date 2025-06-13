import os
import tempfile
import wave
from google import genai
from google.genai import types
from utils.play_sound import play_sound

from tts.base_tts import BaseTTS

class GeminiTTSClient(BaseTTS):
    def __init__(self,
                 model_id: str = "gemini-2.5-flash-preview-tts",
                 voice_name: str = 'Erinome',
                 voice_prompt: str = "Read aloud quickly with a calm, confident and tone: "):
        api_key = os.getenv("GEMINI_API_KEY")

        assert api_key, "GEMINI_API_KEY environment variable not set."
        
        self.client = genai.Client(api_key=api_key)
        self.model_id = model_id
        self.voice_prompt = voice_prompt

        self.config = types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name=voice_name,
                    )
                )
            )
        )

    def speak(self, text: str):
        def save_wave_file(filename, pcm_data, channels=1, rate=24000, sample_width=2):
            with wave.open(filename, "wb") as wf:
                wf.setnchannels(channels)
                wf.setsampwidth(sample_width)
                wf.setframerate(rate)
                wf.writeframes(pcm_data)

        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=self.voice_prompt + text,
                config=self.config
            )

            audio_data = response.candidates[0].content.parts[0].inline_data.data

            # Write to temporary WAV file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                temp_filename = tmp_file.name
                save_wave_file(temp_filename, audio_data)

            # Play the generated sound
            play_sound(temp_filename)

        except Exception as e:
            print(f"[ERROR]: Gemini TTS - {str(e)}")