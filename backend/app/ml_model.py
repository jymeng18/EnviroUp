# app/ml_model.py
import pandas as pd
import numpy as np
from math import radians, cos, sin, asin, sqrt
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import json

class WildfirePredictor:
    def __init__(self, csv_path="./data/viirs-jpss1_2024_Canada.csv"):
        self.csv_path = csv_path
        self.model = None
        self.lat_bins = None
        self.lon_bins = None
        self.le_conf = None
        self.df_fire = None
        
    def haversine_km(self, lat1, lon1, lat2, lon2):
        R = 6371.0
        lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = np.sin(dlat/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2
        return 2*R*np.arcsin(np.sqrt(a))
    
    def load_wildfire_data(self):
        df = pd.read_csv(self.csv_path)
        df = df[(df['latitude'].between(48, 60)) & (df['longitude'].between(-139, -114))]
        df = df[df['type'] == 0]
        df['acq_datetime'] = pd.to_datetime(df['acq_date'], utc=True)
        df = df[df['acq_datetime'].dt.month.isin([9, 10, 11])]
        df['SIZE_HA'] = df['frp']
        df['confidence'] = df['confidence'].fillna('n')
        df['ECOZ_NAME'] = 'Unknown'
        df['CAUSE'] = 'Unknown'
        return df
    
    def prepare_training_data(self, df, grid_res_km=1.0):
        km_per_deg_lat = 111.0
        lat_step = grid_res_km / km_per_deg_lat
        lon_step = grid_res_km / (111.0 * np.cos(radians(54)))
        lat_bins = np.arange(48, 60 + 1e-8, lat_step)
        lon_bins = np.arange(-139, -114 + 1e-8, lon_step)
        
        df['lat_bin'] = np.digitize(df['latitude'], lat_bins)
        df['lon_bin'] = np.digitize(df['longitude'], lon_bins)
        
        le_conf = LabelEncoder()
        df['confidence_encoded'] = le_conf.fit_transform(df['confidence'])
        
        positive_samples = df[['lat_bin', 'lon_bin', 'confidence_encoded', 'SIZE_HA']].copy()
        positive_samples['target'] = 1
        
        negative_samples = []
        n_negatives = len(positive_samples)
        for _ in range(n_negatives):
            lat = np.random.uniform(48, 60)
            lon = np.random.uniform(-139, -114)
            lat_bin = np.digitize(lat, lat_bins)
            lon_bin = np.digitize(lon, lon_bins)
            negative_samples.append({
                'lat_bin': lat_bin, 'lon_bin': lon_bin,
                'confidence_encoded': le_conf.transform(['n'])[0],
                'SIZE_HA': 0, 'target': 0
            })
        
        negative_df = pd.DataFrame(negative_samples)
        data = pd.concat([positive_samples, negative_df], ignore_index=True)
        data['SIZE_HA'] = np.log1p(data['SIZE_HA'])
        
        return data, lat_bins, lon_bins, le_conf
    
    def train(self):
        """Train the model - call this once when server starts"""
        print(" Loading wildfire data...")
        self.df_fire = self.load_wildfire_data()
        
        print(" Preparing training data...")
        data, self.lat_bins, self.lon_bins, self.le_conf = self.prepare_training_data(self.df_fire)
        
        print(" Training model...")
        X = data[['lat_bin', 'lon_bin', 'confidence_encoded', 'SIZE_HA']]
        y = data['target']
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X, y)
        
        print(" Model trained successfully!")
    
    def predict(self, center_lat, center_lon, search_radius_km=50, top_n=5):
        """Predict wildfire coordinates for a given location"""
        if self.model is None:
            raise ValueError("Model not trained! Call train() first.")
        
        grid_res_km = 1.0
        km_per_deg_lat = 111.0
        km_per_deg_lon = 111.0 * np.cos(radians(center_lat))
        lat_extent = search_radius_km / km_per_deg_lat
        lon_extent = search_radius_km / km_per_deg_lon
        
        lat_min, lat_max = center_lat - lat_extent, center_lat + lat_extent
        lon_min, lon_max = center_lon - lon_extent, center_lon + lon_extent
        
        df_local = self.df_fire[
            (self.df_fire['latitude'].between(lat_min, lat_max)) & 
            (self.df_fire['longitude'].between(lon_min, lon_max))
        ].copy()
        
        if not df_local.empty:
            distances = self.haversine_km(
                center_lat, center_lon, 
                df_local['latitude'].values, 
                df_local['longitude'].values
            )
            df_local = df_local[distances <= search_radius_km]
        
        lat_step = grid_res_km / km_per_deg_lat
        lon_step = grid_res_km / km_per_deg_lon
        pred_lat_bins = np.arange(lat_min, lat_max + 1e-8, lat_step)
        pred_lon_bins = np.arange(lon_min, lon_max + 1e-8, lon_step)
        
        grid_data = []
        for lat in pred_lat_bins:
            for lon in pred_lon_bins:
                # Filter out Vancouver urban/coast area
                if abs(lon - (-123.1207)) < 0.05 and abs(lat - 49.2827) < 0.05:
                    continue
                
                lat_bin = np.digitize(lat, self.lat_bins)
                lon_bin = np.digitize(lon, self.lon_bins)
                conf = df_local['confidence_encoded'].mean() if not df_local.empty else self.le_conf.transform(['n'])[0]
                grid_data.append({
                    'lat_bin': lat_bin, 'lon_bin': lon_bin,
                    'confidence_encoded': conf, 'SIZE_HA': 0,
                    'lat': lat, 'lon': lon
                })
        
        if not grid_data:
            return []
        
        pred_df = pd.DataFrame(grid_data)
        X_pred = pred_df[['lat_bin', 'lon_bin', 'confidence_encoded', 'SIZE_HA']]
        probs = self.model.predict_proba(X_pred)[:, 1]
        pred_df['prob'] = probs
        
        top_preds = pred_df.sort_values(by='prob', ascending=False).head(top_n)
        coords = [
            {
                "latitude": float(row['lat']), 
                "longitude": float(row['lon']),
                "probability": float(row['prob']),
                "name": f"Predicted Fire Zone {i+1}"
            } 
            for i, (_, row) in enumerate(top_preds.iterrows())
        ]
        
        # Sort by distance from center
        coords = sorted(
            coords, 
            key=lambda x: self.haversine_km(center_lat, center_lon, x['latitude'], x['longitude'])
        )
        
        return coords