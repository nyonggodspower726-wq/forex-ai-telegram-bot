from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from analysis import analyze_market

TOKEN = "8858152810:AAHvXkD78ybAMb9Tmf9_6bYrhcUnqEPt2zw"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to PipsPilot AI 📈\n\n"
        "Use /analysis XAUUSD"
    )


async def analysis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Example:\n/analysis XAUUSD")
        return

    symbol = context.args[0]
    result = analyze_market(symbol)
    await update.message.reply_text(str(result))


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("analysis", analysis))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
