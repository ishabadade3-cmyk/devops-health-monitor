
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <html>
        <head>
            <title>DevOps Health Monitor</title>
        </head>
        <body style="font-family: Arial; text-align: center;
                     margin-top: 100px;">
            <h1>DevOps Health Monitor</h1>
            <h2 style="color: green;">Application is Running!</h2>
            <p>Your first DevOps project is working.</p>
            <p>Built using Python and Flask.</p>
            <a href="/health">Check Application Health</a>
        </body>
    </html>
    """


@app.route("/health")
def health():
    return jsonify(
        status="ok",
        message="DevOps Health Monitor is healthy"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
