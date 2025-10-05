import React, { useEffect, useRef, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import L from 'leaflet';
import { Loader } from '@googlemaps/js-api-loader';
import 'leaflet/dist/leaflet.css';
import './App.css';


// Fix for default markers in react-leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Custom fire icon for Leaflet
const fireIcon = new L.Icon({
  // Use image from the public folder. Put `icon.png` in `frontend/public/` (served at /icon.png).
  iconUrl: '/icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

// Component to update map center when fires change
function MapUpdater({ fires, center }) {
  const map = useMap();
  
  useEffect(() => {
    if (fires.length > 0) {
      const bounds = L.latLngBounds(fires.map(fire => [fire.latitude, fire.longitude]));
      map.fitBounds(bounds, { padding: [20, 20] });
    } else if (center) {
      map.setView([center.lat, center.lon], 8);
    }
  }, [fires, center, map]);
  
  return null;
}

// Leaflet Map Component
function LeafletMap({ fires, center }) {
  return (
    <div style={{ height: '500px', width: '100%' }}>
      <MapContainer
        center={center ? [center.lat, center.lon] : [49.2827, -123.1207]}
        zoom={8}
        style={{ height: '100%', width: '100%' }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {fires.map((fire, index) => (
          <Marker
            key={index}
            position={[fire.latitude, fire.longitude]}
            icon={fireIcon}
          >
            <Popup>
              <div>
                <h3>{fire.name}</h3>
                <p><strong>Coordinates:</strong> {fire.latitude.toFixed(4)}, {fire.longitude.toFixed(4)}</p>
                <p><strong>Severity:</strong> {fire.severity}</p>
                {fire.confidence && <p><strong>Confidence:</strong> {fire.confidence.toFixed(2)}</p>}
              </div>
            </Popup>
          </Marker>
        ))}
        <MapUpdater fires={fires} center={center} />
      </MapContainer>
    </div>
  );
}



// Main Map Component 
export default function MapComponent({ fires = [], center = null }) {
  const [mapType, setMapType] = useState('leaflet'); // 'leaflet' or 'google'

  return (
    <div className="map-container">
      <div className="map-controls">
        <h3>Wildfire Map</h3>
        <div className="map-toggle">
          <button
            className={mapType === 'leaflet' ? 'active' : ''}
            onClick={() => setMapType('leaflet')}
          >
            Leaflet Map
          </button>
        </div>
      </div>
      
      <div className="map-wrapper">
        {mapType === 'leaflet' ? (
          <LeafletMap fires={fires} center={center} />
        ) : (
          <GoogleMap fires={fires} center={center} />
        )}
      </div>
      
      
    </div>
  );
}
