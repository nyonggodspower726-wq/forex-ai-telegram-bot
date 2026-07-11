from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

from config import BOT_TOKEN
from analysis import analyze_market


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 Welcome to PipsPilot AI!\n\n"
        "Use:\n"
        "/analysis XAUUSD\n"
        "/analysis EURUSD"
    )


async def analysis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text(
            "Usage:\n/analysis XAUUSD"
        )
        return

    symbol = context.args[0]

    result = analyze_market(symbol)

    message = (
        f"📊 {result['symbol']} Analysis\n\n"
        f"Trend: {result['trend']}\n"
        f"Signal: {result['signal']}\n"
        f"Entry: {result['entry']}\n"
        f"Stop Loss: {result['stop_loss']}\n"
        f"Take Profit: {result['take_profit']}\n"
        f"Confidence: {result['confidence']}"
    )

    await update.message.reply_text(message)


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("analysis", analysis))

    print("PipsPilot AI is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
