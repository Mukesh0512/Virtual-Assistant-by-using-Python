from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    query = request.form.get("query")
    response = f"You said: {query}"
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
