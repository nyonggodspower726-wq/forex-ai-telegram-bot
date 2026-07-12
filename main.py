from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from config import BOT_TOKEN
from analysis import analyze_market


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 PipsPilot AI is Online!\n\n"
        "Use:\n"
        "/analysis XAUUSD"
    )


async def analysis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Example:\n/analysis XAUUSD")
        return

    symbol = context.args[0]
    result = analyze_market(symbol)
    await update.message.reply_text(result)


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("analysis", analysis))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
