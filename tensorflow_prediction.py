import mysql.connector, datetime
from tradingview_ta import TA_Handler
import numpy as np
import tensorflow as tf

db_host = "127.0.0.1"
db_user = "root"
db_password = "mysqldev"
db_port = "3307"
db_database = "cryptoai"

def makeprediction(input_cryptoid, input_fiatid, input_exchangeid, input_userid):
    cryptoid = input_cryptoid
    fiatid = input_fiatid
    exchangeid = input_exchangeid
    userid = input_userid

    db = mysql.connector.connect(
        host = db_host,
        user = db_user,
        password = db_password,
        port = db_port,
        database = db_database
    )

    cursor = db.cursor(buffered=True)

    cursor.execute("SELECT coin FROM crypto WHERE cryptoID = %s", (cryptoid,))
    crypto = cursor.fetchone()
    crypto = crypto[0]

    cursor.execute("SELECT currency FROM fiat WHERE fiatID = %s", (fiatid,))
    fiat = cursor.fetchone()
    fiat = fiat[0]

    symbol = crypto + fiat

    cursor.execute("SELECT exchangename FROM exchange WHERE exchangeID = %s", (exchangeid,))
    exchange = cursor.fetchone()
    exchange = exchange[0]

    cursor.execute("SELECT levelID FROM user WHERE userID = %s", (userid,))
    levelid = cursor.fetchone()
    levelid = levelid[0]

    cursor.execute("SELECT modelID, levelID, modelname FROM model WHERE cryptoID = %s ORDER BY levelID DESC", (cryptoid,))
    fetch = cursor.fetchall()

    length = len(fetch)
    x = 0

    while x < length:
        listfetch = fetch[x]
        listmodelid = listfetch[0]
        listlevelid = listfetch[1]
        listmodelname = listfetch[2]

        if listlevelid <= levelid:
            x = 3
            modelid = listmodelid
            modelname = listmodelname
        else:
            x = x + 1

    model = tf.keras.models.load_model('models/' + modelname)

    timestamp = datetime.datetime.now()
    timestamp = timestamp.timestamp()
    timestamp = int(timestamp)

    cursor.execute("SELECT predictionID FROM prediction ORDER BY predictionID DESC")
    predictionid = cursor.fetchone()

    if predictionid == None:
        predictionid = 0
    else:
        predictionid = predictionid[0]

    handlerd = TA_Handler(
        symbol = symbol,
        exchange = exchange,
        screener = 'crypto',
        interval = '1D',
        timeout = None
    )
    
    priced = handlerd.get_analysis().indicators["close"]
    rsid = handlerd.get_analysis().indicators["RSI"]
    upperbbd = handlerd.get_analysis().indicators["BB.upper"]
    lowerbbd = handlerd.get_analysis().indicators["BB.lower"]

    input_datad = np.array([[priced, rsid, upperbbd, lowerbbd]])
    input_datad = input_datad.reshape((input_datad.shape[0], input_datad.shape[1]))

    predictiond = model.predict(input_datad)

    if predictiond > 0.5:
        predictiond = 1
    else:
        predictiond = 2
    
    predictionidd = predictionid + 1

    cursor.execute("INSERT INTO prediction VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (predictionidd, modelid, fiatid, exchangeid, cryptoid, timestamp, priced, rsid, lowerbbd, upperbbd, predictiond, "Day"))
    db.commit()

    handlerh = TA_Handler(
        symbol = symbol,
        exchange = exchange,
        screener = 'crypto',
        interval = '1h',
        timeout = None
    )
    
    priceh = handlerh.get_analysis().indicators["close"]
    rsih = handlerh.get_analysis().indicators["RSI"]
    upperbbh = handlerh.get_analysis().indicators["BB.upper"]
    lowerbbh = handlerh.get_analysis().indicators["BB.lower"]

    input_datah = np.array([[priceh, rsih, upperbbh, lowerbbh]])
    input_datah = input_datah.reshape((input_datah.shape[0], input_datah.shape[1]))

    predictionh = model.predict(input_datah)

    if predictionh > 0.5:
        predictionh = 1
    else:
        predictionh = 2
    
    predictionidh = predictionid + 2

    cursor.execute("INSERT INTO prediction VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (predictionidh, modelid, fiatid, exchangeid, cryptoid, timestamp, priceh, rsih, lowerbbh, upperbbh, predictionh, "Hour"))
    db.commit()

    db.close()

    ids = dict()
    ids['Day'] = predictionidd
    ids['Hour'] = predictionidh

    return ids