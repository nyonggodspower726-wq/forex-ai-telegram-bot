import requests

API_KEY = "YOUR_API_KEY"


def get_candles(symbol, interval):
    url = (
        f"https://api.twelvedata.com/time_series"
        f"?symbol={symbol}"
        f"&interval={interval}"
        f"&outputsize=100"
        f"&apikey={API_KEY}"
    )

    response = requests.get(url)
    data = response.json()

    return data.get("values", [])


def detect_4h_trend(candles):

    if len(candles) < 20:
        return "No Trend"

    highs = [float(c["high"]) for c in candles[:20]]
    lows = [float(c["low"]) for c in candles[:20]]

    last_high = highs[0]
    previous_high = highs[5]

    last_low = lows[0]
    previous_low = lows[5]

    if last_high > previous_high and last_low > previous_low:
        return "Bullish 🟢"

    if last_high < previous_high and last_low < previous_low:
        return "Bearish 🔴"

    return "Range 🟡"


def detect_1h_structure(candles):

    if len(candles) < 20:
        return {
            "trend": "None",
            "structure": "No Structure"
        }

    highs = [float(c["high"]) for c in candles[:20]]
    lows = [float(c["low"]) for c in candles[:20]]

    recent_high = highs[0]
    previous_high = highs[5]

    recent_low = lows[0]
    previous_low = lows[5]

    if recent_high > previous_high and recent_low > previous_low:
        return {
            "trend": "Bullish",
            "structure": "HH → HL 🟢"
        }

    if recent_high < previous_high and recent_low < previous_low:
        return {
            "trend": "Bearish",
            "structure": "LH → LL 🔴"
        }

    return {
        "trend": "Range",
        "structure": "Transition 🟡"
    }


def detect_order_block_zone(candles):

    if len(candles) < 10:
        return None

    for i in range(2, len(candles) - 1):

        current = candles[i - 1]
        previous = candles[i]

        current_open = float(current["open"])
        current_close = float(current["close"])

        previous_open = float(previous["open"])
        previous_close = float(previous["close"])

        previous_high = float(previous["high"])
        previous_low = float(previous["low"])

        # Bullish Order Block
        if (
            previous_close < previous_open
            and current_close > current_open
            and current_close > previous_open
        ):
            return {
                "type": "Bullish",
                "high": previous_high,
                "low": previous_low
            }

        # Bearish Order Block
        if (
            previous_close > previous_open
            and current_close < current_open
            and current_close < previous_open
        ):
            return {
                "type": "Bearish",
                "high": previous_high,
                "low": previous_low
            }

    return None


def wait_for_retracement(order_block, current_price):

    if order_block is None:
        return False

    high = order_block["high"]
    low = order_block["low"]

    if low <= current_price <= high:
        return True

    return False
