def generate_signal(symbol):

    # 4H Trend
    candles_4h = get_candles(symbol, "4h")
    trend_4h = detect_4h_trend(candles_4h)

    if trend_4h == "No Trend":
        return "WAIT ⏳\nNo 4H trend"


    # 1H Structure
    candles_1h = get_candles(symbol, "1h")
    structure_1h = detect_1h_structure(candles_1h)


    # 1H Order Block
    order_block = detect_order_block_zone(candles_1h)

    if order_block is None:
        return (
            f"📊 PipsPilot AI\n\n"
            f"Symbol: {symbol}\n\n"
            f"4H Trend: {trend_4h}\n"
            f"1H Structure: {structure_1h['structure']}\n"
            "1H Order Block: Not Found\n\n"
            "Signal: WAIT ⏳"
        )


    # Current price
    current_price = float(candles_1h[0]["close"])


    # Retracement into Order Block
    retracement = wait_for_retracement(
        order_block,
        current_price
    )


    if not retracement:
        return (
            f"📊 PipsPilot AI\n\n"
            f"Symbol: {symbol}\n\n"
            f"4H Trend: {trend_4h}\n"
            f"1H Structure: {structure_1h['structure']}\n"
            f"Order Block: {order_block['type']} OB\n"
            "Price: Waiting for retracement ⏳\n\n"
            "Signal: WAIT"
        )


    # 5M Confirmation
    candles_5m = get_candles(symbol, "5min")
    confirmation = detect_confirmation(candles_5m)


    if confirmation["confirmed"]:

        return (
            f"🚨 PipsPilot AI SIGNAL\n\n"
            f"Symbol: {symbol}\n\n"
            f"4H Trend: {trend_4h}\n"
            f"1H Structure: {structure_1h['structure']}\n"
            f"Order Block: {order_block['type']} OB\n"
            f"Confirmation: {confirmation['type']}\n\n"
            f"Signal: {confirmation['signal']} ✅"
        )


    return (
        f"📊 PipsPilot AI\n\n"
        f"Symbol: {symbol}\n\n"
        f"4H Trend: {trend_4h}\n"
        f"1H Structure: {structure_1h['structure']}\n"
        f"Order Block: {order_block['type']} OB\n"
        "5M Confirmation: Waiting ⏳\n\n"
        "Signal: WAIT"
    )


def analyze_market(symbol):

    try:
        return generate_signal(symbol)

    except Exception as e:
        return (
            f"📊 PipsPilot AI\n\n"
            f"Symbol: {symbol}\n"
            f"Error: {str(e)}"
        )
