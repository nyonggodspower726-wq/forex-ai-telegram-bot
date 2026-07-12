import requests

API_KEY = "aba787bf68ba4008b359f34229fdbc29"


def get_candles(symbol, interval):
    url = (
        f"https://api.twelvedata.com/time_series"
        f"?symbol={symbol}"
        f"&interval={interval}"
        f"&outputsize=50"
        f"&apikey={API_KEY}"
    )

    response = requests.get(url)
    data = response.json()

    return data.get("values", [])


def detect_bias(candles):
    if len(candles) < 10:
        return "Not enough data"

    closes = [float(c["close"]) for c in candles]

    if closes[0] > closes[-1]:
        return "Bullish 🟢"
    else:
        return "Bearish 🔴"


def detect_mss(candles):
    if len(candles) < 5:
        return "Not enough data"

    recent = candles[:5]

    highs = [float(c["high"]) for c in recent]
    lows = [float(c["low"]) for c in recent]

    current_close = float(recent[0]["close"])

    previous_high = max(highs[1:])
    previous_low = min(lows[1:])

    if current_close > previous_high:
        return "Bullish MSS 🟢"

    if current_close < previous_low:
        return "Bearish MSS 🔴"

    return "No MSS yet"


def analyze_market(symbol):

    symbols = {
        "XAUUSD": "XAU/USD",
        "BTCUSD": "BTC/USD",
        "ETHUSD": "ETH/USD"
    }

    symbol = symbols.get(symbol.upper(), symbol)

    h1 = get_candles(symbol, "1h")
    m5 = get_candles(symbol, "5min")

    if not h1 or not m5:
        return "❌ Unable to get market data"

    bias = detect_bias(h1)
    mss = detect_mss(m5)

    return f"""
📊 PipsPilot AI

Symbol: {symbol}

1H Intraday Bias:
{bias}

5M Entry Analysis:
{mss}

Data connection ✅
"""
