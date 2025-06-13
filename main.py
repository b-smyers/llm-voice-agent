from dotenv import load_dotenv
load_dotenv()
import time

from detect_wake import WakeListener
from record import record
from stt.silero_stt import silero_stt
from llm.gemini_llm import GeminiChatClient
from tts.elevenlabs_tts import elevenlabs_tts_stream
from tts.silero_tts import silero_tts

# Init
is_debug = True
chat = GeminiChatClient()

def handle_ready():
    print("[INFO] Wake word detector ready")

def handle_wake():
    print("[INFO] Wake word detected!")
    print("[INFO] Recording started... Wait for beep.")
    audio = record()
    print("[INFO] Transcribing...")
    question = silero_stt(audio)
    print("[INFO] Transcription: " + question)
    answer = chat.ask(question=question)
    print("[INFO] Gemini: " + answer)
    if is_debug: # save ElevenLabs credits for production use
        silero_tts(answer)
    else:
        if len(answer) > 400: # to save on ElevenLabs credits
            silero_tts(answer)
        else:
            elevenlabs_tts_stream(answer)

def main():
    # Init
    listener = WakeListener("./wake-words/ok-agent_en_linux_v3_0_0.ppn")
    listener.on_ready.subscribe(handle_ready)
    listener.on_wake.subscribe(handle_wake)
    listener.start()

    # Keep the main thread alive
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()