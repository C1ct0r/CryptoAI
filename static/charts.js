function menu() {

}

function coin_button() {
    document.getElementById("content-start").style.display = "none";
    document.getElementById("coin-button").style.display = "none";

    document.getElementById("content-coin").style.display = "flex";
}

function coin_pass(coin) {
    let coin_passed = coin;
    
    sessionStorage.setItem("coin", coin_passed);

    document.getElementById("content-coin").style.display = "none";
    
    document.getElementById("content-currency").style.display = "flex";
}

async function currency_pass(currency) {
    let currency_passed = currency;

    sessionStorage.setItem("currency", currency_passed);

    document.getElementById("content-currency").style.display = "none";

    let clientname = localStorage.getItem("clientname");
    let clientkey = localStorage.getItem("clientkey");

    async function fetchtoken() {
        const response = await fetch('/api/token', {
            headers: {
                'clientname': clientname,
                'clientkey': clientkey,
            }
        });
        const json = await response.json();
        sessionStorage.setItem("token", json["token"]);
    }

    await fetchtoken();

    if (sessionStorage.getItem("token") == "falsetoken") {
        api_error();
    } else {
        token_ok();
    }
}

async function api_error() {
    document.getElementById("main-class").style.display = "none";
    document.getElementById("error-class").style.display = "flex";

    document.getElementById("error-error").innerHTML = "It looks like you do not have permission to access the api";
}

async function token_ok() {
    let crypto = sessionStorage.getItem("coin");
    let fiat = sessionStorage.getItem("currency");

    let day = new Date();
    day = day.getDate();
    if (day < 10) {
        day = "0" + day;
    }

    let month = new Date();
    month = month.getMonth();
    month += 1;
    if (month < 10) {
        month = "0" + month;
    }

    let year = new Date();
    year = year.getFullYear();

    let date = day + "." + month + "." + year;

    let hours = new Date();
    hours = hours.getHours();
    if (hours < 10) {
        hours = "0" + hours;
    }

    let minutes = new Date();
    minutes = minutes.getMinutes();
    if (minutes < 10) {
        minutes = "0" + minutes;
    }

    let time = hours + ":" + minutes;

    let price_symbol;
    let priced;
    let priceh;
    let predictiond;
    let predictionh;
    let model;

    async function fetchprediction() {
        const response = await fetch('/api/prediction', {
            headers: {
                'token': sessionStorage.getItem("token"),
                'authkey': localStorage.getItem("authkey"),
                'coin': sessionStorage.getItem("coin"),
                'fiat': sessionStorage.getItem("currency"),
            }
        });
        const json = await response.json();

        let objsize = Object.keys(json).length;

        sessionStorage.setItem("objsize", objsize);

        priced = json['priced'];
        priceh = json['priceh'];
        predictiond = json['predictiond'];
        predictionh = json['predictionh'];
        model = json['model'];
    }

    await fetchprediction();

    if (sessionStorage.getItem("objsize") == 1) {
        sessionStorage.removeItem("objsize");
        api_error();
    } else {
        if (fiat == "EUR") {
            price_symbol = "€";
        } else if (fiat == "USD") {
            price_symbol = "$";
        }
    
        priced = priced + price_symbol;
        priceh = priceh + price_symbol;
    
        if (predictiond == 1) {
            predictiond = "trending_up";
        } else if (predictiond = 2) {
            predictiond = "trending_down";
        }
    
        if (predictionh == 1) {
            predictionh = "trending_up";
        } else if (predictionh = 2) {
            predictionh = "trending_down";
        }
    
        document.getElementById("chart-coin1").innerHTML = crypto;
        document.getElementById("chart-coin2").innerHTML = crypto;
        document.getElementById("chart-date1").innerHTML = date;
        document.getElementById("chart-date2").innerHTML = date;
        document.getElementById("chart-time1").innerHTML = time;
        document.getElementById("chart-time2").innerHTML = time;
        document.getElementById("chart-priced").innerHTML = priced;
        document.getElementById("chart-priceh").innerHTML = priceh;
        document.getElementById("chart-trendd").innerHTML = predictiond;
        document.getElementById("chart-trendh").innerHTML = predictionh;
        document.getElementById("chart-model").innerHTML = model;
    
        document.getElementById("content-result").style.display = "flex";
        document.getElementById("back-button").style.display = "flex";

        sessionStorage.removeItem("objsize");
    }
}

function back_button() {
    document.getElementById("content-result").style.display = "none";
    document.getElementById("back-button").style.display = "none";

    document.getElementById("content-coin").style.display = "flex";
}