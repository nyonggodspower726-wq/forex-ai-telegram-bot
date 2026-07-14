import asyncio
from datetime import datetime

from telegram import Bot

from strategy_v2 import analyze_market


BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = 6588451803

bot = Bot(token=BOT_TOKEN)


PAIRS = [
    "XAUUSD",
    "EURUSD",
    "GBPUSD"
]


last_signals = {}


async def start_scanner():

    print("Market scanner started...")

    while True:

        for pair in PAIRS:

            try:

                result = analyze_market(pair)

                print(
                    f"\n{datetime.now()}\n"
                    f"{result}"
                )

                if "Signal: BUY" in result or "Signal: SELL" in result:

                    # Prevent duplicate alerts
                    if last_signals.get(pair) != result:

                        await bot.send_message(
                            chat_id=CHAT_ID,
                            text=result
                        )

                        print("🚨 SIGNAL SENT TO TELEGRAM")

                        last_signals[pair] = result

                else:
                    last_signals[pair] = None

            except Exception as e:
                print(f"Scanner Error ({pair}): {e}")

        await asyncio.sleep(300)
