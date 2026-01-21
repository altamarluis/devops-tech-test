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
    # Leer y convertir imagen a base64
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')
    
    # Usar un modelo de visión que SÍ funciona
    payload = {
        "model": "Qwen/Qwen2.5-VL-7B-Instruct:hyperbolic",  # Este modelo SÍ funciona
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe this image in detail."},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}
                    }
                ]
            }
        ],
        "max_tokens": 500
    }
    
    response = requests.post(API_URL, headers=headers, json=payload)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content']
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")


# Uso
descripcion = analyze_image("cat.png")
print(descripcion)