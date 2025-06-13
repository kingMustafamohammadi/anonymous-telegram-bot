import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))

user_map = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! پیام، ویس یا عکست رو بفرست تا ناشناس برای مدیر ارسال بشه.")

async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id
    user_map[user_id] = user.first_name or "ناشناس"

    if update.message.text:
        text = update.message.text
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=f"📩 پیام از کاربر ناشناس (ID: {user_id}):\n{text}\n\n/reply {user_id} پاسخ"
        )
        await update.message.reply_text("✅ پیام متنی شما ناشناس ارسال شد.")
    elif update.message.voice or update.message.photo or update.message.document:
        await context.bot.forward_message(chat_id=ADMIN_CHAT_ID, from_chat_id=user_id, message_id=update.message.message_id)
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"(رسانه‌ای از کاربر ناشناس - ID: {user_id})\n/reply {user_id} پاسخ")
        await update.message.reply_text("✅ پیام شما ناشناس ارسال شد.")
    else:
        await update.message.reply_text("❗️این نوع پیام پشتیبانی نمی‌شود.")

async def reply_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_CHAT_ID:
        await update.message.reply_text("⛔️ فقط مدیر می‌تواند پاسخ دهد.")
        return

    args = context.args
    if len(args) < 2:
        await update.message.reply_text("❗️فرمت: /reply user_id پیام شما")
        return

    user_id = int(args[0])
    message_text = " ".join(args[1:])
    try:
        await context.bot.send_message(chat_id=user_id, text=f"📬 پاسخ مدیر:\n{message_text}")
        await update.message.reply_text("✅ پیام ارسال شد.")
    except Exception as e:
        await update.message.reply_text(f"❌ خطا: {e}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reply", reply_command))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_user_message))
    print("🤖 Bot is running...")
    app.run_polling()
