from flask import Flask, request, jsonify
from Backend.src.HomeEmissionsTracker import main as calculate_co2  # Adjust the import as necessary
from Backend.src.Routes import calculate_and_return_emissions  # Adjust the import as necessary

app = Flask(__name__)

@app.route('/calculate_co2', methods=['POST'])
def calculate_co2_endpoint():
    data = request.json
    zipcode = data.get('zipcode')
    electricity_units = data.get('electricity_units')
    gas_units = data.get('gas_units')
    peopleInHome = data.get('peopleInHome')

    try:
        result = calculate_co2(zipcode, electricity_units, gas_units, peopleInHome)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/calculate_transport_emissions', methods=['POST'])
def calculate_transport_emissions_endpoint():
    data = request.json
    current_location = data.get('current_location')
    destination = data.get('destination')
    distance = data.get('distance', None)

    try:
        result = calculate_and_return_emissions(current_location, destination, distance)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)