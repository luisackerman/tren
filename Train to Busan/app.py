from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Stations data
stations = {
    "LRT1": [
        "Baclaran", "EDSA", "Libertad", "Gil Puyat", "Vito Cruz",
        "Quirino", "Pedro Gil", "United Nations", "Central Terminal",
        "Carriedo", "Doroteo Jose", "Bambang", "Tayuman", "Blumentritt",
        "Abad Santos", "R. Papa", "5th Avenue", "Monumento", "Balintawak",
        "Roosevelt"
    ],
    "LRT2": [
        "Recto", "Legarda", "Pureza", "V. Mapa", "J. Ruiz",
        "Gilmore", "Betty Go-Belmonte", "Cubao", "Anonas",
        "Katipunan", "Santolan", "Marikina", "Antipolo"
    ],
    "MRT": [
        "North Avenue", "Quezon Avenue", "GMA-Kamuning", "Araneta Center-Cubao",
        "Santolan-Annapolis", "Ortigas", "Shaw Boulevard", "Boni", "Guadalupe",
        "Buendia", "Ayala", "Magallanes", "Taft Avenue"
    ]
}

@app.after_request
def add_cors_headers(response):
    """Add CORS headers to all responses."""
    response.headers.add("Access-Control-Allow-Origin", "*")  # Allow all origins
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
    return response

@app.route('/')
def index():
    """Serve the frontend HTML."""
    return render_template('template/index.html')

@app.route('/stations/<train>', methods=['GET'])
def get_stations(train):
    """Return the list of stations for a specific train line."""
    if train in stations:
        return jsonify({"stations": stations[train]})
    return jsonify({"message": "Train line not found"}), 404

@app.route('/route', methods=['POST'])
def calculate_route():
    """Calculate the route between start and target stations."""
    data = request.json

    train = data.get("train")
    start = data.get("start")
    target = data.get("target")

    if not (train and start and target):
        return jsonify({"message": "Missing train, start, or target parameter"}), 400

    if train in stations:
        train_stations = stations[train]
        try:
            start_index = train_stations.index(start)
            target_index = train_stations.index(target)
        except ValueError:
            return jsonify({"message": "Invalid start or destination station"}), 400

        # Calculate the route
        if start_index <= target_index:
            route = train_stations[start_index:target_index + 1]
        else:
            route = train_stations[target_index:start_index + 1][::-1]

        return jsonify({"route": route})

    return jsonify({"message": "Train line not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
