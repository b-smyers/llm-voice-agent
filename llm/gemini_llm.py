import os

from llm.base_llm import BaseLLM

from google import genai
from google.genai import types
from utils.tool_registry import tool_registry

# Imported to initialize tool decorators, do not remove
import utils.tools.advice
import utils.tools.time
import utils.tools.date
import utils.tools.quotes
import utils.tools.add
import utils.tools.ping

class GeminiLLMClient(BaseLLM):
    def __init__(self, prompt_path="internal_prompt.txt"):
        self.model_id = os.getenv("GEMINI_MODEL")

        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

        if not os.path.exists(prompt_path):
            raise FileNotFoundError(f"Prompt file not found at: {prompt_path}")
        
        with open(prompt_path, "r", encoding="utf-8") as f:
            self.internal_prompt = f.read().strip()

        self.config = types.GenerateContentConfig(
            system_instruction=self.internal_prompt,
            temperature=2,
            top_p=0.8,
            top_k=20,
            max_output_tokens=600,
            tools=tool_registry.get_tools_for_gemini_api(),
        )

        self.chat = self.client.chats.create(
            model=self.model_id,
            config=self.config
        )


    def ask(self, question: str) -> str:
        response = self.chat.send_message(
            message=question
        )

        return response.text.strip()
