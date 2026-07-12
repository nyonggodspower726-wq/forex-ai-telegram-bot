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


def detect_engulfing(candles):
    if len(candles) < 2:
        return "Not enough data"

    current = candles[0]
    previous = candles[1]

    current_open = float(current["open"])
    current_close = float(current["close"])

    previous_open = float(previous["open"])
    previous_close = float(previous["close"])

    if (
        previous_close < previous_open
        and current_close > current_open
        and current_close > previous_open
        and current_open < previous_close
    ):
        return "Bullish Engulfing 🟢"

    if (
        previous_close > previous_open
        and current_close < current_open
        and current_close < previous_open
        and current_open > previous_close
    ):
        return "Bearish Engulfing 🔴"

    return "No Engulfing yet"


def generate_signal(bias, mss, engulfing):

    if (
        "Bullish" in bias
        and "Bullish MSS" in mss
        and "Bullish Engulfing" in engulfing
    ):
        return "BUY 🟢"

    if (
        "Bearish" in bias
        and "Bearish MSS" in mss
        and "Bearish Engulfing" in engulfing
    ):
        return "SELL 🔴"

    return "WAIT ⏳"


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
    engulfing = detect_engulfing(m5)
    signal = generate_signal(bias, mss, engulfing)

    return f"""
📊 PipsPilot AI

Symbol: {symbol}

1H Intraday Bias:
{bias}

5M Entry Analysis:
{mss}

Confirmation:
{engulfing}

Signal:
{signal}

Data connection ✅
"""
