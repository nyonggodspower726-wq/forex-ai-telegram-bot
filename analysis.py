import requests

API_KEY = "aba787bf68ba4008b359f34229fdbc29"


def analyze_market(symbol):

    symbols = {
        "XAUUSD": "XAU/USD",
        "BTCUSD": "BTC/USD",
        "ETHUSD": "ETH/USD"
    }

    symbol = symbols.get(symbol.upper(), symbol)

    url = (
        f"https://api.twelvedata.com/time_series"
        f"?symbol={symbol}"
        f"&interval=5min"
        f"&outputsize=10"
        f"&apikey={API_KEY}"
    )

    response = requests.get(url)
    data = response.json()

    if "values" not in data:
        return f"❌ Data error:\n{data}"

    candles = data["values"]

    latest = candles[0]

    return f"""
📊 PipsPilot AI

Symbol: {symbol}

Latest Candle:
Open: {latest['open']}
High: {latest['high']}
Low: {latest['low']}
Close: {latest['close']}

Candle data connected ✅
"""
