import asyncio
from datetime import datetime

from strategy_v2 import analyze_market


PAIRS = [
    "XAUUSD",
    "EURUSD",
    "GBPUSD"
]


CHAT_ID = 6588451803

last_signals = {}


async def start_scanner(bot):

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

                    if last_signals.get(pair) != result:

                        await bot.send_message(
                            chat_id=CHAT_ID,
                            text=result
                        )

                        print(f"🚨 Signal sent for {pair}")

                        last_signals[pair] = result

                else:
                    last_signals[pair] = None

            except Exception as e:
                print(f"Scanner Error ({pair}): {e}")

        await asyncio.sleep(300)
