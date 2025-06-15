import os

from llm.base_llm import BaseLLM

from google import genai
from google.genai import types
from utils.tool_registry import tool_registry

class GeminiLLMClient(BaseLLM):
    def __init__(self,
                 api_key: str,
                 model_id: str = "gemini-2.0-flash",
                 system_prompt_path: str = "internal_prompt.txt",
                 is_tools_enabled: bool = False,
                 temperature: float = 2,
                 top_p: float = 0.8,
                 top_k: int = 20,
                 max_tokens: int = 600):
        self.client = genai.Client(api_key=api_key)

        if not os.path.exists(system_prompt_path):
            raise FileNotFoundError(f"Prompt file not found at: {system_prompt_path}")
        
        with open(system_prompt_path, "r", encoding="utf-8") as f:
            system_prompt = f.read().strip()
            
        tools = None
        if is_tools_enabled:
            # Imports initialize tool decorators, do not remove
            import utils.tools.advice
            import utils.tools.time
            import utils.tools.date
            import utils.tools.quotes
            import utils.tools.add
            import utils.tools.ping
            tools = tool_registry.get_tools_for_gemini_api()

        self.config = types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            max_output_tokens=max_tokens,
            **({'tools': tools} if tools is not None else {})
        )

        self.chat = self.client.chats.create(
            model=model_id,
            config=self.config
        )


    def ask(self, question: str) -> str:
        response = self.chat.send_message(
            message=question
        )

        return response.text.strip()
