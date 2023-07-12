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
    location.href = "/menu?location=ticket";
}

function reference_change() {
    let reference_textarea = document.getElementById("reference-input");
    reference_textarea.style.padding = "6px";
    reference_textarea.style.border = "";

    let reference_value = reference_textarea.value;

    let length = reference_value.length;

    document.getElementById("reference-maxlength").innerHTML = length + "/50";

    if (length == 50) {
        document.getElementById("reference-maxlength").style.color = "#D93E3E";
    } else {
        document.getElementById("reference-maxlength").style.color = "#F1F6F9";
    }
}

function body_change() {
    let body_textarea = document.getElementById("body-input");
    body_textarea.style.padding = "6px";
    body_textarea.style.border = "";

    let body_value = body_textarea.value;

    let length = body_value.length;

    document.getElementById("body-maxlength").innerHTML = length + "/500";

    if (length == 500) {
        document.getElementById("body-maxlength").style.color = "#D93E3E";
    } else {
        document.getElementById("body-maxlength").style.color = "#F1F6F9";
    }
}

async function submit() {
    let reference = document.getElementById("reference-input").value;
    let body = document.getElementById("body-input").value;

    if (reference == "" && body == "") {
        let reference_input = document.getElementById("reference-input");
        reference_input.style.padding = "4px";
        reference_input.style.border = "2px solid #D93E3E";

        let body_input = document.getElementById("body-input");
        body_input.style.padding = "4px";
        body_input.style.border = "2px solid #D93E3E";
    } else if (reference == "") {
        let reference_input = document.getElementById("reference-input");
        reference_input.style.padding = "4px";
        reference_input.style.border = "2px solid #D93E3E";
    } else if (body == "") {
        let body_input = document.getElementById("body-input");
        body_input.style.padding = "4px";
        body_input.style.border = "2px solid #D93E3E";
    } else {
        let username = JSON.parse(localStorage.getItem("username"));
        let password = JSON.parse(localStorage.getItem("password"));

        if (sessionStorage.getItem("token") == null) {
            await get_token();
        }

        if (username != null && password != null) {
            username = username.value;
            password = password.value;

            let response = await fetch("/api/v1/ticket", {
                headers: {
                    "username": username,
                    "password": password,
                    "token": sessionStorage.getItem("token"),
                    "reference": reference,
                    "body": body
                }
            });

            let myjson = await response.json();

            let status = myjson["status"];

            if (status == 0) {
                location.href = "/error";
            } else {
                ticket_submitted();
            }
        } else {
            return;
        }
    }
}

function ticket_submitted() {
    document.getElementById("header").remove();
    document.getElementById("content").remove();
    
    let main = document.getElementById("main");
    main.style.justifyContent = "center";
    main.style.color = "#F1F6F9";
    main.style.gap = "24px";

    let boxwrapper1 = document.getElementById("main");

    let text_wrapper = document.createElement("div");
    text_wrapper.classList.add("text-wrapper");
    text_wrapper.setAttribute("id", "text-wrapper");

    boxwrapper1.appendChild(text_wrapper);

    let boxwrapper2 = document.getElementById("text-wrapper");

    let icon = document.createElement("span");
    icon.classList.add("material-symbols-rounded", "size-48");
    icon.innerHTML = "check_circle";

    boxwrapper2.appendChild(icon);

    let text = document.createElement("p");
    text.classList.add("text");
    text.setAttribute("id", "info-text");
    text.innerHTML = "Your ticket was submitted";

    boxwrapper2.appendChild(text);

    let counter = document.createElement("p");
    counter.classList.add("text");
    counter.setAttribute("id", "counter-text");
    counter.innerHTML = "3";

    boxwrapper1.appendChild(counter);

    counter_interval();
}

let counter = 3;

function counter_interval() {
    setInterval(update, 1000);
}

function update() {
    if (counter >= 1) {
        let counter_text = document.getElementById("counter-text");

        counter = counter - 1;

        counter_text.innerHTML = counter;
    } else {
        location.href = "/";
    }
}