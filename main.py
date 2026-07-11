from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config import BOT_TOKEN


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 Welcome to PipsPilot AI!\n\n"
        "Your AI Forex Trading Assistant is now online.\n\n"
        "Commands:\n"
        "/start - Start the bot\n"
        "/analysis - Analyze the market (coming soon)"
    )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("PipsPilot AI is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
