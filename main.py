import mysql.connector, tensorflow_prediction, hashlib
from flask import Flask, render_template, redirect, request, jsonify, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = "badcryptoaisecretkey"

db_host = "127.0.0.1"
db_user = "root"
db_password = "mysqldev"
db_port = "3306"
db_database = "cryptoai"

def db_setup():
    db = mysql.connector.connect(
        host = db_host,
        user = db_user,
        password = db_password,
        port = db_port
    )

    cursor = db.cursor(buffered=True)
    
    cursor.execute("CREATE DATABASE IF NOT EXISTS cryptoai")
    
    db.close()
    
    db = mysql.connector.connect(
        host = db_host,
        user = db_user,
        password = db_password,
        port = db_port,
        database = db_database
    )
    
    cursor = db.cursor(buffered=True)

    cursor.execute("CREATE TABLE IF NOT EXISTS crypto (cryptoID INT, levelID INT, coin TEXT)")
    db.commit()
    cursor.execute("CREATE TABLE IF NOT EXISTS exchange (exchangeID INT, levelID INT, exchangename TEXT)")
    db.commit()
    cursor.execute("CREATE TABLE IF NOT EXISTS discount (discountID INT, discountname TEXT, price FLOAT)")
    db.commit()
    cursor.execute("CREATE TABLE IF NOT EXISTS fiat (fiatID INT, levelID INT, currency TEXT, symbol TEXT)")
    db.commit()
    cursor.execute("CREATE TABLE IF NOT EXISTS level (levelID INT, levelname TEXT, price FLOAT, predictions INT, api INT, ticket TEXT)")
    db.commit()
    cursor.execute("CREATE TABLE IF NOT EXISTS model (modelID INT, levelID INT, cryptoID INT, version FLOAT, modelname TEXT, accuracy FLOAT)")
    db.commit()
    cursor.execute("CREATE TABLE IF NOT EXISTS payment (paymentID INT, userID INT, levelID INT, paymenttypeID INT, days INT, price FLOAT, timestamp BIGINT)")
    db.commit()
    cursor.execute("CREATE TABLE IF NOT EXISTS paymenttype (paymenttypeID INT, paymenttypename TEXT)")
    db.commit()
    cursor.execute("CREATE TABLE IF NOT EXISTS prediction (predictionID INT, modelID INT, fiatID INT, exchangeID INT, cryptoID INT, timestamp BIGINT, price FLOAT, rsi FLOAT, lowerbb FLOAT, upperbb FLOAT, value INT, timeframe TEXT)")
    db.commit()
    cursor.execute("CREATE TABLE IF NOT EXISTS user (userID INT, levelID INT, username TEXT, password TEXT, email TEXT, token TEXT, apitoken TEXT, apisecret TEXT, predictions INT, days INT, verified INT, code INT, codetimestamp BIGINT)")
    db.commit()
    cursor.execute("CREATE TABLE IF NOT EXISTS ticket (ticketID INT, userID INT, reference TEXT, body TEXT, edited INT)")
    db.commit()
    
    db.close()

db_setup()

@app.route("/api/v1/token")
def api_v1_token():
    db = mysql.connector.connect(
        host = db_host,
        user = db_user,
        password = db_password,
        port = db_port,
        database = db_database
    )
    
    cursor = db.cursor(buffered=True)

    username = request.headers["username"]

    cursor.execute("SELECT userID FROM user WHERE username = %s", (username,))
    userID = cursor.fetchone()
    
    if userID == None:
        json = {"status": 0}
        db.close()
        return jsonify(json)
    else:
        userID = userID[0]
    
    password = request.headers["password"]
    password = hashlib.md5(password.encode("utf-8")).hexdigest()
    
    cursor.execute("SELECT password FROM user WHERE userID = %s AND username = %s", (userID, username))
    password_sql = cursor.fetchone()

    if password_sql == None:
        json = {"status": 0}
        db.close()
        return jsonify(json)
    else:
        password_sql = password_sql[0]

    if password != password_sql:
        json = {"status": 0}
        db.close()
        return jsonify(json)
    else:
        cursor.execute("SELECT token FROM user WHERE userID = %s AND username = %s AND password = %s", (userID, username, password))
        token = cursor.fetchone()

        if token == None:
            json = {"status": 0}
            db.close()
            return jsonify(json)
        else:
            token = token[0]

            json = {"status": 1,
                    "token": token}
            db.close()
            return jsonify(json)

@app.route("/api/v1/predictionamount")
def api_v1_predictionamount():
    db = mysql.connector.connect(
        host = db_host,
        user = db_user,
        password = db_password,
        port = db_port,
        database = db_database
    )
    
    cursor = db.cursor(buffered=True)

    username = request.headers["username"]
    password = request.headers["password"]
    password = hashlib.md5(password.encode("utf-8")).hexdigest()

    cursor.execute("SELECT predictions FROM user WHERE username = %s AND password = %s", (username, password))
    predictions = cursor.fetchone()

    if predictions == None:
        json = {"status": 0}
        db.close()
        return jsonify(json)
    else:
        predictions = predictions[0]
    
    cursor.execute("SELECT userID FROM user WHERE username = %s AND password = %s", (username, password))
    userID = cursor.fetchone()

    if userID == None:
        json = {"status": 0}
        db.close()
        return jsonify(json)
    else:
        userID = userID[0]
    
    cursor.execute("SELECT levelID FROM user WHERE userID = %s", (userID,))
    levelID = cursor.fetchone()

    if levelID == None:
        json = {"status": 0}
        db.close()
        return jsonify(json)
    else:
        levelID = levelID[0]
    
    cursor.execute("SELECT predictions FROM level WHERE levelID = %s", (levelID,))
    predictions_level = cursor.fetchone()

    if predictions_level == None:
        json = {"status": 0}
        db.close()
        return jsonify(json)
    else:
        predictions_level = predictions_level[0]
    
    if predictions > 0:
        json = {"status": 1}
        db.close()
        return jsonify(json)
    else:
        json = {"status": 2,
                "predictions": predictions_level}
        db.close()
        return jsonify(json)

@app.route("/api/v1/crypto")
def api_v1_crypto():
    db = mysql.connector.connect(
        host = db_host,
        user = db_user,
        password = db_password,
        port = db_port,
        database = db_database
    )
    
    cursor = db.cursor(buffered=True)

    username = request.headers["username"]
    password = request.headers["password"]
    password = hashlib.md5(password.encode("utf-8")).hexdigest()
    token = request.headers["token"]

    cursor.execute("SELECT levelID FROM user WHERE username = %s AND password = %s AND token = %s", (username, password, token))
    levelID = cursor.fetchone()

    if levelID == None:
        json = {"status": 0}
        db.close()
        return jsonify(json)
    else:
        levelID = levelID[0]
    
    cursor.execute("SELECT coin FROM crypto WHERE levelID = %s", (levelID,))
    coin = cursor.fetchall()
    
    if not coin:
        if levelID == 3:
            levelID = 2

            cursor.execute("SELECT coin FROM crypto WHERE levelID = %s", (levelID,))
            coin = cursor.fetchall()

            if not coin:
                levelID = 1

                cursor.execute("SELECT coin FROM crypto WHERE levelID = %s", (levelID,))
                coin = cursor.fetchall()

                if not coin:
                    json = {"status": 0}
                    db.close()
                    return jsonify(json)
                elif coin:
                    amount = len(coin)
                    i = 0
                    
                    coin_return = []
                    
                    while i < amount:
                        coin_return.append(coin[i][0])
                        
                        i = i + 1
            elif coin:
                amount = len(coin)
                i = 0
                
                coin_return = []
                
                while i < amount:
                    coin_return.append(coin[i][0])
                    
                    i = i + 1
        elif levelID == 2:
            levelID = 1

            cursor.execute("SELECT coin FROM crypto WHERE levelID = %s", (levelID,))
            coin = cursor.fetchall()

            if not coin:
                json = {"status": 0}
                db.close()
                return jsonify(json)
            elif coin:
                amount = len(coin)
                i = 0
                
                coin_return = []
                
                while i < amount:
                    coin_return.append(coin[i][0])
                    
                    i = i + 1
        elif levelID == 1:
            json = {"status": 0}
            db.close()
            return jsonify(json)
    elif coin:
        amount = len(coin)
        i = 0

        coin_return = []

        while i < amount:
            coin_return.append(coin[i][0])

            i = i + 1

    json = {"status": 1,
            "coin": coin_return}
    db.close()
    return jsonify(json)

@app.route("/api/v1/fiat")
def api_v1_fiat():
    db = mysql.connector.connect(
        host = db_host,
        user = db_user,
        password = db_password,
        port = db_port,
        database = db_database
    )
    
    cursor = db.cursor(buffered=True)

    username = request.headers["username"]
    password = request.headers["password"]
    password = hashlib.md5(password.encode("utf-8")).hexdigest()
    token = request.headers["token"]

    cursor.execute("SELECT levelID FROM user WHERE username = %s AND password = %s AND token = %s", (username, password, token))
    levelID = cursor.fetchone()

    if levelID == None:
        json = {"status": 0}
        db.close()
        return jsonify(json)
    else:
        levelID = levelID[0]
    
    cursor.execute("SELECT currency FROM fiat WHERE levelID = %s", (levelID,))
    fiat = cursor.fetchall()
    
    if not fiat:
        if levelID == 3:
            levelID = 2

            cursor.execute("SELECT currency FROM fiat WHERE levelID = %s", (levelID,))
            fiat = cursor.fetchall()

            if not fiat:
                levelID = 1

                cursor.execute("SELECT currency FROM fiat WHERE levelID = %s", (levelID,))
                fiat = cursor.fetchall()

                if not fiat:
                    json = {"status": 0}
                    db.close()
                    return jsonify(json)
                elif fiat:
                    amount = len(fiat)
                    i = 0
                    
                    fiat_return = []
                    
                    while i < amount:
                        fiat_return.append(fiat[i][0])
                        
                        i = i + 1
            elif fiat:
                amount = len(fiat)
                i = 0
                
                fiat_return = []
                
                while i < amount:
                    fiat_return.append(fiat[i][0])
                    
                    i = i + 1
        elif levelID == 2:
            levelID = 1

            cursor.execute("SELECT currency FROM fiat WHERE levelID = %s", (levelID,))
            fiat = cursor.fetchall()

            if not fiat:
                json = {"status": 0}
                db.close()
                return jsonify(json)
            elif fiat:
                amount = len(fiat)
                i = 0
                
                fiat_return = []
                
                while i < amount:
                    fiat_return.append(fiat[i][0])
                    
                    i = i + 1
        elif levelID == 1:
            json = {"status": 0}
            db.close()
            return jsonify(json)
    elif fiat:
        amount = len(fiat)
        i = 0

        fiat_return = []

        while i < amount:
            fiat_return.append(fiat[i][0])

            i = i + 1

    json = {"status": 1,
            "fiat": fiat_return}
    db.close()
    return jsonify(json)

@app.route("/api/v1/exchange")
def api_v1_exchange():
    db = mysql.connector.connect(
        host = db_host,
        user = db_user,
        password = db_password,
        port = db_port,
        database = db_database
    )
    
    cursor = db.cursor(buffered=True)

    username = request.headers["username"]
    password = request.headers["password"]
    password = hashlib.md5(password.encode("utf-8")).hexdigest()
    token = request.headers["token"]

    cursor.execute("SELECT levelID FROM user WHERE username = %s AND password = %s AND token = %s", (username, password, token))
    levelID = cursor.fetchone()

    if levelID == None:
        json = {"status": 0}
        db.close()
        return jsonify(json)
    else:
        levelID = levelID[0]
    
    cursor.execute("SELECT exchangename FROM exchange WHERE levelID = %s", (levelID,))
    exchange = cursor.fetchall()
    
    if not exchange:
        if levelID == 3:
            levelID = 2

            cursor.execute("SELECT exchangename FROM exchange WHERE levelID = %s", (levelID,))
            exchange = cursor.fetchall()

            if not exchange:
                levelID = 1

                cursor.execute("SELECT exchangename FROM exchange WHERE levelID = %s", (levelID,))
                exchange = cursor.fetchall()

                if not exchange:
                    json = {"status": 0}
                    db.close()
                    return jsonify(json)
                elif exchange:
                    amount = len(exchange)
                    i = 0
                    
                    exchange_return = []
                    
                    while i < amount:
                        exchange_return.append(exchange[i][0])
                        
                        i = i + 1
            elif exchange:
                amount = len(exchange)
                i = 0
                
                exchange_return = []
                
                while i < amount:
                    exchange_return.append(exchange[i][0])
                    
                    i = i + 1
        elif levelID == 2:
            levelID = 1

            cursor.execute("SELECT exchangename FROM exchange WHERE levelID = %s", (levelID,))
            exchange = cursor.fetchall()

            if not exchange:
                json = {"status": 0}
                db.close()
                return jsonify(json)
            elif exchange:
                amount = len(exchange)
                i = 0
                
                exchange_return = []
                
                while i < amount:
                    exchange_return.append(exchange[i][0])
                    
                    i = i + 1
        elif levelID == 1:
            json = {"status": 0}
            db.close()
            return jsonify(json)
    elif exchange:
        amount = len(exchange)
        i = 0

        exchange_return = []

        while i < amount:
            exchange_return.append(exchange[i][0])

            i = i + 1

    json = {"status": 1,
            "exchange": exchange_return}
    db.close()
    return jsonify(json)

@app.route("/api/v1/prediction")
def api_v1_prediction():
    db = mysql.connector.connect(
        host = db_host,
        user = db_user,
        password = db_password,
        port = db_port,
        database = db_database
    )
    
    cursor = db.cursor(buffered=True)

    crypto = request.headers["crypto"]

    cursor.execute("SELECT cryptoID FROM crypto WHERE coin = %s", (crypto,))
    cryptoID = cursor.fetchone()

    if cryptoID == None:
        json = {"status": 0}
        db.close()
        return jsonify(json)
    else:
        cryptoID = cryptoID[0]
    
    fiat = request.headers["fiat"]

    cursor.execute("SELECT fiatID FROM fiat WHERE currency = %s", (fiat,))
    fiatID = cursor.fetchone()

    if fiatID == None:
        json = {"status": 0}
        db.close()
        return jsonify(json)
    else:
        fiatID = fiatID[0]
    
    exchange = request.headers["exchange"]

    cursor.execute("SELECT exchangeID FROM exchange WHERE exchangename = %s", (exchange,))
    exchangeID = cursor.fetchone()

    if exchangeID == None:
        json = {"status": 0}
        db.close()
        return jsonify(json)
    else:
        exchangeID = exchangeID[0]

    username = request.headers["username"]
    password = request.headers["password"]
    password = hashlib.md5(password.encode("utf-8")).hexdigest()
    token = request.headers["token"]

    cursor.execute("SELECT userID FROM user WHERE username = %s AND password = %s AND token = %s", (username, password, token))
    userID = cursor.fetchone()

    if userID == None:
        json = {"status": 0}
        db.close()
        return jsonify(json)
    else:
        userID = userID[0]
    
    db.close()
    
    ids = tensorflow_prediction.makeprediction(cryptoID, fiatID, exchangeID, userID)

    if ids == "nopredictions":
        json = {"status": 0}
        return jsonify(json)

    db = mysql.connector.connect(
        host = db_host,
        user = db_user,
        password = db_password,
        port = db_port,
        database = db_database
    )
    
    cursor = db.cursor(buffered=True)

    timeframe = []
    price = []
    trend = []

    cryptoID = []
    timeframe = []
    timestamp = []
    price = []
    value = []
    modelID = []
    fiatID = []

    cursor.execute("SELECT cryptoID, timeframe, timestamp, price, value, modelID, fiatID FROM prediction WHERE predictionID = %s", (ids[0],))
    fetch = cursor.fetchone()
    cryptoID.append(fetch[0])
    timeframe.append(fetch[1])
    timestamp.append(fetch[2])
    price.append(fetch[3])
    value.append(fetch[4])

    if value[0] == 2:
        trend.append("trending_down")
    elif value[0] == 1:
        trend.append("trending_up")

    modelID.append(fetch[5])
    fiatID.append(fetch[6])

    cursor.execute("SELECT cryptoID, timeframe, timestamp, price, value, modelID, fiatID FROM prediction WHERE predictionID = %s", (ids[1],))
    fetch = cursor.fetchone()
    cryptoID.append(fetch[0])
    timeframe.append(fetch[1])
    timestamp.append(fetch[2])
    price.append(fetch[3])
    value.append(fetch[4])

    if value[1] == 2:
        trend.append("trending_down")
    elif value[1] == 1:
        trend.append("trending_up")

    modelID.append(fetch[5])
    fiatID.append(fetch[6])

    if cryptoID[0] != cryptoID[1]:
        json = {"status": 0}
        db.close()
        return jsonify(json)
    elif cryptoID[0] == cryptoID[1]:
        cursor.execute("SELECT coin FROM crypto WHERE cryptoID = %s", (cryptoID[0],))
        coin = cursor.fetchone()

        if coin == None:
            json = {"status": 0}
            db.close()
            return jsonify(json)
        else:
            coin = coin[0]
    
    if timestamp[0] != timestamp[1]:
        json = {"status": 0}
        db.close()
        return jsonify(json)
    elif timestamp[0] == timestamp[1]:
        dt = datetime.fromtimestamp(timestamp[0])
        date = dt.strftime("%d.%m.%Y")
        time = dt.strftime("%H:%M")
    
    if modelID[0] != modelID[1]:
        json = {"status": 0}
        db.close()
        return jsonify(json)
    elif modelID[0] == modelID[1]:
        cursor.execute("SELECT modelname FROM model WHERE modelID = %s", (modelID[0],))
        modelname = cursor.fetchone()

        if modelname == None:
            json = {"status": 0}
            db.close()
            return jsonify(json)
        else:
            modelname = modelname[0]
    
    if fiatID[0] != fiatID[1]:
        json = {"status": 0}
        db.close()
        return jsonify(json)
    elif fiatID[0] == fiatID[1]:
        cursor.execute("SELECT symbol FROM fiat WHERE fiatID = %s", (fiatID[0],))
        symbol = cursor.fetchone()

        if symbol == None:
            json = {"status": 0}
            db.close()
            return jsonify(json)
        else:
            symbol = symbol[0]

    db.close()
    
    json = {"status": 1,
            "crypto": coin,
            "timeframe": timeframe,
            "date": date,
            "time": time,
            "price": price,
            "trend": trend,
            "model": modelname,
            "symbol": symbol}
    return jsonify(json)

@app.route("/api/v1/login")
def api_v1_login():
    db = mysql.connector.connect(
        host = db_host,
        user = db_user,
        password = db_password,
        port = db_port,
        database = db_database
    )
    
    cursor = db.cursor(buffered=True)

    username = request.headers["username"]
    password = request.headers["password"]
    password = hashlib.md5(password.encode("utf-8")).hexdigest()
    ts_fetch = request.headers["timestamp"]
    ts_fetch = int(ts_fetch)
    ts_fetch_30d = ts_fetch + 2592000

    cursor.execute("SELECT password FROM user WHERE username = %s", (username,))
    password_sql = cursor.fetchone()

    if password_sql == None:
        json = {"status": 0}
        db.close()
        return jsonify(json)
    else:
        password_sql = password_sql[0]
    
    if password_sql != password:
        json = {"status": 0}
        db.close()
        return jsonify(json)
    else:
        dt = datetime.now().replace(microsecond=0)
        ts = int(dt.timestamp())

        ts_next_day = ts + 86400

        if ts_next_day > ts_fetch_30d:
            ts = ts_fetch - 1

        session["user"] = ts
        
        json = {"status": 1}
        db.close()
        return jsonify(json)

@app.route("/api/v1/logout")
def api_v1_logout():
    session.pop('user', None)

    json = {"status": 1}
    return jsonify(json)

@app.route("/")
def main():
    if 'user' in session:
        user = session["user"]
        user = int(user)

        dt = datetime.now().replace(microsecond=0)
        ts = int(dt.timestamp())
        ts_previous_day = ts - 86400

        if user < ts_previous_day:
            session.pop('user', None)
            return redirect("/login")
        else:
            return redirect("/charts")
    else:
        return redirect("/login")

@app.route("/charts")
def charts():
    if 'user' in session:
        user = session["user"]
        user = int(user)

        dt = datetime.now().replace(microsecond=0)
        ts = int(dt.timestamp())
        ts_previous_day = ts - 86400

        if user < ts_previous_day:
            session.pop('user', None)
            return redirect("/login")
        else:
            return render_template("charts.html")
    else:
        return redirect("/login")

@app.route("/login")
def login():
    if 'user' in session:
        user = session["user"]
        user = int(user)

        dt = datetime.now().replace(microsecond=0)
        ts = int(dt.timestamp())
        ts_previous_day = ts - 86400

        if user < ts_previous_day:
            session.pop('user', None)
            return render_template("login.html")
        else:
            return redirect("/")
    else:
        return render_template("login.html")

if __name__ == '__main__': app.run(debug=True, port=8000, host='0.0.0.0')