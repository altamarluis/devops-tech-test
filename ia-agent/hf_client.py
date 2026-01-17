import os
import requests

HF_API_TOKEN = os.getenv("HF_API_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/bigcode/starcoder"
HEADERS = {
    "Authorization": f"Bearer {HF_API_TOKEN}"
}

def analyze(prompt):
    response = requests.post(
        API_URL,
        headers=HEADERS,
        json={"inputs": prompt},
        timeout=60
    )
    response.raise_for_status()
    return response.json()[0]["generated_text"]
