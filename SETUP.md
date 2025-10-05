# EnviroUp - BC Wildfire Tracker with AI Fire Prevention Assistant

Raising awareness about environmental issues and promoting the UN Sustainable Development Goals.

## Features

- **Wildfire Prediction**: ML-powered wildfire location prediction using historical data
- **Fire Prevention Chatbot**: AI-powered assistant using Google Gemini for fire safety advice
- **Interactive Search**: Search for wildfires by location name
- **Real-time Data**: Get up-to-date wildfire information

## Setup Instructions

### Backend Setup

1. **Install Python dependencies**:
   ```bash
   cd backend
   pip install -r ../requirements.txt
   ```

2. **Set up Gemini API Key**:
   - Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Set the environment variable:
     ```bash
     export GEMINI_API_KEY="your_api_key_here"
     ```
   - Or create a `.env` file in the project root:
     ```
     GEMINI_API_KEY=your_api_key_here
     ```

3. **Run the backend**:
   ```bash
   python run.py
   ```
   The backend will start on `http://localhost:5001`

### Frontend Setup

1. **Install Node.js dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Run the frontend**:
   ```bash
   npm run dev
   ```
   The frontend will start on `http://localhost:5173`

## Usage

1. **Wildfire Search**: Use the search box to find wildfires by location (e.g., "Vancouver", "BC", "Kamloops")
2. **Fire Prevention Chatbot**: Click the "🔥 Fire Safety Assistant" button in the bottom-right corner to:
   - Ask questions about fire prevention
   - Get advice on creating defensible space
   - Learn about emergency preparedness
   - Understand fire safety best practices

## API Endpoints

- `POST /api/search` - Search for wildfires by location
- `POST /api/predict-fires` - Predict fires by coordinates
- `GET /api/chatbot/welcome` - Get chatbot welcome message
- `POST /api/chatbot/chat` - Send message to fire prevention chatbot

## Technology Stack

- **Backend**: Flask, scikit-learn, pandas, Google Generative AI
- **Frontend**: React, Vite
- **AI**: Google Gemini Pro for fire prevention advice
- **ML**: Random Forest for wildfire prediction

## Contributing

This project promotes environmental awareness and wildfire safety. Contributions are welcome!
