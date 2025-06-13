from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler

# آیدی عددی شما (ادمین)
ADMIN_ID = 455102383  # ← آی‌دی عددی خودت رو اینجا بذار

# دیکشنری برای نگه‌داشتن ارتباط بین پیام‌ها و کاربرا
user_message_map = {}

# هندل پیام کاربران
async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.effective_message
    text = message.text or "(متن ندارد)"
    
    # ذخیره آی‌دی کاربر و پیام
    user_message_map[message.message_id] = user.id

    # فوروارد به ادمین با آیدی و نام
    forward_text = f"📩 پیام جدید از @{user.username or 'بی‌نام'} (ID: {user.id}):\n\n{text}"
    await context.bot.send_message(chat_id=ADMIN_ID, text=forward_text)

# هندل پاسخ ادمین به کاربران
async def handle_admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    reply = message.reply_to_message

    # چک کنیم پیام پاسخ به کدوم کاربره
    if reply and "ID:" in reply.text:
        try:
            user_id_line = [line for line in reply.text.split('\n') if "ID:" in line][0]
            user_id = int(user_id_line.split("ID:")[1].strip().replace(")", "").replace(":", ""))
            await context.bot.send_message(chat_id=user_id, text=message.text)
            await context.bot.send_message(chat_id=ADMIN_ID, text="✅ پیام برای کاربر ارسال شد.")
        except Exception as e:
            await context.bot.send_message(chat_id=ADMIN_ID, text=f"❌ خطا در ارسال پیام: {e}")

# راه‌اندازی ربات
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! پیام‌تو بفرست، ادمین جواب می‌ده 🙂")

def main():
    app = ApplicationBuilder().token("7921760794:AAGcot2bVBiiM012GMk6exNFZ7lTiOO_44E").build()

    app.add_handler(CommandHandler("start", start))
    
    # پیام‌های دریافتی از همه کاربران
    app.add_handler(MessageHandler(filters.TEXT & ~filters.User(user_id=ADMIN_ID), handle_user_message))
    
    # پیام‌های ادمین که به کاربر reply زده
    app.add_handler(MessageHandler(filters.TEXT & filters.User(user_id=ADMIN_ID), handle_admin_reply))

    print("ربات فعال شد.")
    app.run_polling()

if __name__ == "__main__":
    main()