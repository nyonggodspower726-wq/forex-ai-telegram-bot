def analyze_market(symbol):
    symbol = symbol.upper()

    if symbol == "XAUUSD":
        return f"""
📊 PipsPilot AI

Symbol: {symbol}

Trend: Bullish 🟢

Entry: 3348.20
Stop Loss: 3342.00
Take Profit: 3362.50

Risk Reward: 1:3

Confidence: 87%

⚠ Demo Analysis Only
"""

    return f"❌ {symbol} is not supported yet."
