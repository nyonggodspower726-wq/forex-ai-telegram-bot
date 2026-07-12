from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

import asyncio

from strategy import analyze_market
from scanner import start_scanner

TOKEN = "


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to Godspower Trading Bot 📊\n\n"
        "Your EUR/USD analysis assistant is online.\n"
        "The market scanner is active.\n"
        "Use /analysis to check the market."
    )


async def analysis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = analyze_market()
    await update.message.reply_text(result)


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("analysis", analysis))

    print("Bot is running...")

    # Start background scanner
    asyncio.get_event_loop().create_task(start_scanner())

    app.run_polling()


if __name__ == "__main__":
    main()
