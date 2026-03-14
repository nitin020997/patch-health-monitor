import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/health")
def health():
    return jsonify({
        "server_name": os.getenv("SERVER_NAME"),
        "domain_joined": os.getenv("DOMAIN_JOINED") == "true",
        "domain_name": os.getenv("DOMAIN_NAME"),
        "cpu_usage": int(os.getenv("CPU_USAGE", 0)),
        "memory_usage": int(os.getenv("MEMORY_USAGE", 0)),
        "app_port": int(os.getenv("APP_PORT", 8080)),
        "status": "healthy"
    })

@app.route("/ping")
def ping():
    return jsonify({"alive": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)