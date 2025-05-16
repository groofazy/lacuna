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
        body: JSON.stringify({ artist_name: name })
    })

    .then(response => response.json())
    
    .then(data => {
        if (data.message) {
            // alert(data.message); // success
            load_artists();
        } else if (data.error) {
            alert("Error: " + data.error); // error from backend
        }
    })
    
    .catch(err => {
        console.error('Request failed:', err);
        alert("Something went wrong.");
    });
});

function load_artists() {
    fetch("http://127.0.0.1:5000/artists")
    .then(response => response.json())
    .then(data => {
        const listContainer = document.querySelector("#artist_list");
        listContainer.innerHTML = ""; // clear existing list

        data.forEach(artist => {
            const item = document.createElement("div"); // dynamically create element
            item.textContent = `${artist.name} - ${artist.num_albums} albums - Popularity: ${artist.popularity} - Top Tracks: ${artist.top_tracks}`;
            
            const deleteBtn = document.createElement("button"); // dynamically create element
            
            deleteBtn.className = "delete-btn";
            
            deleteBtn.textContent = "Delete";
            deleteBtn.style.marginLeft = "10px";

            deleteBtn.addEventListener("click", () => {
                fetch(`http://127.0.0.1:5000/artists/${encodeURIComponent(artist.name)}`, {
                    method: "DELETE"
            })
            .then(response => response.json())
            .then(data => {
                load_artists(); // refresh the list after deletion
            })
            .catch(err => {
                console.error("Failed to delete artist:", err);
            });
        });
        
        item.appendChild(deleteBtn);
        listContainer.appendChild(item);
        });
    })
    .catch(err => {
        console.error("Failed to load artists:", err);
    });
}

load_artists()