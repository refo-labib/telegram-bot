import os
import json
from flask import Flask, render_template, request
from bot import application

app = Flask(__name__)
DB_FILE = "data.json"

# === ROUTE UNTUK WEBHOOK TELEGRAM ===
@app.route(f"/{os.getenv('TELEGRAM_BOT_TOKEN')}", methods=["POST"])
def webhook():
    if request.method == "POST":
        update = request.get_json(force=True)
        application.update_queue.put_nowait(update)
        return "OK", 200
    return "Method Not Allowed", 405


# === ROUTE UNTUK TAMPILAN REKAP ===
@app.route("/", methods=["GET"])
def index():
    reports = []
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            try:
                reports = json.load(f)
            except:
                reports = []
    return render_template("index.html", reports=reversed(reports))


# === ROUTE UNTUK STATIC FILE (foto/video) ===
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return app.send_static_file(os.path.join("uploads", filename))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
