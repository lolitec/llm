import web
import os
from groq import Groq

os.environ["GROQ_API_KEY"] = "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"

urls = (
    "/", "Index",
    "/recetas/stylesheet/(.*)", "StaticHandler"  # Nueva ruta para archivos estáticos
)

app = web.application(urls, globals())
render = web.template.render("templates/")

class Index:
    def GET(self):
        return render.index(resultado=None)

    def POST(self):
        user_input = web.input().mensaje

        client = Groq()

        completion = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
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
            temperature=1,
            max_completion_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
        )

        respuesta = completion.choices[0].message.content
        return render.index(resultado=respuesta)

class StaticHandler:
    def GET(self, filename):
        filepath = os.path.join("stylesheet", filename)
        if os.path.exists(filepath):
            web.header("Content-Type", "text/css")
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
        else:
            return web.notfound("Archivo no encontrado")

if __name__ == "__main__":
    app.run()
