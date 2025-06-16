import web
import requests
import json

urls = (
    '/', 'Index'
)
render = web.template.render('templates')
app = web.application(urls, globals())

class Index:
    def GET(self):
        return "render.generate()"
    
    def POST(self):
        formulario = web.input()
        prompt = formulario.inp_prompt
        data = {
        "model": "gemma3:1b",
        "prompt":prompt,
        "stream":False
        }

        url = "http://localhost:11434/api/generate"

        response = requests.post(url, json=data)
        response = json.loads(response.text)
        response = response["response"]

        return render.generate(response)

if __name__ == "__main__":
    app.run()