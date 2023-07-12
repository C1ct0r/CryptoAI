async function credentials_expire() {
    let username = JSON.parse(localStorage.getItem("username"));
    let password = JSON.parse(localStorage.getItem("password"));

    if (username == null || password == null) {
        return;
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
        auto_login();
    }
}

async function auto_login() {
    let username = JSON.parse(localStorage.getItem("username"));
    let password = JSON.parse(localStorage.getItem("password"));

    if (username != null && password != null) {
        let timestamp = username.timestamp;
        username = username.value;
        password = password.value;

        let response = await fetch("/api/v1/login", {
            headers: {
                "username": username,
                "password": password,
                "timestamp": timestamp
            }
        });
    
        let myjson = await response.json();
    
        let status = myjson["status"];
    
        if (status == 0) {
            return;
        } else if (status == 1) {
            location.href = "/";
        }
    } else {
        return;
    }
}

function change_visibility(input_visibility) {
    let change_visibility = input_visibility;

    if (change_visibility == 'visible') {
        let input_field = document.getElementById("password-input-field");
        input_field.type = "text";

        let visibility_button = document.getElementById("visibility-button");
        visibility_button.remove();

        let boxwrapper = document.getElementById("password-input-container");

        let box = document.createElement("button");
        box.classList.add("visibility-button");
        box.setAttribute("id", "visibility-button");
        box.setAttribute("onclick", "change_visibility('invisible')");
        box.innerHTML = "<span class='material-symbols-rounded size-24'>visibility_off</span>";

        boxwrapper.appendChild(box);
    } else if (change_visibility == 'invisible') {
        let input_field = document.getElementById("password-input-field");
        input_field.type = "password";

        let visibility_button = document.getElementById("visibility-button");
        visibility_button.remove();

        let boxwrapper = document.getElementById("password-input-container");

        let box = document.createElement("button");
        box.classList.add("visibility-button");
        box.setAttribute("id", "visibility-button");
        box.setAttribute("onclick", "change_visibility('visible')");
        box.innerHTML = "<span class='material-symbols-rounded size-24'>visibility</span>";

        boxwrapper.appendChild(box);
    }
}

async function login() {
    let username_input = document.getElementById("username-input-field").value;
    let password_input = document.getElementById("password-input-field").value;

    if (username_input == '' && password_input == '') {
        let username_input_field_input = document.querySelector("input.username-input-field");
        username_input_field_input.style.paddingLeft = "10px";
        username_input_field_input.style.paddingRight = "10px";
        username_input_field_input.style.paddingTop = "4px";
        username_input_field_input.style.paddingBottom = "4px";

        let username_input_field = document.getElementById("username-input-field");
        username_input_field.style.border = "2px solid #D93E3E";

        let password_input_field_input = document.querySelector("input.password-input-field");
        password_input_field_input.style.paddingLeft = "10px";
        password_input_field_input.style.paddingRight = "10px";
        password_input_field_input.style.paddingTop = "4px";
        password_input_field_input.style.paddingBottom = "4px";

        let password_input_field = document.getElementById("password-input-field");
        password_input_field.style.border = "2px solid #D93E3E";

        return;
    } else if (username_input == '') {
        let username_input_field_input = document.querySelector("input.username-input-field");
        username_input_field_input.style.paddingLeft = "10px";
        username_input_field_input.style.paddingRight = "10px";
        username_input_field_input.style.paddingTop = "4px";
        username_input_field_input.style.paddingBottom = "4px";

        let username_input_field = document.getElementById("username-input-field");
        username_input_field.style.border = "2px solid #D93E3E";

        return;
    } else if (password_input == '') {
        let password_input_field_input = document.querySelector("input.password-input-field");
        password_input_field_input.style.paddingLeft = "10px";
        password_input_field_input.style.paddingRight = "10px";
        password_input_field_input.style.paddingTop = "4px";
        password_input_field_input.style.paddingBottom = "4px";

        let password_input_field = document.getElementById("password-input-field");
        password_input_field.style.border = "2px solid #D93E3E";

        return;
    }

    let timestamp = new Date().getTime() / 1000;
    timestamp = parseInt(timestamp)
    let username = {value: username_input, timestamp: timestamp};
    let password = {value: password_input, timestamp: timestamp};

    localStorage.setItem("username", JSON.stringify(username));
    localStorage.setItem("password", JSON.stringify(password));

    let response = await fetch("/api/v1/login", {
        headers: {
            "username": username_input,
            "password": password_input,
            "timestamp": timestamp
        }
    });

    let myjson = await response.json();

    let status = myjson["status"];

    if (status == 0) {
        let username_input_field_input = document.querySelector("input.username-input-field");
        username_input_field_input.style.paddingLeft = "10px";
        username_input_field_input.style.paddingRight = "10px";
        username_input_field_input.style.paddingTop = "4px";
        username_input_field_input.style.paddingBottom = "4px";

        let username_input_field = document.getElementById("username-input-field");
        username_input_field.style.border = "2px solid #D93E3E";

        let password_input_field_input = document.querySelector("input.password-input-field");
        password_input_field_input.style.paddingLeft = "10px";
        password_input_field_input.style.paddingRight = "10px";
        password_input_field_input.style.paddingTop = "4px";
        password_input_field_input.style.paddingBottom = "4px";

        let password_input_field = document.getElementById("password-input-field");
        password_input_field.style.border = "2px solid #D93E3E";

        return;
    } else if (status == 1) {
        location.href = "/";
    }
}

function input_valuechange(input_field) {
    let field = input_field;

    if (field == "username") {
        let username_input_field_input = document.querySelector("input.username-input-field");
        username_input_field_input.style.paddingLeft = "12px";
        username_input_field_input.style.paddingRight = "12px";
        username_input_field_input.style.paddingTop = "6px";
        username_input_field_input.style.paddingBottom = "6px";

        let username_input_field = document.getElementById("username-input-field");
        username_input_field.style.border = "";
    } else if (field == "password") {
        let password_input_field_input = document.querySelector("input.password-input-field");
        password_input_field_input.style.paddingLeft = "12px";
        password_input_field_input.style.paddingRight = "12px";
        password_input_field_input.style.paddingTop = "6px";
        password_input_field_input.style.paddingBottom = "6px";

        let password_input_field = document.getElementById("password-input-field");
        password_input_field.style.border = "";
    }
}