import requests
import os
import base64

HF_TOKEN = os.getenv("HF_API_TOKEN")
API_URL = "https://router.huggingface.co/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

def analyze_image(image_path: str) -> str:
    if not HF_TOKEN:
        raise Exception("HF_API_TOKEN not set")

    if not os.path.exists(image_path):
        raise Exception(f"Image not found: {image_path}")
    
    # Read image and encode as base64
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')
    
    payload = {
        "model": "Qwen/Qwen2.5-VL-7B-Instruct:hyperbolic",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Analyze this frontend screenshot and describe any visible UI or layout."},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}
                    }
                ]
            }
        ],
        "max_tokens": 500
    }
    
    response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    response.raise_for_status()

    result = response.json()

    # Defensive parsing (important for LLMs)
    try:
        return result["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        raise Exception(f"Unexpected HF response format: {result}")