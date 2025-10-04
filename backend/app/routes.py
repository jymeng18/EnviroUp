from flask import Blueprint, jsonify, request

bp = Blueprint('routes', __name__)

# Dummy wildfire data
WILDFIRE_DATA = {
    'bc': [
        {'latitude': 49.2827, 'longitude': -123.1207, 'name': 'Vancouver Fire', 'severity': 'moderate'},
        {'latitude': 50.6745, 'longitude': -120.3273, 'name': 'Kamloops Fire', 'severity': 'high'},
        {'latitude': 53.9171, 'longitude': -122.7497, 'name': 'Prince George Fire', 'severity': 'low'},
    ],
    'california': [
        {'latitude': 34.0522, 'longitude': -118.2437, 'name': 'Los Angeles Fire', 'severity': 'high'},
        {'latitude': 37.7749, 'longitude': -122.4194, 'name': 'San Francisco Fire', 'severity': 'moderate'},
    ],
    'alberta': [
        {'latitude': 51.0447, 'longitude': -114.0719, 'name': 'Calgary Fire', 'severity': 'moderate'},
        {'latitude': 53.5461, 'longitude': -113.4938, 'name': 'Edmonton Fire', 'severity': 'high'},
    ]
}

@bp.route('/api/search', methods=['POST'])
def search_fires():
    """
    Search for fires by location name
    Frontend sends over user input: "British Columbia"
    Backend must return: list of wildfire coordinates
    """
    data = request.get_json()
    
    # Extract the query field from our frontend
    location = data.get('q', '').lower().strip()
    
    if not location:
        return jsonify({'error': 'Location query required'}), 400
    
    # Search for matching fires
    matching_fires = []
    matched_region = None
    
    for region, fires in WILDFIRE_DATA.items():
        if location in region or region in location:
            matching_fires = fires
            matched_region = region
            break
    
    if not matching_fires:
        return jsonify({
            'fires': [],
            'count': 0,
            'message': f'No wildfires found for "{location}"'
        }), 404
    
    return jsonify({
        'fires': matching_fires,
        'count': len(matching_fires),
        'region': matched_region,
        'searched_location': location
    })