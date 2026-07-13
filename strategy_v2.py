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
