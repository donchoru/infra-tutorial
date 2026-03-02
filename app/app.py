import os
import platform
import socket
import time
from datetime import datetime

from flask import Flask, jsonify, render_template

app = Flask(__name__)

START_TIME = time.time()


def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


@app.route("/")
def index():
    uptime_sec = int(time.time() - START_TIME)
    hours, remainder = divmod(uptime_sec, 3600)
    minutes, seconds = divmod(remainder, 60)

    context = {
        "hostname": socket.gethostname(),
        "ip": get_ip(),
        "deploy_env": os.environ.get("DEPLOY_ENV", "local"),
        "uptime": f"{hours}h {minutes}m {seconds}s",
        "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    return render_template("index.html", **context)


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/info")
def info():
    return jsonify({
        "hostname": socket.gethostname(),
        "ip": get_ip(),
        "deploy_env": os.environ.get("DEPLOY_ENV", "local"),
        "python_version": platform.python_version(),
        "os": f"{platform.system()} {platform.release()}",
        "arch": platform.machine(),
        "uptime_seconds": int(time.time() - START_TIME),
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
