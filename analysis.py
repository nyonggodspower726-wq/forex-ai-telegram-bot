import requests

API_KEY = "YOUR_TWELVE_DATA_API_KEY"

def analyze_market(symbol):
    url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={API_KEY}"

    response = requests.get(url)
    data = response.json()

    return str(data)
