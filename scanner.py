from analysis import analyze_market

PAIRS = [
    "XAUUSD",
    "EURUSD",
    "GBPUSD"
]


async def scanner_job(context):

    bot = context.bot

    chat_id = context.job.chat_id

    for pair in PAIRS:

        try:

            result = analyze_market(pair)

            if "BUY 🟢" in result or "SELL 🔴" in result:

                await bot.send_message(
                    chat_id=chat_id,
                    text="🚨 PipsPilot AI Signal\n\n" + result
                )

        except Exception as e:

            print(f"Scanner Error: {e}")
