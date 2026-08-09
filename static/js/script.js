



let waitingForResponse = false;
let startPressed = false;
let pausePressed = false;

document.getElementById("stop-button").disabled = true; // disable the stop button initially
document.getElementById("pause-button").disabled = true; // disable the pause button initially

fetch("/api/get_settings") // initialize the input fields with the current settings from the server and set the initial countdown value
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        document.getElementById("work-min-input").value = data.work_min;
        count = data.work_min * 60; // set initial countdown value based on work_min
        document.getElementById("count_display").textContent = count;
        document.getElementById("break-min-input").value = data.break_min;
        document.getElementById("long-break-min-input").value = data.long_break_min;
        document.getElementById("break-cycles-input").value = data.cycles_before_long_break;
    });

setInterval(function() {
    if (waitingForResponse || !startPressed || pausePressed) {
        return; // skip this tick if waiting for a response
    }

    
    if (count < 0) {
        waitingForResponse = true; // pause ticking until fetch finishes
        
        fetch("/api/next_state")
            .then(function(response) {
                return response.json();
            })
            .then(function(data) {
                document.getElementById("state_display").textContent = "The current timer state is: " + data.state;
                count = data.current_state_min * 60; // reset the count to the new state's duration
                document.getElementById("count_display").textContent = count;
                waitingForResponse = false; // resume ticking
            });
    }
    document.getElementById("count_display").textContent = count;
    count--;
}, 1000);

document.getElementById("start-button").addEventListener("click", function() {
    startPressed = true;
    document.getElementById("start-button").disabled = true; // disable the button after it's clicked
    document.getElementById("stop-button").disabled = false; // enable the stop button
    document.getElementById("pause-button").disabled = false; // enable the pause button
});

document.getElementById("pause-button").addEventListener("click", function() {
    pausePressed = !pausePressed; // toggle the pause state
    document.getElementById("pause-button").textContent = pausePressed ? "Resume" : "Pause"; // change button text based on state
});

document.getElementById("stop-button").addEventListener("click", function() {
    startPressed = false;
    document.getElementById("start-button").disabled = false;
    document.getElementById("stop-button").disabled = true;
    document.getElementById("pause-button").disabled = true;
});

// document.getElementById("change-state-button").addEventListener("click", function() {
//     fetch("/api/next_state")
//         .then(function(response) {
//             return response.text();
//         })
//         .then(function(data) {
//             document.getElementById("state_display").textContent = "The current timer state is: " + data;
//         });
// });

document.getElementById("settings-button").addEventListener("click", function() {
    startPressed = false; // stop the timer when settings are changed
    document.getElementById("start-button").disabled = false; // disable the button after it's clicked
    document.getElementById("stop-button").disabled = true; // enable the stop button
    document.getElementById("pause-button").disabled = true; // enable the pause button

    const workMin = document.getElementById("work-min-input").value;
    const breakMin = document.getElementById("break-min-input").value;
    const longBreakMin = document.getElementById("long-break-min-input").value;
    const cyclesToLongBreak = document.getElementById("break-cycles-input").value;

    waitingForResponse = true;

    fetch("/api/set_settings", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            work_min: workMin,
            break_min: breakMin, 
            long_break_min: longBreakMin,
            cycles_before_long_break: cyclesToLongBreak})
    })
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            count = data.current_state_min * 60; // reset the count to the new state's duration
            document.getElementById("count_display").textContent = count;
            waitingForResponse = false; //resume ticking
        });
});
