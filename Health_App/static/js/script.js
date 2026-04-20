const messages = [
    "Analyzing your activity patterns...",
    "Checking health indicators...",
    "Running AI prediction model...",
    "Generating personalized results..."
];

let i = 0;

// Change loading text
setInterval(() => {
    const text = document.getElementById("loading-text");
    if (text) {
        text.innerText = messages[i];
        i = (i + 1) % messages.length;
    }
}, 1500);

// Auto submit form after delay
setTimeout(() => {
    const form = document.getElementById("hidden-form");
    if (form) {
        form.submit();
    }
}, 3500);