import requests

# Pon tu token aquí directamente
HF_TOKEN = "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"

API_URL = "https://router.huggingface.co/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

payload = {
    "model": "Qwen/Qwen2.5-Coder-7B-Instruct",
    "messages": [
        {
            "role": "user",
            "content": "Write a simple FastAPI health endpoint"
        }
    ],
    "max_tokens": 500
}

response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=60)

print("STATUS:", response.status_code)
print("--- RESPUESTA ---")
print(response.text)

if response.status_code == 200:
    result = response.json()
    print("\n--- CÓDIGO GENERADO ---")
    print(result['choices'][0]['message']['content'])