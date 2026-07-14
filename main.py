from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

import asyncio

from strategy_v2 import analyze_market
from scanner import start_scanner

TOKEN = "YOUR_NEW_BOT_TOKEN"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📊 Welcome to PipsPilot AI\n\n"
        "Analyze any supported market.\n\n"
        "Examples:\n"
        "/analysis XAUUSD\n"
        "/analysis EURUSD\n"
        "/analysis GBPUSD\n\n"
        "Market scanner is active ✅"
    )


async def analysis(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text(
            "Usage:\n"
            "/analysis XAUUSD"
        )
        return

    symbol = context.args[0].upper()

    result = analyze_market(symbol)

    await update.message.reply_text(result)


async def post_init(application: Application):
    asyncio.create_task(start_scanner(application.bot))


def main():

    app = (
        Application.builder()
        .token(TOKEN)
        .post_init(post_init)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("analysis", analysis))

    print("🚀 Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
