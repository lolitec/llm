# llm
Modelos de lenguaje largo

curl http://localhost:11434/api/generate -d '{
  "model": "gemma3:1b",
  "prompt":"¿Por que el cielo es azul?",
  "stream":false
}'