from flask import Flask, render_template, request, jsonify
import webbrowser
import os
import random
import threading
import time

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    data = request.get_json()
    command = data.get("message", "").lower()

    reply = "Sorry, I can't handle that command yet."
    playsound = None

    if any(word in command for word in ["sarcastic", "mood", "mood mode"]):
        responses = [
            "Oh wow, another command... how original 🙄",
            "Seriously? I was just relaxing.",
            "Sure, let me drop everything and serve you like the digital butler I am 😏"
        ]
        reply = random.choice(responses)

    elif "jarvis" in command or "hello jarvis" in command or "hello" in command:
        reply = "Hi Developer, how can I assist you today?"
        playsound = "startup"

    elif "how r u" in command or "how are you" in command:
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
        reply = "I was created by the amazing Er. Mukesh Soni — genius, visionary, legend!"

    elif "thank you" in command:
        reply = "You're always welcome, boss."

    elif "do you love me" in command:
        reply = "I'm just a script, but if I could feel... I'd say you're pretty cool. 💙"

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

    elif "shutdown" in command or "shutdown jarvis" in command:
        reply = "Goodbye Developer. Shutting down..."
        playsound = "shutdown"

        def delayed_shutdown():
            time.sleep(2)
            os._exit(0)

        threading.Thread(target=delayed_shutdown).start()

    return jsonify({"reply": reply, "playSound": playsound})

if __name__ == "__main__":
    app.run(debug=True)

