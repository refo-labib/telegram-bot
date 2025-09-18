import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from datetime import datetime

# Ambil token dari Environment Variable (Render → Environment)
TOKEN = os.getenv("7892545779:AAGOW64pmCCGQA1XZW8soZCgcblQWEZcA5U")

# Pastikan ada folder uploads
os.makedirs("uploads", exist_ok=True)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    caption = update.message.caption or update.message.text or ""

    # Kalau user kirim foto
    if update.message.photo:
        file = await context.bot.get_file(update.message.photo[-1].file_id)
        filename = f"uploads/{datetime.now().strftime('%Y%m%d%H%M%S')}_photo.jpg"
        await file.download_to_drive(filename)
        print(f"📸 Foto dari @{user.username}: {caption} -> {filename}")

    # Kalau user kirim video
    elif update.message.video:
        file = await context.bot.get_file(update.message.video.file_id)
        filename = f"uploads/{datetime.now().strftime('%Y%m%d%H%M%S')}_video.mp4"
        await file.download_to_drive(filename)
        print(f"🎥 Video dari @{user.username}: {caption} -> {filename}")

    # Kalau user kirim teks
    elif update.message.text:
        print(f"📝 Teks dari @{user.username}: {caption}")

    # Balas ke user
    await update.message.reply_text("✅ Laporan kamu sudah direkam!")

def main():
    if not TOKEN:
        print("❌ BOT_TOKEN belum diatur di environment variables!")
        return

    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, handle_message))
    print("🤖 Bot berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
