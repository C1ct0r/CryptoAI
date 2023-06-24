import mysql.connector
from tensorflow_process_data import getdata, evaluatedata
from flask import Flask, render_template, redirect, request, jsonify, session
from datetime import date

app = Flask(__name__)
app.secret_key = 'session_secret_key bad_secret_key'

@app.route("/api/token")
def token_api():
    clientname = request.headers['clientname']
    clientkey = request.headers['clientkey']

    db = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='mysqldev',
        database='tensorflow',
        port='3307'
    )

    cursor = db.cursor(buffered=True)

    cursor.execute("SELECT token FROM backend WHERE clientname = %s AND clientkey = %s", (clientname, clientkey, ))
    token = cursor.fetchone()
    if token == None:
        return jsonify({'token': 'falsetoken'})
    else:
        token = token[0]

    db.close()

    return jsonify({'token': token})

@app.route("/api/prediction")
def predict_api():
    token = request.headers['token']
    authkey = request.headers['authkey']
    crypto = request.headers['coin']
    fiat = request.headers['fiat']

    db = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='mysqldev',
        database='tensorflow',
        port='3307'
    )

    cursor = db.cursor(buffered=True)

    cursor.execute("SELECT token FROM backend WHERE authkey = %s", (authkey, ))
    token_sql = cursor.fetchone()
    token_sql = token_sql[0]

    db.close()

    if token == token_sql:
        db = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='mysqldev',
        database='tensorflow',
        port='3307'
        )
        
        cursor = db.cursor(buffered=True)

        cursor.execute("SELECT level FROM backend WHERE authkey = %s", (authkey, ))
        level = cursor.fetchone()
        level = level[0]

        getdata(crypto, fiat, 'binance', '1d')
        evaluatedata(crypto, fiat, 'binance', '1d', level)

        return jsonify({'priced': '123443',
                        'priceh': '34233',
                        'predictiond': '2',
                        'predictionh': '1',
                        'model': 'BTC1-1'})
    else:
        return jsonify({'error': 'authkey and token not matching'})

@app.route("/")
def route1():
    return render_template("chart.html")

if __name__ == '__main__': app.run(debug=True, port=8000, host='0.0.0.0')