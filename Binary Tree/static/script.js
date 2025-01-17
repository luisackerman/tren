const baseUrl = "http://127.0.0.1:5000";

document.getElementById("searchBtn").addEventListener("click", () => {
    const key = document.getElementById("keyInput").value;
    if (key === "") {
        document.getElementById("result").textContent = "Please enter a key.";
        return;
    }
    fetch(`${baseUrl}/search?key=${key}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById("result").textContent = 
                data.found 
                ? `Key ${data.key} found in the tree.` 
                : `Key ${data.key} not found in the tree.`;
        })
        .catch(err => console.error(err));
});

document.getElementById("deleteBtn").addEventListener("click", () => {
    const key = document.getElementById("keyInput").value;
    if (key === "") {
        document.getElementById("result").textContent = "Please enter a key.";
        return;
    }
    fetch(`${baseUrl}/delete`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ key: parseInt(key) })
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById("result").textContent = data.message;
        })
        .catch(err => console.error(err));
});
