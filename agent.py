import time
import string

from utils.audio import play
from detect_wake import WakeListener
from record import record

from stt.base_stt import BaseSTT
from llm.base_llm import BaseLLM
from tts.base_tts import BaseTTS

from stt.whisper_stt import WhisperSTTClient
from llm.gemini_llm import GeminiLLMClient
from tts.silero_tts import SileroTTSClient

class Agent:
    def __init__(
        self,
        stt_client: BaseSTT,
        llm_client: BaseLLM,
        tts_client: BaseTTS,
        silence_threshold: float = 1.5
    ):
        self.stt_client = stt_client
        self.llm_client = llm_client
        self.tts_client = tts_client

        self.silence_threshold = silence_threshold # sec
        self.start_sound_path = "sounds/record_start.wav"
        self.stop_sound_path = "sounds/record_end.wav"

        self.abort_keywords = ['abort', 'cancel', 'stop', 'no thanks']

        self.listener = WakeListener("./wake-words/ok-agent_en_linux_v3_0_0.ppn")
        self.listener.on_ready.subscribe(self._handle_ready)
        self.listener.on_wake.subscribe(self._handle_wake)

        self.running = False
        self.thread = None

        print(self)

    def __str__(self):
        return (
            f"\nAgent Info:\n"
            f"  STT Client: {self.stt_client.__class__.__name__}\n"
            f"  LLM Client: {self.llm_client.__class__.__name__}\n"
            f"  TTS Client: {self.tts_client.__class__.__name__}\n"
            f"  Silence Threshold: {self.silence_threshold}s,\n"
            f"  Abort Keywords: {self.abort_keywords}\n"
            f"  Listener: {self.listener.__class__.__name__}\n"
        )

    def _handle_ready(self):
        print("[INFO] Wake word detector ready")
        play('sounds/startup.wav')

    def _handle_wake(self):
        while True:
            print("[INFO] Wake word detected!")
            print("[INFO] Recording started... Wait for beep.")
            audio = record(
                silence_threshold=self.silence_threshold,
                start_sound_path=self.start_sound_path,
                stop_sound_path=self.stop_sound_path
            )

            print("[INFO] Transcribing...")
            text = self.stt_client.transcribe(audio)

            print("[INFO] Transcription: " + text)
            answer = self.llm_client.ask(question=text)

            if self._should_abort(text):
                play('sounds/abort.wav')
                print("[INFO] Aborting interaction.")
                break

            print("[INFO] LLM: " + answer)
            self.tts_client.speak(answer)

            if not self._should_continue_conversation(answer):
                break  # Exit the loop if conversation should not continue
    
    def _should_continue_conversation(self, answer):
        if not answer:
            return False
        return answer.strip().endswith('?')

    def _should_abort(self, text):
        if not text:
            return True
        cleaned_text = text.strip().rstrip(string.punctuation).lower()
        return any(cleaned_text.endswith(keyword) for keyword in self.abort_keywords)
    
    def start(self):
        print("[INFO] Agent starting...")
        self.listener.start()
        print("[INFO] Agent Started.")

        # Keep thread alive
        while True:
            time.sleep(1)