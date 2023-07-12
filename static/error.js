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