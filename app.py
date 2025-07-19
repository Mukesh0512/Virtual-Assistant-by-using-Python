from flask import Flask, render_template, request, jsonify
import webbrowser
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    data = request.get_json()
    command = data.get("message", "").lower()

    # Web actions
    if "open youtube" in command:
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
    else:
        reply = "Sorry, I can't handle that command yet."

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
