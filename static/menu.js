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

function back() {
    let querystring = window.location.search;

    let urlparams = new URLSearchParams(querystring);

    let location_param = urlparams.get("location");
    console.log(location_param);

    location.href = "/" + location_param;
}

function charts() {
    location.href = "/charts";
}

function plans() {
    location.href = "/plans";
}

function api() {
    location.href = "/api";
}

function ticket() {
    location.href = "/ticket";
}

function account() {
    location.href = "/account";
}

async function logout() {
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
}

function legalnotice() {
    window.open("/legal/legalnotice");
}

function termsofuse() {
    window.open("/legal/termsofuse");
}

function privacypolicy() {
    window.open("/legal/privacypolicy");
}