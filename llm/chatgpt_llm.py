import os
from openai import OpenAI

from llm.base_llm import BaseLLM
from utils.tool_registry import tool_registry

class ChatGPTLLMClient(BaseLLM):
    def __init__(self,
                 api_key: str,
                 model_id: str = "gpt-4.1-nano-2025-04-14",
                 system_prompt_path: str = None,
                 is_tools_enabled: bool = False,
                 temperature: float = 0.7,
                 top_p: float = 0.9,
                 max_tokens: int = 600):
        self.client = OpenAI(api_key=api_key)

        if system_prompt_path:
            if not os.path.exists(system_prompt_path):
                raise FileNotFoundError(f"Prompt file not found at: {system_prompt_path}")

            with open(system_prompt_path, "r", encoding="utf-8") as f:
                system_prompt = f.read().strip()
        else:
            system_prompt = ""

        self.model_id = model_id
        self.system_prompt = {"role": "system", "content": system_prompt}
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens

        self.tools = []
        if is_tools_enabled:
            # TODO: Add tools
            pass

        # Chat history starts with system prompt
        self.chat_history = [self.system_prompt]

    def _get_chat_history(self, max_characters=8192):
        history = []
        total_chars = 0

        # Always include system prompt
        system_prompt = self.chat_history[0]
        history.append(system_prompt)
        total_chars += len(system_prompt['content'])

        recent_messages = []

        # Process rest of the history in reverse (newest first)
        for message in reversed(self.chat_history[1:]):
            message_chars = len(message['content'])
            if total_chars + message_chars > max_characters:
                break
            recent_messages.insert(0, message)
            total_chars += message_chars

        history.extend(recent_messages)

        return history

    def ask(self, question: str) -> str:
        self.chat_history.append({"role": "user", "content": question})

        response = self.client.chat.completions.create(
            model=self.model_id,
            messages=self._get_chat_history(),
            temperature=self.temperature,
            top_p=self.top_p,
            max_tokens=self.max_tokens,
            tools=self.tools if self.tools else None,
            tool_choice="auto" if self.tools else None
        )

        # Extract assistant's reply
        assistant_message = response.choices[0].message.content.strip()

        # Append the assistant's response to history
        self.chat_history.append({"role": "assistant", "content": assistant_message})

        return assistant_message