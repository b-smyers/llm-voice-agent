from dotenv import load_dotenv
load_dotenv()
import os
from agent import Agent

from stt.whisper_stt import WhisperSTTClient
from llm.gemini_llm import GeminiLLMClient
from tts.silero_tts import SileroTTSClient

def main():
    stt_client = WhisperSTTClient(model_size="tiny")
    llm_client = GeminiLLMClient(api_key=os.getenv("GEMINI_API_KEY"))
    tts_client = SileroTTSClient()

    agent = Agent(
        stt_client=stt_client,
        llm_client=llm_client,
        tts_client=tts_client
    )
    agent.start()

if __name__ == "__main__":
    main()