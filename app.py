import os 
import json
from datetime import datetime
from flask import Flask, render_template, request
from telegram import Bot, Update

# === Flask App ===
app = Flask(__name__)
DB_FILE = "data.json"

@app.route("/")
def index():
    reports = []
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            try:
                reports = json.load(f)
            except:
                reports = []
    return render_template("index.html", reports=reports)

# === Telegram Bot ===
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TOKEN)

def save_report(entry):
    data = []
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            try:
                data = json.load(f)
            except:
                data = []
    data.append(entry)
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    message = update.message

    if message:
        user = message.from_user
        caption = message.caption or message.text or ""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        entry = {
            "username": user.username or user.first_name,
            "caption": caption,
            "file": None,
            "timestamp": timestamp
        }

        # Foto
        if message.photo:
            file = bot.get_file(message.photo[-1].file_id)
            entry["file"] = file.file_path

        # Video
        elif message.video:
            file = bot.get_file(message.video.file_id)
            entry["file"] = file.file_path

        save_report(entry)
        bot.send_message(chat_id=message.chat_id, text="✅ Laporan kamu sudah direkam!")

    return "ok"

# === Main Run ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
