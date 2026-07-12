import requests

API_KEY = "aba787bf68ba4008b359f34229fdbc29"

def analyze_market(symbol):

    url = (
        f"https://api.twelvedata.com/time_series"
        f"?symbol={symbol}"
        f"&interval=5min"
        f"&outputsize=10"
        f"&apikey={API_KEY}"
    )

    response = requests.get(url)
    data = response.json()

    return str(data)
