import os
import requests
import base64
from flask import Flask, request, render_template
from dotenv import load_dotenv

load_dotenv()
HF_API_TOKEN = os.getenv("HUGGINGFACE_API_KEY")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.form.get('prompt')
    print("Prompt:", prompt)

    if not prompt:
        return render_template('index.html', error="No prompt provided")

    headers = {
        "Authorization": f"Bearer {HF_API_TOKEN}",
        "Content-Type": "application/json"
    }

    data = { "inputs": prompt }

    model_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    response = requests.post(model_url, headers=headers, json=data)

    print("Status Code:", response.status_code)

    if response.status_code == 200:
        image_base64 = base64.b64encode(response.content).decode("utf-8")
        image_url = f"data:image/png;base64,{image_base64}"
        return render_template('index.html', image_url=image_url, prompt=prompt)
    else:
        print("Error:", response.text)
        return render_template('index.html', error="API Error", details=response.text)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
