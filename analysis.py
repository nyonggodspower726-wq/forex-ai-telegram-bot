import requests

API_KEY = "YOUR_TWELVE_DATA_API_KEY"

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
