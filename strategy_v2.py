import requests

API_KEY="YOUR_TWELVEDATA_API_KEY"

def get_candles(symbol,interval):
    url=f"https://api.twelvedata.com/time_series?symbol={symbol}&interval={interval}&outputsize=30&apikey={API_KEY}"
    return requests.get(url).json().get("values",[])

def detect_30m_trend(c):
    if len(c)<6:return "Range 🟡"
    h=[float(x["high"]) for x in c[:6]]
    l=[float(x["low"]) for x in c[:6]]
    if h[0]>h[3] and l[0]>l[3]: return "Bullish 🟢"
    if h[0]<h[3] and l[0]<l[3]: return "Bearish 🔴"
    return "Range 🟡"

def engulfing(c):
    if len(c)<2:return None,None
    a,b=c[0],c[1]
    ao,ac=float(a["open"]),float(a["close"])
    bo,bc=float(b["open"]),float(b["close"])
    if bc<bo and ac>ao and ac>bo:return "BUY","Bullish Engulfing"
    if bc>bo and ac<ao and ac<bo:return "SELL","Bearish Engulfing"
    return None,None

def generate_signal(symbol):
    trend=detect_30m_trend(get_candles(symbol,"30min"))
    sig,name=engulfing(get_candles(symbol,"15min"))
    if trend.startswith("Bullish") and sig=="BUY":
        return f"🚨 PipsPilot AI SIGNAL\n\nSymbol: {symbol}\n\n30M Trend: {trend}\n15M Confirmation: {name} ✅\n\nEntry: Market\nStop Loss: Below engulfing candle\nTrade Management: Trail after minor structure break\n\nSignal: BUY ✅"
    if trend.startswith("Bearish") and sig=="SELL":
        return f"🚨 PipsPilot AI SIGNAL\n\nSymbol: {symbol}\n\n30M Trend: {trend}\n15M Confirmation: {name} ✅\n\nEntry: Market\nStop Loss: Above engulfing candle\nTrade Management: Trail after minor structure break\n\nSignal: SELL ✅"
    return f"📊 PipsPilot AI\n\nSymbol: {symbol}\n\n30M Trend: {trend}\n15M Confirmation: Waiting ⏳\n\nSignal: WAIT ⏳"

def analyze_market(symbol):
    try:return generate_signal(symbol)
    except Exception as e:return f"📊 PipsPilot AI\n\nSymbol: {symbol}\nError: {e}"
    
