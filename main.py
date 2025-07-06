from flask import Flask, render_template

from datetime import datetime

from sklearn.preprocessing import StandardScaler
import tensorflow as tf
import numpy as np

from tradingview_ta import TA_Handler, Interval, Exchange
import tradingview_ta

app = Flask(__name__)

@app.route("/")
def home():
    # Get time
    now = datetime.now()
    time = now.strftime("%H:%M")

    # Load the model
    model = tf.keras.models.load_model('models/v1-2.h5')

    # Set up tradingview_ta TA_Handler
    handler_btc = TA_Handler(
        symbol="BTCUSDT",
        exchange="BINANCE",
        screener="CRYPTO",
        interval="1h",
        timeout=None
    )

    handler_btc_input = handler_btc.get_analysis()
    price_btc = handler_btc_input.indicators["close"]
    rsi_btc = handler_btc_input.indicators["RSI"]
    lowerbb_btc = handler_btc_input.indicators["BB.lower"]
    upperbb_btc = handler_btc_input.indicators["BB.upper"]

    inputs_btc = [[price_btc, rsi_btc, upperbb_btc, lowerbb_btc]]
    
    # Normalize input
    scaler_btc = StandardScaler()
    inputs_btc = scaler_btc.fit_transform(inputs_btc)
    
    # Make predictions using the model
    predictions_btc = model.predict(inputs_btc)
    
    # Make the output readable
    predictions_readable_btc = np.where(predictions_btc > 0.5, 1, 0)

    if predictions_readable_btc == 1:
        predictions_readable_btc = "Buy"
    elif predictions_readable_btc == 0:
        predictions_readable_btc = "Sell"
    
    # Set up tradingview_ta TA_Handler
    handler_eth = TA_Handler(
        symbol="ETHUSDT",
        exchange="BINANCE",
        screener="CRYPTO",
        interval="1h",
        timeout=None
    )

    handler_eth_input = handler_eth.get_analysis()
    price_eth = handler_eth_input.indicators["close"]
    rsi_eth = handler_eth_input.indicators["RSI"]
    lowerbb_eth = handler_eth_input.indicators["BB.lower"]
    upperbb_eth = handler_eth_input.indicators["BB.upper"]

    inputs_eth = [[price_eth, rsi_eth, upperbb_eth, lowerbb_eth]]
    
    # Normalize input
    scaler_eth = StandardScaler()
    inputs_eth = scaler_eth.fit_transform(inputs_eth)
    
    # Make predictions using the model
    predictions_eth = model.predict(inputs_eth)
    
    # Make the output readable
    predictions_readable_eth = np.where(predictions_eth > 0.5, 1, 0)

    if predictions_readable_eth == 1:
        predictions_readable_eth = "Buy"
    elif predictions_readable_eth == 0:
        predictions_readable_eth = "Sell"
    
    # Set up tradingview_ta TA_Handler
    handler_sol = TA_Handler(
        symbol="SOLUSDT",
        exchange="BINANCE",
        screener="CRYPTO",
        interval="1h",
        timeout=None
    )

    handler_sol_input = handler_sol.get_analysis()
    price_sol = handler_sol_input.indicators["close"]
    rsi_sol = handler_sol_input.indicators["RSI"]
    lowerbb_sol = handler_sol_input.indicators["BB.lower"]
    upperbb_sol = handler_sol_input.indicators["BB.upper"]

    inputs_sol = [[price_sol, rsi_sol, upperbb_sol, lowerbb_sol]]
    
    # Normalize input
    scaler_sol = StandardScaler()
    inputs_sol = scaler_sol.fit_transform(inputs_sol)
    
    # Make predictions using the model
    predictions_sol = model.predict(inputs_sol)
    
    # Make the output readable
    predictions_readable_sol = np.where(predictions_sol > 0.5, 1, 0)

    if predictions_readable_sol == 1:
        predictions_readable_sol = "Buy"
    elif predictions_readable_sol == 0:
        predictions_readable_sol = "Sell"

    return render_template("home.html", time=time,
                           btc_price=round(price_btc, 1), btc_rsi=round(rsi_btc, 1), btc_lowerbb=round(lowerbb_btc, 1), btc_upperbb=round(upperbb_btc, 1), btc=predictions_readable_btc,
                           eth_price=round(price_eth, 1), eth_rsi=round(rsi_eth, 1), eth_lowerbb=round(lowerbb_eth, 1), eth_upperbb=round(upperbb_eth, 1), eth=predictions_readable_eth,
                           sol_price=round(price_sol, 1), sol_rsi=round(rsi_sol, 1), sol_lowerbb=round(lowerbb_sol, 1), sol_upperbb=round(upperbb_sol, 1), sol=predictions_readable_sol)