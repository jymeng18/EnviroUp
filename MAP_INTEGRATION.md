# Map Integration Guide

## Overview
The EnviroUp application now includes interactive maps to visualize wildfire locations returned from the backend. The map component supports both Leaflet (OpenStreetMap) and Google Maps.

## Features

### Leaflet Map (Default)
- **Free and open source** - No API key required
- Uses OpenStreetMap tiles
- Custom red fire markers
- Popup information for each fire location
- Automatic bounds fitting to show all fires

### Google Maps
- **Requires API key** - More detailed satellite/terrain views
- Professional mapping data
- Custom fire markers with red icons
- Info windows with fire details
- Automatic bounds fitting

## Setup

### For Leaflet (Works out of the box)
No additional setup required. The Leaflet map will work immediately.

### For Google Maps
1. Get a Google Maps API key from [Google Cloud Console](https://console.cloud.google.com/google/maps-apis)
2. Create a `.env` file in the `frontend` directory
3. Add your API key:
   ```
   REACT_APP_GOOGLE_MAPS_API_KEY=your_api_key_here
   ```
4. Restart the development server

## Usage

1. Search for a location (e.g., "Vancouver", "British Columbia", "Kamloops")
2. The backend will return wildfire coordinates
3. The map will automatically display all fire locations
4. Use the toggle buttons to switch between Leaflet and Google Maps
5. Click on markers to see detailed fire information

## Map Controls

- **Toggle Buttons**: Switch between Leaflet and Google Maps
- **Zoom**: Use mouse wheel or zoom controls
- **Pan**: Click and drag to move around the map
- **Markers**: Click on red fire markers to see details

## Data Format

The map expects fire data in this format:
```javascript
{
  fires: [
    {
      latitude: 49.2827,
      longitude: -123.1207,
      name: "Fire Name",
      severity: "high|moderate|low",
      confidence: 0.85 // optional
    }
  ],
  center: {
    lat: 49.2827,
    lon: -123.1207
  }
}
```

## Troubleshooting

### Google Maps not loading
- Check that your API key is correctly set in the `.env` file
- Ensure the API key has the necessary permissions (Maps JavaScript API)
- Check the browser console for error messages

### Leaflet markers not showing
- Check that the fire data includes valid latitude and longitude values
- Ensure the coordinates are numbers, not strings

### Map not fitting to bounds
- Verify that the fires array is not empty
- Check that all fire objects have valid coordinates
