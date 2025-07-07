import requests
import os
from dotenv import load_dotenv
load_dotenv()

def get_groq_response(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {
                "role": "system",
                "content": "Tu es un assistant pédagogique intelligent et bienveillant.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    }

    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
