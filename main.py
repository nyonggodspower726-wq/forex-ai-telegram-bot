import requests

API_KEY = "8858152810:AAGVLGsa9VunTglspZfvW1ivu-sCcghzxEI"


def get_candles(symbol, interval):
    url = (
        f"https://api.twelvedata.com/time_series"
        f"?symbol={symbol}"
        f"&interval={interval}"
        f"&outputsize=100"
        f"&apikey={API_KEY}"
    )

    response = requests.get(url)
    data = response.json()

    return data.get("values", [])


def detect_4h_trend(candles):

    if len(candles) < 10:
        return "No Trend"

    highs=[float(c["high"]) for c in candles[:10]]
    lows=[float(c["low"]) for c in candles[:10]]

    bullish=0
    bearish=0

    for i in range(4):
        if highs[i] > highs[i+1]:
            bullish += 1
        else:
            bearish += 1

        if lows[i] > lows[i+1]:
            bullish += 1
        else:
            bearish += 1

    if bullish >= 6:
        return "Bullish 🟢"

    if bearish >= 6:
        return "Bearish 🔴"

    return "Range 🟡"


def detect_1h_structure(candles):

    if len(candles) < 20:
        return {
            "trend": "None",
            "structure": "No Structure"
        }

    highs = [float(c["high"]) for c in candles[:20]]
    lows = [float(c["low"]) for c in candles[:20]]

    recent_high = highs[0]
    previous_high = highs[5]

    recent_low = lows[0]
    previous_low = lows[5]

    if recent_high > previous_high and recent_low > previous_low:
        return {
            "trend": "Bullish",
            "structure": "HH → HL 🟢"
        }

    if recent_high < previous_high and recent_low < previous_low:
        return {
            "trend": "Bearish",
            "structure": "LH → LL 🔴"
        }

    return {
        "trend": "Range",
        "structure": "Transition 🟡"
    }




def detect_swing_structure(candles):
    if len(candles) < 12:
        return {"trend":"Range","hh":False,"hl":False,"lh":False,"ll":False}

    highs=[float(c["high"]) for c in candles[:12]]
    lows=[float(c["low"]) for c in candles[:12]]

    hh=highs[0]>highs[2]
    hl=lows[0]>lows[2]
    lh=highs[0]<highs[2]
    ll=lows[0]<lows[2]

    if hh and hl:
        return {"trend":"Bullish","hh":True,"hl":True,"lh":False,"ll":False}

    if lh and ll:
        return {"trend":"Bearish","hh":False,"hl":False,"lh":True,"ll":True}

    return {"trend":"Range","hh":False,"hl":False,"lh":False,"ll":False}


def detect_order_block_zone(candles):

    if len(candles) < 10:
        return None

    for i in range(2, len(candles) - 1):

        current = candles[i - 1]
        previous = candles[i]

        current_open = float(current["open"])
        current_close = float(current["close"])

        previous_open = float(previous["open"])
        previous_close = float(previous["close"])

        previous_high = float(previous["high"])
        previous_low = float(previous["low"])

        # Bullish Order Block
        if (
            previous_close < previous_open
            and current_close > current_open
            and current_close > previous_open
        ):
            return {
                "type": "Bullish",
                "high": previous_high,
                "low": previous_low
            }

        # Bearish Order Block
        if (
            previous_close > previous_open
            and current_close < current_open
            and current_close < previous_open
        ):
            return {
                "type": "Bearish",
                "high": previous_high,
                "low": previous_low
            }

    return None


def wait_for_retracement(order_block, current_price):

    if order_block is None:
        return False

    high = order_block["high"]
    low = order_block["low"]

    if low <= current_price <= high:
        return True

    return False


def detect_confirmation(candles):

    if len(candles) < 2:
        return {
            "confirmed": False,
            "signal": "WAIT",
            "type": "None"
        }

    current = candles[0]
    previous = candles[1]

    current_open = float(current["open"])
    current_close = float(current["close"])

    previous_open = float(previous["open"])
    previous_close = float(previous["close"])

    # Bullish Engulfing
    if (
        previous_close < previous_open
        and current_close > current_open
        and current_close > previous_open
    ):
        return {
            "confirmed": True,
            "signal": "BUY",
            "type": "Bullish Engulfing"
        }

    # Bearish Engulfing
    if (
        previous_close > previous_open
        and current_close < current_open
        and current_close < previous_open
    ):
        return {
            "confirmed": True,
            "signal": "SELL",
            "type": "Bearish Engulfing"
        }

    # Bullish Overlap
    if current_close > previous_close:
        return {
            "confirmed": True,
            "signal": "BUY",
            "type": "Bullish Overlap"
        }

    # Bearish Overlap
    if current_close < previous_close:
        return {
            "confirmed": True,
            "signal": "SELL",
            "type": "Bearish Overlap"
        }

    return {
        "confirmed": False,
        "signal": "WAIT",
        "type": "None"
    }


def generate_signal(symbol):
    candles_4h=get_candles(symbol,"4h")
    trend_4h=detect_4h_trend(candles_4h)
    if trend_4h=="No Trend":
        return "WAIT ⏳\nNo 4H trend"
    candles_1h=get_candles(symbol,"1h")
    structure_1h=detect_1h_structure(candles_1h)
    swing=detect_swing_structure(candles_1h)
    order_block=detect_order_block_zone(candles_1h)
    if order_block is None:
        return f"📊 PipsPilot AI\n\nSymbol: {symbol}\n\n4H Trend: {trend_4h}\n1H Structure: {structure_1h['structure']}\n1H Order Block: Not Found\n\nSignal: WAIT ⏳"
    current_price=float(candles_1h[0]["close"])
    if not wait_for_retracement(order_block,current_price):
        return f"📊 PipsPilot AI\n\nSymbol: {symbol}\n\n4H Trend: {trend_4h}\n1H Structure: {structure_1h['structure']}\nOrder Block: {order_block['type']} OB\nPrice: Waiting for retracement ⏳\n\nSignal: WAIT"
    candles_5m=get_candles(symbol,"5min")
    confirmation=detect_confirmation(candles_5m)
    if confirmation["confirmed"]:
        return f"🚨 PipsPilot AI SIGNAL\n\nSymbol: {symbol}\n\n4H Trend: {trend_4h}\n1H Structure: {structure_1h['structure']}\nSwing Trend: {swing['trend']}\nOrder Block: {order_block['type']} OB\nConfirmation: {confirmation['type']}\n\nSignal: {confirmation['signal']} ✅"
    return f"📊 PipsPilot AI\n\nSymbol: {symbol}\n\n4H Trend: {trend_4h}\n1H Structure: {structure_1h['structure']}\nOrder Block: {order_block['type']} OB\n5M Confirmation: Waiting ⏳\n\nSignal: WAIT"

def analyze_market(symbol):
    try:
        return generate_signal(symbol)
    except Exception as e:
        return f"📊 PipsPilot AI\n\nSymbol: {symbol}\nError: {e}"
