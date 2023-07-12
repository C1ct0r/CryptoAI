let prediction_parameters = [];

async function credentials_expire() {
    let username = JSON.parse(localStorage.getItem("username"));
    let password = JSON.parse(localStorage.getItem("password"));

    if (username == null || password == null) {
        location.href = "/login";
    }

    username = username.timestamp;
    password = password.timestamp;

    let timestamp = new Date().getTime() / 1000;
    timestamp = parseInt(timestamp)
    timestamp = timestamp - 2592000;

    if (username < timestamp || password < timestamp) {
        localStorage.removeItem("username");
        localStorage.removeItem("password");

        let response = await fetch("/api/v1/logout");

        let myjson = await response.json();

        let status = myjson["status"];

        if (status == 1) {
            location.href = "/login";
        } else {
            return;
        }
    } else {
        return;
    }
}

async function get_token() {
    let username = JSON.parse(localStorage.getItem("username"));
    let password = JSON.parse(localStorage.getItem("password"));

    username = username.value;
    password = password.value;

    let response = await fetch("/api/v1/token", {
        headers: {
            "username": username,
            "password": password
        }
    });

    let myjson = await response.json();

    let status = myjson["status"];

    if (status == 0) {
        location.href = "/error";
    } else {
        let token = myjson["token"];
        sessionStorage.setItem("token", token);
    }
}

function menu() {
    location.href = "/menu?location=charts";
}

function back() {
    location.href = "/charts";
}

async function prediction() {
    let username = JSON.parse(localStorage.getItem("username"));
    let password = JSON.parse(localStorage.getItem("password"));

    username = username.value;
    password = password.value;

    let response = await fetch("/api/v1/predictionamount", {
        headers: {
            "username": username,
            "password": password
        }
    });

    let myjson = await response.json();

    let status = myjson["status"];

    let text = document.getElementById("start-text");
    let select_button = document.getElementById("start-evaluation-button");
    text.remove();
    select_button.remove();

    if (status == 0) {
        location.href = "/error";
    } else if (status == 1) {
        start_evaluation();
    } else if (status == 2) {
        predictions_level = myjson["predictions"];
        nopredictions_left(predictions_level);
    }
}

async function nopredictions_left(input_predictionslevel) {
    let boxwrapper = document.getElementById("content");

    let box = document.createElement("p");
    box.classList.add("content-text");
    box.setAttribute("id", "limit-text");
    predictions_level = input_predictionslevel;
    box.innerHTML = "You've used all of your " + predictions_level + " daily predictions. If you want to continue, you can take a look at our <a class='content-link' id='content-link' href='/plans'>plans</a>."

    boxwrapper.appendChild(box);
}

async function start_evaluation() {
    if (sessionStorage.getItem("token") == null) {
        await get_token();
    }

    async function get_crypto() {
        let username = JSON.parse(localStorage.getItem("username"));
        let password = JSON.parse(localStorage.getItem("password"));
        
        username = username.value;
        password = password.value;

        let response = await fetch("/api/v1/crypto", {
            headers: {
                "username": username,
                "password": password,
                "token": sessionStorage.getItem("token")
            }
        });

        let myjson = await response.json();

        let status = myjson["status"];

        if (status == 0) {
            location.href = "/error";
        } else {
            let coin = myjson["coin"];
            return coin;
        }
    }

    let coin = await get_crypto();
    let amount = coin.length;

    let boxwrapper = document.getElementById("content");

    let box = document.createElement("div");
    box.classList.add("button-container");
    box.setAttribute("id", "button-container-crypto");

    boxwrapper.appendChild(box);

    for (let i = 0; i < amount; i++) {
        let coin_current = coin[i];
        let coin_current_text = coin_current.toUpperCase();

        let boxwrapper = document.getElementById("button-container-crypto");

        let box = document.createElement("button");
        box.innerHTML = coin_current_text;
        box.classList.add("select-button");
        box.setAttribute("id", coin_current + "-button");
        box.setAttribute("onclick", "crypto('" + coin_current + "')");

        boxwrapper.appendChild(box);
    }
}

async function crypto(input_coin) {
    let coin = input_coin;

    prediction_parameters[0] = coin;

    let button_container = document.getElementById("button-container-crypto");
    button_container.remove();

    if (sessionStorage.getItem("token") == null) {
        await get_token();
    }

    async function get_fiat() {
        let username = JSON.parse(localStorage.getItem("username"));
        let password = JSON.parse(localStorage.getItem("password"));
        
        username = username.value;
        password = password.value;

        let response = await fetch("/api/v1/fiat", {
            headers: {
                "username": username,
                "password": password,
                "token": sessionStorage.getItem("token")
            }
        });

        let myjson = await response.json();

        let status = myjson["status"];

        if (status == 0) {
            location.href = "/error";
        } else {
            let fiat = myjson["fiat"];
            return fiat;
        }
    }

    let fiat = await get_fiat();
    let amount = fiat.length;

    let boxwrapper = document.getElementById("content");

    let box = document.createElement("div");
    box.classList.add("button-container");
    box.setAttribute("id", "button-container-fiat");

    boxwrapper.appendChild(box);

    for (let i = 0; i < amount; i++) {
        let fiat_current = fiat[i];
        let fiat_current_text = fiat_current.toUpperCase();

        let boxwrapper = document.getElementById("button-container-fiat");

        let box = document.createElement("button");
        box.innerHTML = fiat_current_text;
        box.classList.add("select-button");
        box.setAttribute("id", fiat_current + "-button");
        box.setAttribute("onclick", "fiat('" + fiat_current + "')");

        boxwrapper.appendChild(box);
    }
}

async function fiat(input_fiat) {
    let fiat = input_fiat;

    prediction_parameters[1] = fiat;

    let button_container = document.getElementById("button-container-fiat");
    button_container.remove();

    if (sessionStorage.getItem("token") == null) {
        await get_token();
    }

    async function get_exchange() {
        let username = JSON.parse(localStorage.getItem("username"));
        let password = JSON.parse(localStorage.getItem("password"));
        
        username = username.value;
        password = password.value;

        let response = await fetch("/api/v1/exchange", {
            headers: {
                "username": username,
                "password": password,
                "token": sessionStorage.getItem("token")
            }
        });

        let myjson = await response.json();

        let status = myjson["status"];

        if (status == 0) {
            location.href = "/error";
        } else {
            let exchange = myjson["exchange"];
            return exchange;
        }
    }

    let exchange = await get_exchange();
    let amount = exchange.length;

    let boxwrapper = document.getElementById("content");

    let box = document.createElement("div");
    box.classList.add("button-container");
    box.setAttribute("id", "button-container-exchange");

    boxwrapper.appendChild(box);

    for (let i = 0; i < amount; i++) {
        let exchange_current = exchange[i];
        let exchange_current_text = exchange_current.charAt(0).toUpperCase() + exchange_current.slice(1);

        let boxwrapper = document.getElementById("button-container-exchange");

        let box = document.createElement("button");
        box.innerHTML = exchange_current_text;
        box.classList.add("select-button");
        box.setAttribute("id", exchange_current + "-button");
        box.setAttribute("onclick", "exchange('" + exchange_current + "')");

        boxwrapper.appendChild(box);
    }
}

async function exchange(input_exchange) {
    let exchange = input_exchange;

    prediction_parameters[2] = exchange;

    let button_container = document.getElementById("button-container-exchange");
    button_container.remove();

    if (sessionStorage.getItem("token") == null) {
        await get_token();
    }

    async function get_prediction() {
        let username = JSON.parse(localStorage.getItem("username"));
        let password = JSON.parse(localStorage.getItem("password"));
        
        username = username.value;
        password = password.value;

        let response = await fetch("/api/v1/prediction", {
            headers: {
                "username": username,
                "password": password,
                "token": sessionStorage.getItem("token"),
                "crypto": prediction_parameters[0],
                "fiat": prediction_parameters[1],
                "exchange": prediction_parameters[2]
            }
        });

        let myjson = await response.json();

        let status = myjson["status"];

        if (status == 0) {
            location.href = "/error";
        } else {
            return myjson;
        }
    }

    let loader_point_blue = 2;
    let loader_point_gray = 1;

    let loader_interval;

    function loader_animation() {
        let point_blue = document.getElementById("loader-point-" + loader_point_blue);
        point_blue.style.marginBottom = "0";
        point_blue.style.backgroundColor = "#F1F6F9";

        let point_gray = document.getElementById("loader-point-" + loader_point_gray);
        point_gray.style.marginBottom = "0";
        point_gray.style.backgroundColor = "#F1F6F9";

        if (loader_point_blue == 5) {
            loader_point_blue = 1;

            point_blue = document.getElementById("loader-point-" + loader_point_blue);
            point_blue.style.marginBottom = "24px";
            point_blue.style.backgroundColor = "#394867";
        } else {
            loader_point_blue = loader_point_blue + 1;

            point_blue = document.getElementById("loader-point-" + loader_point_blue);
            point_blue.style.marginBottom = "24px";
            point_blue.style.backgroundColor = "#394867";
        }

        if (loader_point_gray == 5) {
            loader_point_gray = 1;

            point_gray = document.getElementById("loader-point-" + loader_point_gray);
            point_gray.style.marginBottom = "12px";
            point_gray.style.backgroundColor = "#9BA4B5";
        } else {
            loader_point_gray = loader_point_gray + 1;
            
            point_gray = document.getElementById("loader-point-" + loader_point_gray);
            point_gray.style.marginBottom = "12px";
            point_gray.style.backgroundColor = "#9BA4B5";
        }
    }

    function loader() {
        let boxwrapper = document.getElementById("content");

        let box = document.createElement("div");
        box.classList.add("loader");
        box.setAttribute("id", "loader");

        boxwrapper.appendChild(box);

        for (let i = 0; i < 5; i++) {
            let x = i + 1;

            let boxwrapper = document.getElementById("loader");

            let box = document.createElement("div");
            box.classList.add("loader-point");
            box.setAttribute("id", "loader-point-" + x);

            boxwrapper.appendChild(box);
        }

        let point_1 = document.getElementById("loader-point-1");
        point_1.style.marginBottom = "12px";
        point_1.style.backgroundColor = "#9BA4B5";

        let point_2 = document.getElementById("loader-point-2");
        point_2.style.marginBottom = "24px";
        point_2.style.backgroundColor = "#394867";

        loader_interval = setInterval(loader_animation, 250);
    }

    loader();

    let myjson = await get_prediction();

    let crypto = myjson["crypto"];
    console.log(crypto);
    crypto = crypto.toUpperCase();
    console.log(crypto);
    let date = myjson["date"];
    let model = myjson["model"];
    model = model.substring(0, model.length-3);
    model = model.toUpperCase();
    let price = myjson["price"];
    let symbol = myjson["symbol"];
    let time = myjson["time"];
    let timeframe = myjson["timeframe"];
    let timeframe_text = [];
    for (let i = 0; i < 2; i++) {
        timeframe_text.push(timeframe[i].charAt(0).toUpperCase() + timeframe[i].slice(1));
    }
    let trend = myjson["trend"];

    console.log(myjson);
        
    let loader_element = document.getElementById("loader");
    loader_element.remove();
        
    clearInterval(loader_interval);

    let boxwrapper = document.getElementById("content");

    let box = document.createElement("div");
    box.classList.add("prediction-container");
    box.setAttribute("id", "prediction-container");

    boxwrapper.appendChild(box);

    for (let i = 0; i < 2; i++) {
        let boxwrapper = document.getElementById("prediction-container");
        
        let box = document.createElement("div");
        box.classList.add("prediction-item");
        box.setAttribute("id", timeframe[i] + "-item");

        boxwrapper.appendChild(box);

        let prediction_item = document.getElementById(timeframe[i] + "-item");

        let prediction_title = document.createElement("p");
        prediction_title.classList.add("prediction-title");
        prediction_title.setAttribute("id", timeframe[i] + "-title");
        prediction_title.innerHTML = crypto + " - " + timeframe_text[i];

        prediction_item.appendChild(prediction_title);

        let info_container = document.createElement("div");
        info_container.classList.add("info-container");
        info_container.setAttribute("id", timeframe[i] + "-container");
        
        prediction_item.appendChild(info_container);

        info_container = document.getElementById(timeframe[i] + "-container");

        let prediction_info_date = document.createElement("p");
        prediction_info_date.classList.add("prediction-info");
        prediction_info_date.setAttribute("id", timeframe[i] + "-info-date");
        prediction_info_date.innerHTML = "Date: " + date;

        info_container.appendChild(prediction_info_date);

        let prediction_info_time = document.createElement("p");
        prediction_info_time.classList.add("prediction-info");
        prediction_info_time.setAttribute("id", timeframe[i] + "-info-time");
        prediction_info_time.innerHTML = "Time: " + time;

        info_container.appendChild(prediction_info_time);

        let prediction_info_price = document.createElement("p");
        prediction_info_price.classList.add("prediction-info");
        prediction_info_price.setAttribute("id", timeframe[i] + "-info-price");
        prediction_info_price.innerHTML = "Price: " + price[i] + symbol;

        info_container.appendChild(prediction_info_price);

        let trend_element = document.createElement("span");
        trend_element.classList.add("material-symbols-rounded", "size-42");
        trend_element.setAttribute("id", timeframe[i] + "-trend");
        trend_element.innerHTML = trend[i];

        prediction_item.appendChild(trend_element);
    }

    let prediction_container = document.getElementById("prediction-container");

    let model_element = document.createElement("p");
    model_element.classList.add("model-info");
    model_element.setAttribute("id", "model-info");
    model_element.innerHTML = "Model: " + model;

    prediction_container.appendChild(model_element);

    let footer = document.getElementById("footer");

    let button = document.createElement("button");
    button.classList.add("footer-button");
    button.setAttribute("id", "back-button");
    button.setAttribute("onclick", "back()");
    button.innerHTML = "Back";

    footer.appendChild(button);
}