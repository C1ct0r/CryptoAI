import mysql.connector
from flask import Flask, render_template, redirect, jsonify
from datetime import date

app = Flask(__name__)

db_host = "127.0.0.1"
db_user = "root"
db_password = "mysqldev"
db_port = "3307"
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

@app.route("/")
def main():
    return redirect("/charts")

@app.route("/charts")
def charts():
    return render_template("charts.html")

if __name__ == '__main__': app.run(debug=True, port=8000, host='0.0.0.0')