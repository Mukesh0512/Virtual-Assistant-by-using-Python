from flask import Flask, render_template, request, jsonify
import openai
import os
from gtts import gTTS
import pygame

app = Flask(__name__)

# Set your OpenAI API key here
openai.api_key = "<YOUR_OPENAI_KEY>"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_input = data["message"]

    try:
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant named Jarvis."},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response['choices'][0]['message']['content']
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": "Error: " + str(e)})

if __name__ == "__main__":
    app.run(debug=True)
