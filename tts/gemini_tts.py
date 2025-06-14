import os
from google import genai
from google.genai import types
from utils.audio import play, temp_wave_file

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
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=self.voice_prompt + text,
                config=self.config
            )

            audio_np = response.candidates[0].content.parts[0].inline_data.data

            tmp_filename = temp_wave_file(audio_np=audio_np)

            # Play the generated sound
            play(tmp_filename)
        except Exception as e:
            print(f"[ERROR]: Gemini TTS - {str(e)}")
        finally:
            os.remove(tmp_filename)