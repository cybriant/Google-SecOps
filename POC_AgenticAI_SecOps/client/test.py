def generate_comprehensive_stock_analysis(macd, rsi, moving_avg, last_price, volume, pivot_levels):
    """
    Generates a comprehensive stock analysis with detailed handling of different conditions and edge cases.
    
    :param macd: A dictionary containing MACD values.
    :param rsi: The RSI value.
    :param moving_avg: A dictionary containing the last price and SMA values.
    :param last_price: The last closing price of the stock.
    :param volume: Current trading volume of the stock.
    :param pivot_levels: Dictionary with pivot and support/resistance levels.
    :return: A string summary of stock analysis with enhanced insights.
    """
    # MACD Analysis
    if macd["valueMACD"] > macd["valueMACDSignal"]:
        macd_trend = "bullish"
    elif macd["valueMACD"] < macd["valueMACDSignal"]:
        macd_trend = "bearish"
    else:
        macd_trend = "neutral"

    if macd["valueMACDHist"] > 0:
        macd_histogram = "positive"
    elif macd["valueMACDHist"] < 0:
        macd_histogram = "negative"
    else:
        macd_histogram = "neutral"

    macd_analysis = f"MACD: The MACD is {macd_trend}, and the histogram is {macd_histogram}. This indicates a potential {macd_trend} trend."

    # RSI Analysis
    if rsi > 70:
        rsi_signal = "overbought"
    elif rsi < 30:
        rsi_signal = "oversold"
    else:
        rsi_signal = "neutral"

    rsi_analysis = f"RSI: The RSI is at {rsi}, indicating the market is {rsi_signal}. It's a good time to watch for potential reversal."

    # Moving Averages Analysis
    sma5 = moving_avg["sma5"]
    sma20 = moving_avg["sma20"]
    sma200 = moving_avg["sma200"]
    price = moving_avg["lastPrice"]

    if price > sma5:
        sma5_condition = "above"
    elif price < sma5:
        sma5_condition = "below"
    else:
        sma5_condition = "equal"

    if price > sma20:
        sma20_condition = "above"
    elif price < sma20:
        sma20_condition = "below"
    else:
        sma20_condition = "equal"

    if price > sma200:
        sma200_condition = "above"
    elif price < sma200:
        sma200_condition = "below"
    else:
        sma200_condition = "equal"

    moving_avg_analysis = (
        f"Moving Averages: The last price ({price}) is {sma5_condition} the SMA_5 ({sma5}), "
        f"{sma20_condition} the SMA_20 ({sma20}), and {sma200_condition} the SMA_200 ({sma200}). "
        "This suggests the stock may be in a short-term bullish trend, but could face resistance in the medium term."
    )

    # Volume Analysis
    if volume > pivot_levels['average_volume']:
        volume_condition = "strong buying pressure"
    elif volume < pivot_levels['average_volume']:
        volume_condition = "weak buying pressure"
    else:
        volume_condition = "neutral volume"

    volume_analysis = f"Volume: The trading volume indicates {volume_condition}. The price movement may not sustain unless volume continues to rise."

    # Pivot Levels Analysis
    pivot_point = pivot_levels['pivot']
    r1 = pivot_levels['R1']
    r2 = pivot_levels['R2']
    r3 = pivot_levels['R3']
    s1 = pivot_levels['S1']
    s2 = pivot_levels['S2']

    # Determine price vs. pivot and resistance/support
    if last_price > pivot_point:
        pivot_condition = "above the pivot point"
    elif last_price < pivot_point:
        pivot_condition = "below the pivot point"
    else:
        pivot_condition = "equal to the pivot point"

    if last_price > r1:
        r1_condition = "above R1"
    elif last_price < r1:
        r1_condition = "below R1"
    else:
        r1_condition = "equal to R1"

    if last_price > r2:
        r2_condition = "above R2"
    elif last_price < r2:
        r2_condition = "below R2"
    else:
        r2_condition = "equal to R2"

    if last_price > r3:
        r3_condition = "above R3"
    elif last_price < r3:
        r3_condition = "below R3"
    else:
        r3_condition = "equal to R3"

    pivot_analysis = (
        f"Pivot Levels: The current price is {last_price}, which is {pivot_condition} ({pivot_point}). "
        f"It is {r1_condition} ({r1}), {r2_condition} ({r2}), and {r3_condition} ({r3}). "
        f"Support levels are at S1 ({s1}) and S2 ({s2})."
    )

    # Future Projections
    future_projection = (
        f"Future Projections: If the price breaks above R2 ({r2}) with strong volume, it could potentially reach R3 ({r3}). "
        f"Failure to hold above R1 ({r1}) might lead to a pullback toward the pivot point ({pivot_point}) or even lower support levels. "
        "Keep an eye on the price action near these critical levels for confirmation of the next move."
    )

    # Recommended Action
    action = (
        f"Recommended Action:\n"
        f"If you currently hold positions: Maintain your position but monitor the price action closely near the R2 ({r2}) resistance. "
        f"Consider partial profit-taking if the price struggles to break above this level.\n"
        f"If you do not own the stock: Wait for a breakout above R2 ({r2}) with strong volume confirmation before entering. "
        f"Alternatively, consider buying near the pivot point ({pivot_point}) if the price pulls back and stabilizes. "
        f"Set a stop-loss below S1 ({s1}) to manage downside risk."
    )

    # Return full analysis
    full_analysis = (
        f"{macd_analysis}\n\n"
        f"{rsi_analysis}\n\n"
        f"{moving_avg_analysis}\n\n"
        f"{volume_analysis}\n\n"
        f"{pivot_analysis}\n\n"
        f"{future_projection}\n\n"
        f"{action}"
    )

    return full_analysis


def test_bullish_case():
    macd_data = {"valueMACD": 20, "valueMACDSignal": 15, "valueMACDHist": 3.0}
    rsi_value = 55
    moving_avg_data = {"lastPrice": 600, "sma5": 590, "sma20": 580, "sma200": 570}
    last_price = 600
    volume = 1500000
    pivot_levels = {
        'pivot': 550, 'R1': 570, 'R2': 580, 'R3': 600,
        'S1': 530, 'S2': 520, 'average_volume': 1000000
    }
    print(generate_comprehensive_stock_analysis(macd_data, rsi_value, moving_avg_data, last_price, volume, pivot_levels))

def test_bearish_case_low_rsi():
    macd_data = {"valueMACD": -18, "valueMACDSignal": -10, "valueMACDHist": -2.0}
    rsi_value = 25
    moving_avg_data = {"lastPrice": 450, "sma5": 460, "sma20": 470, "sma200": 480}
    last_price = 450
    volume = 900000
    pivot_levels = {
        'pivot': 460, 'R1': 470, 'R2': 480, 'R3': 500,
        'S1': 440, 'S2': 420, 'average_volume': 1000000
    }
    print(generate_comprehensive_stock_analysis(macd_data, rsi_value, moving_avg_data, last_price, volume, pivot_levels))

def test_neutral_market_conditions():
    macd_data = {"valueMACD": -0.5, "valueMACDSignal": -0.6, "valueMACDHist": 0.1}
    rsi_value = 50
    moving_avg_data = {"lastPrice": 550, "sma5": 555, "sma20": 560, "sma200": 570}
    last_price = 550
    volume = 1000000
    pivot_levels = {
        'pivot': 555, 'R1': 565, 'R2': 575, 'R3': 590,
        'S1': 545, 'S2': 535, 'average_volume': 1000000
    }
    print(generate_comprehensive_stock_analysis(macd_data, rsi_value, moving_avg_data, last_price, volume, pivot_levels))

def test_bullish_with_high_rsi():
    macd_data = {"valueMACD": 25, "valueMACDSignal": 18, "valueMACDHist": 4.0}
    rsi_value = 70
    moving_avg_data = {"lastPrice": 700, "sma5": 690, "sma20": 680, "sma200": 660}
    last_price = 700
    volume = 2000000
    pivot_levels = {
        'pivot': 680, 'R1': 700, 'R2': 720, 'R3': 740,
        'S1': 660, 'S2': 640, 'average_volume': 1500000
    }
    print(generate_comprehensive_stock_analysis(macd_data, rsi_value, moving_avg_data, last_price, volume, pivot_levels))

def test_bearish_case_with_price_below_moving_averages():
    macd_data = {"valueMACD": -10, "valueMACDSignal": -5, "valueMACDHist": -1.0}
    rsi_value = 35
    moving_avg_data = {"lastPrice": 450, "sma5": 460, "sma20": 470, "sma200": 480}
    last_price = 450
    volume = 800000
    pivot_levels = {
        'pivot': 460, 'R1': 470, 'R2': 480, 'R3': 500,
        'S1': 440, 'S2': 420, 'average_volume': 1000000
    }
    print(generate_comprehensive_stock_analysis(macd_data, rsi_value, moving_avg_data, last_price, volume, pivot_levels))

def test_edge_case_no_data():
    macd_data = {"valueMACD": 0, "valueMACDSignal": 0, "valueMACDHist": 0}
    rsi_value = 50
    moving_avg_data = {"lastPrice": 500, "sma5": 500, "sma20": 500, "sma200": 500}
    last_price = 500
    volume = 0
    pivot_levels = {
        'pivot': 500, 'R1': 510, 'R2': 520, 'R3': 530,
        'S1': 490, 'S2': 480, 'average_volume': 0
    }
    print(generate_comprehensive_stock_analysis(macd_data, rsi_value, moving_avg_data, last_price, volume, pivot_levels))

def test_edge_case_high_volume():
    macd_data = {"valueMACD": 10, "valueMACDSignal": 8, "valueMACDHist": 1.5}
    rsi_value = 60
    moving_avg_data = {"lastPrice": 550, "sma5": 540, "sma20": 530, "sma200": 510}
    last_price = 550
    volume = 5000000  # Extremely high volume
    pivot_levels = {
        'pivot': 540, 'R1': 550, 'R2': 560, 'R3': 580,
        'S1': 530, 'S2': 510, 'average_volume': 1000000
    }
    print(generate_comprehensive_stock_analysis(macd_data, rsi_value, moving_avg_data, last_price, volume, pivot_levels))

def test_edge_case_low_price():
    macd_data = {"valueMACD": -5, "valueMACDSignal": -4, "valueMACDHist": -0.8}
    rsi_value = 40
    moving_avg_data = {"lastPrice": 100, "sma5": 105, "sma20": 110, "sma200": 120}
    last_price = 100
    volume = 300000
    pivot_levels = {
        'pivot': 110, 'R1': 120, 'R2': 130, 'R3': 140,
        'S1': 95, 'S2': 90, 'average_volume': 1000000
    }
    print(generate_comprehensive_stock_analysis(macd_data, rsi_value, moving_avg_data, last_price, volume, pivot_levels))

def test_edge_case_high_rsi_overbought():
    macd_data = {"valueMACD": 10, "valueMACDSignal": 5, "valueMACDHist": 1.0}
    rsi_value = 85  # Overbought condition
    moving_avg_data = {"lastPrice": 700, "sma5": 690, "sma20": 680, "sma200": 660}
    last_price = 700
    volume = 1500000
    pivot_levels = {
        'pivot': 680, 'R1': 700, 'R2': 720, 'R3': 740,
        'S1': 660, 'S2': 640, 'average_volume': 1000000
    }
    print(generate_comprehensive_stock_analysis(macd_data, rsi_value, moving_avg_data, last_price, volume, pivot_levels))

# Run all tests
test_bullish_case()
# test_bearish_case_low_rsi()
# test_neutral_market_conditions()
# test_bullish_with_high_rsi()
# test_bearish_case_with_price_below_moving_averages()
# test_edge_case_no_data()
# test_edge_case_high_volume()
# test_edge_case_low_price()
# test_edge_case_high_rsi_overbought()
