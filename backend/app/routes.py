# app/routes.py
from flask import Blueprint, jsonify, request
from app.ml_model import WildfirePredictor

bp = Blueprint('routes', __name__)

# Initialize and train model once when server starts
print("Initializing wildfire prediction model...")
predictor = WildfirePredictor(csv_path="./data/viirs-jpss1_2024_Canada.csv")
predictor.train()

# Dummy data for locations without ML predictions
WILDFIRE_DATA = {
    'british columbia': [
        {'latitude': 49.2827, 'longitude': -123.1207, 'name': 'Vancouver Fire', 'severity': 'moderate'},
        {'latitude': 50.6745, 'longitude': -120.3273, 'name': 'Kamloops Fire', 'severity': 'high'},
    ]
}

# Location name to coordinates mapping
LOCATION_COORDS = {
    'bc': (54.0, -125.0),  # Center of BC
    'vancouver': (49.2827, -123.1207),
    'kamloops': (50.6745, -120.3273),
    'prince george': (53.9171, -122.7497),
}

@bp.route('/api/search', methods=['POST'])
def search_fires():
    """
    Search for fires by location name using ML predictions
    """
    data = request.get_json()
    location = data.get('q', '').lower().strip()
    
    if not location:
        return jsonify({'error': 'Location query required'}), 400
    
    # Try to get coordinates for the location
    coords = None
    for loc_name, loc_coords in LOCATION_COORDS.items():
        if location in loc_name or loc_name in location:
            coords = loc_coords
            break
    
    if not coords:
        return jsonify({
            'fires': [],
            'message': f'Location "{location}" not recognized. Try: British Columbia, Vancouver, Kamloops'
        }), 404
    
    try:
        # Get ML predictions
        predicted_fires = predictor.predict(
            center_lat=coords[0],
            center_lon=coords[1],
            search_radius_km=100,
            top_n=10
        )
        
        return jsonify({
            'fires': predicted_fires,
            'count': len(predicted_fires),
            'location': location,
            'center': {'lat': coords[0], 'lon': coords[1]},
            'source': 'ML Prediction'
        })
        
    except Exception as e:
        print(f"ML prediction error: {e}")
        # Fallback to dummy data
        dummy_fires = WILDFIRE_DATA.get(location, [])
        return jsonify({
            'fires': dummy_fires,
            'count': len(dummy_fires),
            'location': location,
            'source': 'Fallback Data'
        })

@bp.route('/api/predict-fires', methods=['POST'])
def predict_fires_by_coords():
    """
    Predict fires by exact coordinates (lat/lon)
    """
    data = request.get_json()
    lat = data.get('lat')
    lon = data.get('lon')
    radius = data.get('radius', 50)
    
    if lat is None or lon is None:
        return jsonify({'error': 'lat and lon required'}), 400
    
    try:
        predicted_fires = predictor.predict(
            center_lat=float(lat),
            center_lon=float(lon),
            search_radius_km=radius,
            top_n=10
        )
        
        return jsonify({
            'fires': predicted_fires,
            'count': len(predicted_fires),
            'center': {'lat': lat, 'lon': lon}
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500