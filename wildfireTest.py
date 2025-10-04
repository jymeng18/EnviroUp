# wildfire_predict_bc_json.py
import pandas as pd
import numpy as np
from math import radians, cos, sin, asin, sqrt
from scipy.ndimage import gaussian_filter
from scipy import ndimage
from datetime import datetime, timedelta, timezone
import random
import json

# ------------------ Step 1: BC inland centers ------------------
BC_CENTERS = [
    (49.2827, -123.1207),  # Vancouver
    (48.4284, -123.3656),  # Victoria
    (49.8951, -119.4940),  # Kelowna
    (50.1163, -120.3470),  # Kamloops
    (53.9171, -122.7497),  # Prince George
    (52.9840, -122.4930),  # Quesnel
    (52.1292, -122.1409),  # Williams Lake
    (49.1666, -122.9050),  # Hope
    (49.4936, -117.2942),  # Nelson
    (49.0955, -117.7140),  # Trail
]

def jitter_point(lat, lon, max_km=12):
    import math
    km_to_deg_lat = 1.0 / 111.0
    km_to_deg_lon = 1.0 / (111.0 * math.cos(math.radians(lat)))
    r = max_km * (random.random() ** 0.5)
    theta = random.random() * 2 * np.pi
    dlat = r * km_to_deg_lat * np.cos(theta)
    dlon = r * km_to_deg_lon * np.sin(theta)
    return lat + dlat, lon + dlon

def generate_hotspots(total=500, days_back=7):
    rows = []
    now = datetime.now(timezone.utc)
    for _ in range(total):
        clat, clon = random.choice(BC_CENTERS)
        lat, lon = jitter_point(clat, clon)
        acq_dt = now - timedelta(days=random.randint(0, days_back-1))
        acq_date_str = acq_dt.strftime("%Y-%m-%d")
        confidence = random.randint(60, 100)
        rows.append({"latitude": lat, "longitude": lon, "acq_date": acq_date_str, "confidence": confidence})
    df = pd.DataFrame(rows)
    return df

# ------------------ Step 2: Haversine distance ------------------
def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    phi1, phi2 = radians(lat1), radians(lat2)
    dphi = radians(lat2 - lat1)
    dlambda = radians(lon2 - lon1)
    a = sin(dphi/2)**2 + cos(phi1)*cos(phi2)*sin(dlambda/2)**2
    return 2*R*asin(sqrt(a))

# ------------------ Step 3: Wildfire prediction (JSON output) ------------------
def predict_wildfire_coords_json(firms_df, center_lat, center_lon,
                                 search_radius_km=50, grid_res_km=1.0,
                                 time_decay_days=3, top_n=5):
    firms_df = firms_df.copy()
    firms_df['dist_km'] = firms_df.apply(lambda r: haversine_km(center_lat, center_lon, r['latitude'], r['longitude']), axis=1)
    df_local = firms_df[firms_df['dist_km'] <= search_radius_km].copy()
    now = pd.Timestamp.now(tz="UTC")
    df_local['acq_datetime'] = pd.to_datetime(df_local['acq_date'], utc=True)
    df_local['age_days'] = (now - df_local['acq_datetime']).dt.total_seconds() / (3600*24)
    df_local['time_w'] = np.exp(-df_local['age_days']/max(1.0, time_decay_days))
    df_local['weight'] = df_local['time_w'] * df_local['confidence']/100.0

    # Create grid for KDE
    km_per_deg_lat = 111.0
    km_per_deg_lon = 111.0 * cos(radians(center_lat))
    lat_extent = search_radius_km / km_per_deg_lat
    lon_extent = search_radius_km / km_per_deg_lon
    lat_step = grid_res_km / km_per_deg_lat
    lon_step = grid_res_km / km_per_deg_lon
    lat_bins = np.arange(center_lat - lat_extent, center_lat + lat_extent + 1e-8, lat_step)
    lon_bins = np.arange(center_lon - lon_extent, center_lon + lon_extent + 1e-8, lon_step)
    grid = np.zeros((len(lat_bins), len(lon_bins)), dtype=float)

    for _, r in df_local.iterrows():
        i = int(round((r['latitude'] - lat_bins[0]) / lat_step))
        j = int(round((r['longitude'] - lon_bins[0]) / lon_step))
        if 0 <= i < grid.shape[0] and 0 <= j < grid.shape[1]:
            grid[i,j] += float(r['weight'])

    grid_smooth = gaussian_filter(grid, sigma=2.0)
    neighborhood = ndimage.generate_binary_structure(2,2)
    local_max = (ndimage.maximum_filter(grid_smooth, footprint=neighborhood)==grid_smooth) & (grid_smooth>0)
    peaks = np.argwhere(local_max)

    coords = []
    for i,j in peaks:
        lat = float(lat_bins[i])
        lon = float(lon_bins[j])
        coords.append({"lat": lat, "lon": lon})

    # Return top_n closest peaks to input coordinate
    coords = sorted(coords, key=lambda x: haversine_km(center_lat, center_lon, x['lat'], x['lon']))[:top_n]
    return json.dumps(coords, indent=2)

# ------------------ Step 4: Main test ------------------
if __name__ == "__main__":
    df_fire = generate_hotspots(total=500)
    test_lat, test_lon = 49.2827, -123.1207  # Vancouver
    print(f"Test coordinates: ({test_lat}, {test_lon})")

    json_output = predict_wildfire_coords_json(df_fire, test_lat, test_lon, top_n=10)
    print("Predicted wildfire coordinates (JSON):")
    print(json_output)
