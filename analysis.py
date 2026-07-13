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
        return "No Trend"

    highs = [float(c["high"]) for c in candles[:10]]
    lows = [float(c["low"]) for c in candles[:10]]

    recent_high = highs[0]
    previous_high = max(highs[1:5])
    recent_low = lows[0]
    previous_low = min(lows[1:5])

    if recent_high > previous_high and recent_low > previous_low:
        return "Bullish 🟢"

    if recent_high < previous_high and recent_low < previous_low:
        return "Bearish 🔴"

    return "Range / Transition 🟡"


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
        return "Not enough data"

    for i in range(1, 5):

        current = candles[i-1]
        previous = candles[i]

        current_open = float(current["open"])
        current_close = float(current["close"])

        previous_open = float(previous["open"])
        previous_close = float(previous["close"])


        if (
            previous_close < previous_open
            and current_close > current_open
            and current_close > previous_open
        ):
            return "Bullish Order Block 🟢"


        if (
            previous_close > previous_open
            and current_close < current_open
            and current_close < previous_open
        ):
            return "Bearish Order Block 🔴"


    return "No Order Block yet"


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
        return "Not enough data"


    current = candles[0]
    previous = candles[1]


    current_open = float(current["open"])
    current_close = float(current["close"])

    previous_high = float(previous["high"])
    previous_low = float(previous["low"])


    body = abs(current_close - current_open)

    previous_range = abs(previous_high - previous_low)


    if (
        current_close > current_open
        and body > previous_range * 0.7
    ):
        return "Bullish Displacement 🟢"


    if (
        current_close < current_open
        and body > previous_range * 0.7
    ):
        return "Bearish Displacement 🔴"


    return "No Displacement yet"


def detect_fvg(candles):

    if len(candles) < 3:
        return "Not enough data"


    candle1 = candles[2]
    candle3 = candles[0]


    candle1_high = float(candle1["high"])
    candle1_low = float(candle1["low"])

    candle3_high = float(candle3["high"])
    candle3_low = float(candle3["low"])


    if candle3_low > candle1_high:
        return "Bullish FVG 🟢"


    if candle3_high < candle1_low:
        return "Bearish FVG 🔴"


    return "No FVG yet"


def generate_signal(bias, zone, ob, engulfing):


    if (
        "Bullish" in bias
        and "Discount" in zone
        and "Bullish Order Block" in ob
        and "Bullish Engulfing" in engulfing
    ):
        return "BUY 🟢"


    if (
        "Bearish" in bias
        and "Premium" in zone
        and "Bearish Order Block" in ob
        and "Bearish Engulfing" in engulfing
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


    h4 = get_candles(symbol, "4h")
    h1 = get_candles(symbol, "1h")
    m5 = get_candles(symbol, "5min")


    if not h4 or not h1 or not m5:
        return "❌ Unable to get market data"


    bias = detect_bias(h4)

    zone = detect_premium_discount(h1)

    ob = detect_order_block(h1)

    engulfing = detect_engulfing(m5)


    signal = generate_signal(
        bias,
        zone,
        ob,
        engulfing
    )


    return f"""
📊 PipsPilot AI

Symbol: {symbol}

4H Trend:
{bias}

1H Zone:
{zone}

1H Order Block:
{ob}

5M Confirmation:
{engulfing}

Signal:
{signal}

Data connection ✅
"""
