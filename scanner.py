import asyncio
from datetime import datetime

from strategy_v2 import analyze_market


PAIRS = [
    "XAUUSD",
    "EURUSD",
    "GBPUSD"
]


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
                    print("🚨 SIGNAL FOUND")

            except Exception as e:
                print(f"Scanner Error ({pair}): {e}")

        await asyncio.sleep(300)
