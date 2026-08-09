

let count = 20
let waitingForResponse = false;

setInterval(function() {
    if (waitingForResponse) {
        return; // skip this tick if waiting for a response
    }

    document.getElementById("counter_display").textContent = count;
    count--;
    if (count < 0) {
        waitingForResponse = true; // pause ticking until fetch finishes

        fetch("/api/next_state")
            .then(function(response) {
            return response.text();
            })
            .then(function(data) {
                document.getElementById("state_display").textContent = "The current timer state is: " + data;
                waitingForResponse = false; // resume ticking
                count = 20; // reset the counter
            });
    }
}, 1000);

document.getElementById("change-state-button").addEventListener("click", function() {
    fetch("/api/next_state")
        .then(function(response) {
        return response.text();
        })
        .then(function(data) {
            document.getElementById("state_display").textContent = "The current timer state is: " + data;
        });
});

