import requests

API_KEY = "PASTE_YOUR_TWELVE_DATA_API_KEY"

def analyze_market(symbol):
    url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={API_KEY}"

    response = requests.get(url)
    data = response.json()

    if "price" not in data:
        return f"❌ Unable to get price for {symbol}"

    price = float(data["price"])

    return f"""
📊 PipsPilot AI

Symbol: {symbol}
Live Price: {price}

Trend: Waiting for AI Analysis...

⚠️ Live data connected successfully.
"""
