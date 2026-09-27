from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello! My first Docker application is running."

@app.route("/health")
def health():
    return jsonify(status="healthy", container="my-python-container", code=200)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
