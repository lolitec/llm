import web
import os
import re
from groq import Groq

os.environ["GROQ_API_KEY"] = "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"

urls = ("/", "Index")
app = web.application(urls, globals())
render = web.template.render("templates/")

# Función para eliminar el 'razonamiento' de la IA.
def limpiar_respuesta(texto):
    return re.sub(r"<think>.*?</think>", "", texto, flags=re.DOTALL).strip()

class Index:
    def GET(self):
        return render.index(resultado=None)

    def POST(self):
        user_input = web.input().mensaje

        client = Groq()

        completion = client.chat.completions.create(
            model="qwen-qwq-32b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Eres un chef experto. Responde siempre con una receta directa, clara y detallada "
                        "solo cuando el usuario te indique el nombre de un platillo. No pidas más detalles. "
                        "No expliques lo que haces ni hables sobre tu capacidad, solo da la receta. "
                        "Si el usuario no menciona un platillo, responde con 'No puedo ayudarte con eso'."
                    )
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            temperature=0.6,
            max_tokens=1024,
            top_p=0.95,
            stream=False,
        )

        respuesta = limpiar_respuesta(completion.choices[0].message.content)
        return render.index(resultado=respuesta)

if __name__ == "__main__":
    app.run()
