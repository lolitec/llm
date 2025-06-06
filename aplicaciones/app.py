import requests

data = {
  "model": "gemma3:1b",
  "prompt":"¿Por que el cielo es azul?"
}

url = "http://localhost:11434/api/generate"

response = requests.post(url, json=data)

print(response.text)
