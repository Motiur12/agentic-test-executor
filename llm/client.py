import json
import requests
import config


class LLM:

    def __init__(self):
        self.url = config.OLLAMA_URL
        self.model = config.MODEL

    def ask(self, system_prompt: str, user_prompt: str):

        payload = {
            "model": self.model,
            "stream": False,
            "format": "json",
            "options": {
                "temperature": config.TEMPERATURE
            },
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]
        }

        response = requests.post(
            self.url,
            json=payload,
            timeout=120
        )

        response.raise_for_status()

        content = response.json()["message"]["content"]

        return json.loads(content)