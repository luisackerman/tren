const API_URL = 'http://127.0.0.1:5000';

const trainSelect = document.getElementById("train");
const startSelect = document.getElementById("start");
const targetSelect = document.getElementById("target");
const findPathButton = document.getElementById("findPath");
const resultDiv = document.getElementById("result");

// Fetch stations when a train line is selected
trainSelect.addEventListener("change", async () => {
    const selectedTrain = trainSelect.value;
    startSelect.innerHTML = `<option value="">Select Start Station</option>`;
    targetSelect.innerHTML = `<option value="">Target Station</option>`;

    if (selectedTrain) {
        try {
            const response = await fetch(`${API_URL}/stations/${selectedTrain}`);
            const data = await response.json();

            if (data.stations) {
                data.stations.forEach(station => {
                    const optionStart = document.createElement("option");
                    optionStart.value = station;
                    optionStart.textContent = station;

                    const optionTarget = document.createElement("option");
                    optionTarget.value = station;
                    optionTarget.textContent = station;

                    startSelect.appendChild(optionStart);
                    targetSelect.appendChild(optionTarget);
                });
            }
        } catch (error) {
            console.error("Error fetching stations:", error);
        }
    }
});

// Fetch route calculation when button is clicked
findPathButton.addEventListener("click", async () => {
    const trainLine = trainSelect.value;
    const start = startSelect.value;
    const target = targetSelect.value;

    if (trainLine && start && target) {
        try {
            const response = await fetch(`${API_URL}/route`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ train: trainLine, start, target }),
            });
            const data = await response.json();

            if (data.route) {
                resultDiv.innerHTML = `
                    <p><strong>Fastest Route:</strong> ${data.route.join(" → ")}</p>
                `;
            } else {
                resultDiv.innerHTML = `<p>${data.message}</p>`;
            }
        } catch (error) {
            console.error("Error finding route:", error);
        }
    } else {
        resultDiv.innerHTML = `<p>Please select a train, start station, and destination.</p>`;
    }
});
