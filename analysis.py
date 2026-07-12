import requests

API_KEY = "YOUR_API_KEY_HERE"


def get_candles(symbol, interval):
    url = (
        "https://api.twelvedata.com/time_series"
        f"?symbol={symbol}"
        f"&interval={interval}"
        "&outputsize=50"
        f"&apikey={API_KEY}"
    )

    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        return data.get("values", [])

    except Exception:
        return []


def detect_bias(candles):
    if len(candles) < 10:
        return "Not enough data"

    closes = [float(c["close"]) for c in candles]

    if closes[0] > closes[-1]:
        return "Bullish 🟢"

    return "Bearish 🔴"


def detect_premium_discount(candles):

    highs = [float(c["high"]) for c in candles]
    lows = [float(c["low"]) for c in candles]

    high = max(highs)
    low = min(lows)

    price = float(candles[0]["close"])

    midpoint = (high + low) / 2

    if price > midpoint:
        return "Premium Zone 🔴"

    return "Discount Zone 🟢"


def detect_order_block(candles):

    if len(candles) < 6:
        return "No Order Block yet"

    current = candles[0]
    previous = candles[1]

    current_open = float(current["open"])
    current_close = float(current["close"])

    previous_open = float(previous["open"])
    previous_close = float(previous["close"])

    if previous_close < previous_open and current_close > current_open:
        return "Bullish Order Block 🟢"

    if previous_close > previous_open and current_close < current_open:
        return "Bearish Order Block 🔴"

    return "No Order Block yet"


def detect_mss(candles):

    if len(candles) < 5:
        return "No MSS yet"

    current = float(candles[0]["close"])

    highs = [float(c["high"]) for c in candles[1:5]]
    lows = [float(c["low"]) for c in candles[1:5]]

    if current > max(highs):
        return "Bullish MSS 🟢"

    if current < min(lows):
        return "Bearish MSS 🔴"

    return "No MSS yet"
  def detect_engulfing(candles):

    if len(candles) < 2:
        return "No Engulfing yet"

    current = candles[0]
    previous = candles[1]

    co = float(current["open"])
    cc = float(current["close"])

    po = float(previous["open"])
    pc = float(previous["close"])


    if (
        pc < po
        and cc > co
        and cc > po
        and co < pc
    ):
        return "Bullish Engulfing 🟢"


    if (
        pc > po
        and cc < co
        and cc < po
        and co > pc
    ):
        return "Bearish Engulfing 🔴"


    return "No Engulfing yet"



def detect_displacement(candles):

    if len(candles) < 3:
        return "No Displacement yet"


    current = candles[0]
    previous = candles[1]


    current_open = float(current["open"])
    current_close = float(current["close"])

    previous_range = (
        float(previous["high"])
        -
        float(previous["low"])
    )


    body = abs(current_close - current_open)


    if body > previous_range * 0.7:

        if current_close > current_open:
            return "Bullish Displacement 🟢"

        else:
            return "Bearish Displacement 🔴"


    return "No Displacement yet"



def detect_fvg(candles):

    if len(candles) < 3:
        return "No FVG yet"


    candle1 = candles[2]
    candle3 = candles[0]


    c1_high = float(candle1["high"])
    c1_low = float(candle1["low"])

    c3_high = float(candle3["high"])
    c3_low = float(candle3["low"])


    if c3_low > c1_high:
        return "Bullish FVG 🟢"


    if c3_high < c1_low:
        return "Bearish FVG 🔴"


    return "No FVG yet"



def generate_signal(
    bias,
    zone,
    ob,
    mss,
    engulfing,
    displacement,
    fvg
):

    if (
        "Bullish" in bias
        and "Discount" in zone
        and "Bullish Order Block" in ob
        and "Bullish MSS" in mss
        and (
            "Bullish Engulfing" in engulfing
            or "Bullish Displacement" in displacement
        )
    ):
        return "BUY 🟢"


    if (
        "Bearish" in bias
        and "Premium" in zone
        and "Bearish Order Block" in ob
        and "Bearish MSS" in mss
        and (
            "Bearish Engulfing" in engulfing
            or "Bearish Displacement" in displacement
        )
    ):
        return "SELL 🔴"


    return "WAIT ⏳"
def analyze_market(symbol):

    symbols = {
        "XAUUSD": "XAU/USD",
        "BTCUSD": "BTC/USD",
        "ETHUSD": "ETH/USD",
        "EURUSD": "EUR/USD",
        "GBPUSD": "GBP/USD"
    }


    symbol = symbols.get(symbol.upper(), symbol)


    h1 = get_candles(symbol, "1h")
    m5 = get_candles(symbol, "5min")


    if not h1 or not m5:
        return "❌ Unable to get market data"


    bias = detect_bias(h1)

    zone = detect_premium_discount(h1)

    ob = detect_order_block(m5)

    mss = detect_mss(m5)

    engulfing = detect_engulfing(m5)

    displacement = detect_displacement(m5)

    fvg = detect_fvg(m5)


    signal = generate_signal(
        bias,
        zone,
        ob,
        mss,
        engulfing,
        displacement,
        fvg
    )


    return f"""
📊 PipsPilot AI

Symbol: {symbol}

1H Intraday Bias:
{bias}

1H Zone:
{zone}

5M Order Block:
{ob}

5M MSS:
{mss}

5M Confirmation:
{engulfing}

5M Displacement:
{displacement}

5M Imbalance:
{fvg}

Signal:
{signal}

Data connection ✅
"""
