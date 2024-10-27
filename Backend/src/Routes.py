import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Define carbon emission values (in kilograms of CO2 per kilometer)
EMISSION_FACTORS = {
    "car": 0.12,          # kg of CO2 per km
    "carpool": 0.08,     # kg of CO2 per km (assuming 2 people)
    "bus": 0.03,         # kg of CO2 per km
    "train": 0.015,      # kg of CO2 per km
    "bicycle": 0,        # kg of CO2 per km (considered carbon neutral)
    "walking": 0,        # kg of CO2 per km (considered carbon neutral)
    "motorcycle": 0.1,   # kg of CO2 per km
    "electric_car": 0.05,# kg of CO2 per km
}

def calculate_emissions(distance, mode):
    """Calculate the carbon emissions based on the mode of transport."""
    emission_factor = EMISSION_FACTORS.get(mode, 0)
    emissions = distance * emission_factor
    return emissions

def fetch_distance(origin, destination):
    """Fetch distance from Google Maps API."""
    api_key = 'YOUR_GOOGLE_MAPS_API_KEY'
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins={origin}&destinations={destination}&key={api_key}"
    response = requests.get(url)
    data = response.json()
    
    if response.status_code == 200 and data['status'] == 'OK':
        return data['rows'][0]['elements'][0]['distance']['value'] / 1000  # Return in kilometers
    else:
        logging.error("Error fetching distance: %s", data.get('error_message', 'Unknown error'))
        return None

def calculate_and_return_emissions(current_location, destination, distance=None):
    """Calculate emissions and return as a list."""
    # Calculate distance if not provided
    if distance is None:
        distance = fetch_distance(current_location, destination)
        if distance is None:
            raise ValueError("Unable to fetch distance. Please enter the distance manually.")

    # Calculate emissions for different modes of transport
    emissions_data = []
    for mode in EMISSION_FACTORS.keys():
        emissions = calculate_emissions(distance, mode)
        emissions_data.append({
            "mode": mode,
            "emissions": emissions
        })

    return emissions_data