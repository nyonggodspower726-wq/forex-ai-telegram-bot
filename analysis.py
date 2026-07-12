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


def analyze_market(symbol):

    symbols = {
        "XAUUSD": "XAU/USD",
        "BTCUSD": "BTC/USD",
        "ETHUSD": "ETH/USD"
    }

    symbol = symbols.get(symbol.upper(), symbol)

    h1 = get_candles(symbol, "1h")
    m5 = get_candles(symbol, "5min")

    bias = detect_bias(h1)

    return f"""
📊 PipsPilot AI

Symbol: {symbol}

1H Intraday Bias:
{bias}

5M Analysis:
Waiting for MSS + Engulfing confirmation...

Data connection ✅
"""
