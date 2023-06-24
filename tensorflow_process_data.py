import mysql.connector
from tradingview_ta import TA_Handler, Interval, Exchange
import tradingview_ta
import numpy as np
import tensorflow as tf

# Create global id variable
identification = 0

# Connect to mysql database
db = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='mysqldev',
    database='tensorflow',
    port='3307'
)

# Create cursor object
cursor = db.cursor(buffered=True)

# Disconnect from mysql database
db.close()

# Create getdata function
def getdata(input_crypto, input_fiat, input_exchange, input_timeframe):
    # Global assignment
    global identification

    # Assign the inputs to variables
    crypto = input_crypto
    fiat = input_fiat
    exchange = input_exchange
    timeframe = input_timeframe

    # Connect to mysql database
    db = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='mysqldev',
        database='tensorflow',
        port='3307'
    )

    # Create cursor object
    cursor = db.cursor(buffered=True)

    # Create symbol
    symbol = crypto + fiat

    # Create tablename
    tablename = symbol + '-' + exchange + '-' + timeframe

    # Create table if it doesn't exist yet
    cursor.execute("CREATE TABLE IF NOT EXISTS `%s` (ID INT, price FLOAT, rsi FLOAT, upper_bb FLOAT, lower_bb FLOAT, prediction INT, used INT)", (tablename, ))
    db.commit()

    # Set up ta handler
    handler = TA_Handler(
        symbol=symbol,
        exchange=exchange,
        screener="crypto",
        interval=timeframe,
        timeout=None
    )

    # Get the data with the handler
    close = handler.get_analysis().indicators["close"]
    rsi = handler.get_analysis().indicators["RSI"]
    upper_bb = handler.get_analysis().indicators["BB.upper"]
    lower_bb = handler.get_analysis().indicators["BB.lower"]

    # Get latest id from table
    cursor.execute("SELECT ID FROM `%s` ORDER BY ID DESC", (tablename, ))
    identification = cursor.fetchone()

    # Evaluate the id data
    if identification == None:
        identification = 1
    else:
        identification = identification[0] + 1
    
    # Set id variable
    identification = identification

    # Insert the data into the table (prediction and used is set to 0 / prediction positive if 1 and negative if 2)
    cursor.execute("INSERT INTO `%s` VALUES (%s, %s, %s, %s, %s, 0, 0)", (tablename, identification, close, rsi, upper_bb, lower_bb))
    db.commit()

    # Close the database connection
    db.close()

def evaluatedata(input_crypto, input_fiat, input_exchange, input_timeframe, input_level):
    # Assign the inputs to variables
    crypto = input_crypto
    fiat = input_fiat
    exchange = input_exchange
    timeframe = input_timeframe
    level = input_level

    # Connect to mysql database
    db = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='mysqldev',
        database='tensorflow',
        port='3307'
    )

    # Create cursor object
    cursor = db.cursor(buffered=True)

    # Create symbol
    symbol = crypto + fiat

    # Create tablename
    tablename = symbol + '-' + exchange + '-' + timeframe

    # Get the data from the database
    cursor.execute("SELECT price, rsi, upper_bb, lower_bb FROM `%s` WHERE ID = %s", (tablename, identification))
    data = cursor.fetchone()

    # Assign the tuple data to variables
    price = data[0]
    rsi = data[1]
    upper_bb = data[2]
    lower_bb = data[3]

    # Create a numpy array with the data
    input_data = np.array([[price, rsi, upper_bb, lower_bb]])
    input_data = input_data.reshape((input_data.shape[0], input_data.shape[1]))

    # Get the needed model from the database
    cursor.execute("SELECT model FROM models WHERE crypto = %s AND level = %s", (crypto, level))
    modelname = cursor.fetchone()
    modelname = modelname[0]

    # Load the model with the modelname
    model = tf.keras.models.load_model('models/' + modelname)

    # Make a prediction using the model
    prediction = model.predict(input_data)

    # Make prediction readable
    if prediction > 0.5:
        prediction = 1
    else:
        prediction = 2

    # Upload data in the table
    cursor.execute("UPDATE `%s` SET prediction = %s, used = 1 WHERE ID = %s", (tablename, prediction, identification))
    db.commit()

    # Close database connection
    db.close()