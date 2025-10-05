import pandas as pd
import numpy as np
from math import radians, cos, sin, asin, sqrt
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from datetime import datetime, timezone
import json

# ------------------ Step 1: Haversine distance (vectorized) ------------------
def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2
    return 2*R*np.arcsin(np.sqrt(a))

# ------------------ Step 2: Load and preprocess wildfire data ------------------
def load_wildfire_data(csv_path="./data/viirs-jpss1_2024_Canada.csv"):
    df = pd.read_csv(csv_path)
    # Filter for British Columbia (approximate bounds: lat 48-60, lon -139 to -114)
    df = df[(df['latitude'].between(48, 60)) & (df['longitude'].between(-139, -114))]
    # Filter for presumed vegetation fires (type == 0)
    df = df[df['type'] == 0]
    # Filter for fall season (September–November)
    df['acq_datetime'] = pd.to_datetime(df['acq_date'], utc=True)
    df = df[df['acq_datetime'].dt.month.isin([9, 10, 11])]
    # Use 'frp' as proxy for fire size/intensity
    df['SIZE_HA'] = df['frp']  # Assuming frp correlates with size
    # Handle confidence column
    df['confidence'] = df['confidence'].fillna('n')  # Default to nominal
    # No ECOZ_NAME or CAUSE, so add placeholders
    df['ECOZ_NAME'] = 'Unknown'
    df['CAUSE'] = 'Unknown'
    return df

# ------------------ Step 3: Prepare training data ------------------
def prepare_training_data(df, grid_res_km=1.0):
    # Create a grid covering BC (approximate bounds: 48–60N, -139–-114W)
    km_per_deg_lat = 111.0
    lat_step = grid_res_km / km_per_deg_lat
    lon_step = grid_res_km / (111.0 * np.cos(radians(54)))  # Approx middle latitude
    lat_bins = np.arange(48, 60 + 1e-8, lat_step)
    lon_bins = np.arange(-139, -114 + 1e-8, lon_step)
    
    # Assign wildfires to grid cells
    df['lat_bin'] = np.digitize(df['latitude'], lat_bins)
    df['lon_bin'] = np.digitize(df['longitude'], lon_bins)
    
    # Encode confidence column
    le_conf = LabelEncoder()
    df['confidence_encoded'] = le_conf.fit_transform(df['confidence'])
    
    # Create positive samples
    positive_samples = df[['lat_bin', 'lon_bin', 'confidence_encoded', 'SIZE_HA']].copy()
    positive_samples['target'] = 1
    
    # Create negative samples
    negative_samples = []
    n_negatives = len(positive_samples)
    for _ in range(n_negatives):
        lat = np.random.uniform(48, 60)
        lon = np.random.uniform(-139, -114)
        lat_bin = np.digitize(lat, lat_bins)
        lon_bin = np.digitize(lon, lon_bins)
        negative_samples.append({
            'lat_bin': lat_bin, 'lon_bin': lon_bin,
            'confidence_encoded': le_conf.transform(['n'])[0],  # Default to nominal
            'SIZE_HA': 0, 'target': 0
        })
    
    # Combine samples
    negative_df = pd.DataFrame(negative_samples)
    data = pd.concat([positive_samples, negative_df], ignore_index=True)
    
    # Log-transform SIZE_HA
    data['SIZE_HA'] = np.log1p(data['SIZE_HA'])
    
    return data, lat_bins, lon_bins, le_conf

# ------------------ Step 4: Train ML model ------------------
def train_model(data):
    X = data[['lat_bin', 'lon_bin', 'confidence_encoded', 'SIZE_HA']]
    y = data['target']
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

# ------------------ Step 5: Predict wildfire coords ------------------
def predict_wildfire_coords_json(df, center_lat, center_lon, model, lat_bins, lon_bins, le_conf,
                                 search_radius_km=50, grid_res_km=1.0, top_n=5):
    # Pre-filter with bounding box
    km_per_deg_lat = 111.0
    km_per_deg_lon = 111.0 * np.cos(radians(center_lat))
    lat_extent = search_radius_km / km_per_deg_lat
    lon_extent = search_radius_km / km_per_deg_lon
    lat_min, lat_max = center_lat - lat_extent, center_lat + lat_extent
    lon_min, lon_max = center_lon - lon_extent, center_lon + lon_extent
    df_local = df[(df['latitude'].between(lat_min, lat_max)) & 
                  (df['longitude'].between(lon_min, lon_max))].copy()
    
    # Vectorized Haversine filter
    if not df_local.empty:
        distances = haversine_km(center_lat, center_lon, df_local['latitude'].values, df_local['longitude'].values)
        df_local = df_local[distances <= search_radius_km]
    
    # Debug: Check number of wildfires in radius
    print(f"Number of fall wildfires within {search_radius_km} km of ({center_lat}, {center_lon}): {len(df_local)}")
    
    # Create prediction grid
    lat_step = grid_res_km / km_per_deg_lat
    lon_step = grid_res_km / km_per_deg_lon
    pred_lat_bins = np.arange(center_lat - lat_extent, center_lat + lat_extent + 1e-8, lat_step)
    pred_lon_bins = np.arange(center_lon - lon_extent, center_lon + lon_extent + 1e-8, lon_step)
    
    grid_data = []
    for i, lat in enumerate(pred_lat_bins):
        for j, lon in enumerate(pred_lon_bins):
            # Simplified land cover filter: exclude ocean/urban (latitudes near coast or known urban areas)
            if abs(lon - (-123.1207)) < 0.05 and abs(lat - 49.2827) < 0.05:  # Near Vancouver urban/coast
                continue
            lat_bin = np.digitize(lat, lat_bins)
            lon_bin = np.digitize(lon, lon_bins)
            conf = df_local['confidence_encoded'].mean() if not df_local.empty else le_conf.transform(['n'])[0]
            grid_data.append({
                'lat_bin': lat_bin, 'lon_bin': lon_bin,
                'confidence_encoded': conf, 'SIZE_HA': 0,
                'lat': lat, 'lon': lon
            })
    
    pred_df = pd.DataFrame(grid_data)
    if pred_df.empty:
        print("No grid points generated after land cover filtering. Returning empty predictions.")
        return json.dumps([], indent=2)
    
    # Predict probabilities
    X_pred = pred_df[['lat_bin', 'lon_bin', 'confidence_encoded', 'SIZE_HA']]
    probs = model.predict_proba(X_pred)[:, 1]
    pred_df['prob'] = probs
    
    # Select top N locations
    top_preds = pred_df.sort_values(by='prob', ascending=False).head(top_n)
    coords = [{"lat": float(row['lat']), "lon": float(row['lon'])} for _, row in top_preds.iterrows()]
    coords = sorted(coords, key=lambda x: haversine_km(center_lat, center_lon, x['lat'], x['lon']))
    return json.dumps(coords, indent=2)

# ------------------ Step 6: Main test ------------------
if __name__ == "__main__":
    # Load and prepare data
    df_fire = load_wildfire_data()
    data, lat_bins, lon_bins, le_conf = prepare_training_data(df_fire)
    
    # Train model
    model = train_model(data)
    
    # Test coordinates (Vancouver)
    test_lat, test_lon = 49.2827, -123.1207
    print(f"Test coordinates: ({test_lat}, {test_lon})")
    
    # Predict
    json_output = predict_wildfire_coords_json(df_fire, test_lat, test_lon, model, lat_bins, lon_bins, le_conf, top_n=10)
    print("Predicted wildfire coordinates (JSON):")
    print(json_output)