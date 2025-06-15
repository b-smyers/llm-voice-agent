from dotenv import load_dotenv
load_dotenv()
from agent import Agent

from stt.whisper_stt import WhisperSTTClient
from llm.gemini_llm import GeminiLLMClient
from tts.silero_tts import SileroTTSClient

def main():
    stt_client = WhisperSTTClient(model_size="tiny")
    llm_client = GeminiLLMClient(prompt_path="internal_prompt.txt")
    tts_client = SileroTTSClient()

    agent = Agent(
        stt_client=stt_client,
        llm_client=llm_client,
        tts_client=tts_client
    )
    agent.start()

if __name__ == "__main__":
    main()