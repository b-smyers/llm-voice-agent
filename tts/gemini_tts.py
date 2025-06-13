from google import genai
from google.genai import types
from utils.play_sound import play_sound
import tempfile
import wave
import os

try:
    api_key = os.getenv("GEMINI_API_KEY")
except KeyError:
    raise ValueError("GEMINI_API_KEY environment variable not set.")

client = genai.Client(api_key=api_key)

model_id = "gemini-2.5-flash-preview-tts"
voice_name = 'Erinome'

config = types.GenerateContentConfig(
    response_modalities=["AUDIO"],
    speech_config=types.SpeechConfig(
        voice_config=types.VoiceConfig(
            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                voice_name=voice_name,
            )
        )
    )
)

voice_prompt = "Read aloud quickly with a calm, confident and tone: "

def gemini_tts(text: str, output_filename: str = 'output.wav'):
    def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(sample_width)
            wf.setframerate(rate)
            wf.writeframes(pcm)

    try:
        response = client.models.generate_content(
            model=model_id,
            contents=voice_prompt + text,
            config=config
        )

        audio_data = response.candidates[0].content.parts[0].inline_data.data

        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
            temp_filename = tmp_file.name
            wave_file(temp_filename, audio_data)

        # Play the generated sound
        play_sound(output_filename)
    except Exception as e:
        print(f"[ERROR]: Gemini TTS - {str(e)}")