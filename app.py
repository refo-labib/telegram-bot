import os
import json
from datetime import datetime
from flask import Flask, request, render_template
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# === Flask App ===
app = Flask(__name__)
DB_FILE = "data.json"

# Baca laporan dari file JSON
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


# === Telegram Bot Setup ===
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
application = Application.builder().token(TOKEN).build()
os.makedirs("uploads", exist_ok=True)

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


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    caption = update.message.caption or update.message.text or ""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    entry = {
        "username": user.username or user.first_name,
        "caption": caption,
        "file": None,
        "timestamp": timestamp
    }

    # Simpan foto
    if update.message.photo:
        file = await context.bot.get_file(update.message.photo[-1].file_id)
        filename = f"uploads/{datetime.now().strftime('%Y%m%d%H%M%S')}_photo.jpg"
        await file.download_to_drive(filename)
        entry["file"] = filename

    # Simpan video
    elif update.message.video:
        file = await context.bot.get_file(update.message.video.file_id)
        filename = f"uploads/{datetime.now().strftime('%Y%m%d%H%M%S')}_video.mp4"
        await file.download_to_drive(filename)
        entry["file"] = filename

    save_report(entry)
    await update.message.reply_text("✅ Laporan kamu sudah direkam!")


# Tambahkan handler
application.add_handler(MessageHandler(filters.ALL, handle_message))


# === Route untuk Webhook ===
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put(update)
    return "OK"


# === Main Run (hanya Flask, Railway pakai gunicorn) ===
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
