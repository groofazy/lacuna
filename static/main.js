const input = document.querySelector("#artist_input");
const btn = document.querySelector("#submit_btn");
btn.addEventListener("click", () => {
    const name = input.value.trim();

    if (!name) {
        alert("Please enter an artist name.");
        return;
    }

    // fetch block
    fetch("http://127.0.0.1:5000/artists", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ name: name })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message); // success
        } else if (data.error) {
            alert("Error: " + data.error); // error from backend
        }
    })
    .catch(err => {
        console.error('Request failed:', err);
        alert("Something went wrong.");
    });
});