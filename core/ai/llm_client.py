import requests

class LLMClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://api.groq.com/openai/v1/chat/completions"

    def generate(self, prompt):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": "You are a CNC expert assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3
        }

        response = requests.post(self.url, headers=headers, json=data)

        if response.status_code != 200:
            raise Exception(f"API Error: {response.text}")

        return response.json()["choices"][0]["message"]["content"]