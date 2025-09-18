from flask import Flask, request
from bot import application
import os

app = Flask(__name__)

# route utama untuk webhook Telegram
@app.route(f"/{os.getenv('TELEGRAM_BOT_TOKEN')}", methods=["POST"])
def webhook():
    if request.method == "POST":
        update = request.get_json(force=True)
        application.update_queue.put_nowait(update)
        return "OK", 200
    else:
        return "Method Not Allowed", 405


@app.route("/", methods=["GET"])
def home():
    return "Telegram Bot is running!", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
