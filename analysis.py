import requests

API_KEY = "aba787bf68ba4008b359f34229fdbc29"

def analyze_market(symbol):
    symbols = {
        "BTCUSD": "BTC/USD",
        "ETHUSD": "ETH/USD",
        "XAUUSD": "XAU/USD",
    }

    symbol = symbol.upper()

    if symbol in symbols:
        symbol = symbols[symbol]

    url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={API_KEY}"

    response = requests.get(url)
    data = response.json()

    return str(data)
