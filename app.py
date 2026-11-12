import logging

from flask import Flask, jsonify, render_template

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

app = Flask(__name__)


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/health")
def health():
    app.logger.info("Health check succeeded")
    return jsonify(
        status="ok",
        message="DevOps Health Monitor is healthy",
    ), 200


if __name__ == "__main__":
    app.logger.info("Starting DevOps Health Monitor on 0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000, debug=False)
