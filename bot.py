import os
import csv
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CSV_FILE = "rekap.csv"

# Inisialisasi bot application
application = Application.builder().token(TOKEN).build()


# Command /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Kirimkan teks atau gambar untuk direkap.")


# Handler untuk pesan teks
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text

    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([user.username, text])

    await update.message.reply_text("Pesanmu sudah direkap ✅")


# Handler untuk gambar/photo
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    photo = update.message.photo[-1].file_id  # ambil resolusi terbesar

    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([user.username, f"Photo ID: {photo}"])

    await update.message.reply_text("Gambar kamu sudah direkap 🖼️✅")


# Register handler
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
