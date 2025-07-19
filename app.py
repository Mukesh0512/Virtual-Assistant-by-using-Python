from flask import Flask, render_template, request, jsonify
import webbrowser
import os
import random

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    data = request.get_json()
    command = data.get("message", "").lower()

    reply = "Sorry, I can't handle that command yet."

    # Sarcastic mode responses
    sarcastic_mode = any(word in command for word in ["sarcastic", "mood", "mood mode"])
    if sarcastic_mode:
        responses = [
            "Oh wow, another command... how original 🙄",
            "Seriously? I was just relaxing.",
            "Sure, let me drop everything and serve you like the digital butler I am 😏"
        ]
        reply = random.choice(responses)
        return jsonify({"reply": reply})

    # Greetings
    if "jarvis" in command or "hello jarvis" in command:
        reply = "Hi Developer, how can I assist you today?"

    # Custom talks
    elif "how are you" in command:
        responses = [
            "Running 99.99% error-free!",
            "Doing great, just debugging myself.",
            "As good as code can get!",
            "Faster than ever. What’s next?"
        ]
        reply = random.choice(responses)

    elif "tell me a joke" in command:
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "Why did the function stop calling? Because it had constant arguments!",
            "Debugging: Being the detective in a crime movie where you are also the murderer."
        ]
        reply = random.choice(jokes)

    elif "what's your name" in command:
        reply = "I’m Jarvis, your personal voice assistant. And part-time superhero sidekick."

    elif "who created you" in command:
        reply = "I was created by the amazing Mukesh Soni — genius, visionary, legend!"

    elif "thank you" in command:
        reply = "You're always welcome, boss."

    elif "do you love me" in command:
        reply = "I'm just a script, but if I could feel... I'd say you're pretty cool. 💙"

    # Web opening commands
    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
        reply = "Opening YouTube."
    elif "open google" in command:
        webbrowser.open("https://google.com")
        reply = "Opening Google."
    elif "open facebook" in command:
        webbrowser.open("https://facebook.com")
        reply = "Opening Facebook."
    elif "open linkedin" in command:
        webbrowser.open("https://linkedin.com")
        reply = "Opening LinkedIn."
    elif "shutdown" in command:
        os._exit(0)


    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
