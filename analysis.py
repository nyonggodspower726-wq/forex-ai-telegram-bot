import requests

API_KEY = "aba787bf68ba4008b359f34229fdbc29"

SUPPORTED_SYMBOLS = [
    "XAUUSD",
    "EURUSD",
    "GBPUSD",
    "BTCUSD",
    "ETHUSD"
]


def analyze_market(symbol):
    symbol = symbol.upper()

    if symbol not in SUPPORTED_SYMBOLS:
        return f"""
❌ {symbol} is not supported.

Available:
XAUUSD
EURUSD
GBPUSD
BTCUSD
ETHUSD
"""

    url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={API_KEY}"

    response = requests.get(url)
    data = response.json()

    if "price" not in data:
        return f"❌ Unable to get price for {symbol}\n\n{data}"

    price = data["price"]

    return f"""
📊 PipsPilot AI

Symbol: {symbol}
Live Price: {price}

Status: Market data connected ✅

⚠️ Analysis engine coming next...
"""
