import os
import requests

class GeminiChatClient:
    def __init__(self, prompt_path="internal_prompt.txt"):
        self.location = os.getenv("GEMINI_LOCATION")
        self.project_id = os.getenv("GEMINI_PROJECT_ID")
        self.model_id = os.getenv("GEMINI_MODEL")
        self.api_key = os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            raise EnvironmentError("GEMINI_API_KEY not found in environment variables.")
        
        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_id}:generateContent?key={self.api_key}"
        self.headers = {"Content-Type": "application/json"}

        if not os.path.exists(prompt_path):
            raise FileNotFoundError(f"Prompt file not found at: {prompt_path}")
        
        with open(prompt_path, "r", encoding="utf-8") as f:
            self.internal_prompt = f.read().strip()

        self.contents = [
            {
                "role": "user",
                "parts": [{"text": self.internal_prompt}]
            }
        ]

    def ask(self, question: str) -> str:
        self.contents.append(
            {
                "role": "user",
                "parts": [{"text": question}]
            }
        )

        payload = {
            "contents": self.contents,
            "generationConfig": {
                "temperature": 2.0,
                "maxOutputTokens": 600,
                "topP": 0.8,
                "topK": 15
            },
            "tools": [{
                "googleSearch": {}
            }],
            "model": f"projects/{self.project_id}/locations/{self.location}/publishers/google/models/{self.model_id}"
        }

        response = requests.post(self.url, headers=self.headers, json=payload)
        if response.status_code != 200:
            raise RuntimeError(f"Gemini API call failed: {response.status_code} - {response.text}")

        try:
            answer = response.json()["candidates"][0]["content"]["parts"][0]["text"]
            self.contents.append({"role": "model", "parts": [{"text": answer}]})
            return answer.strip()
        except (KeyError, IndexError):
            raise ValueError("Unexpected response format from Gemini API")
