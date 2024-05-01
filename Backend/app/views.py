from flask import request, Response
from . import app
from openai import OpenAI, RateLimitError

client = OpenAI()

@app.route("/")
def hello_world():
    return "Hello, World!"

@app.post('/translate')
def translate():
    try:
        # Read plain text from the POST body
        text = request.data.decode('utf-8').strip()

        if not text:
            return Response("Please input something", mimetype='text/plain', status=400)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Translate the following text to Chinese."},
                {"role": "user", "content": text}
            ],
            stream=True
        )
        translation = response.choices[0].message['content']
        return Response(translation, mimetype='text/plain')
    except RateLimitError:
        error_message = "Translation service is currently unavailable due to rate limit. Please try again later."
        return Response(error_message, mimetype='text/plain', status=503)