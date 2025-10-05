# EnviroUp - BC Wildfire Tracker with AI Fire Prevention Assistant

Raising awareness about environmental issues and promoting the UN Sustainable Development Goals.

## Features

- **Wildfire Prediction**: ML-powered wildfire location prediction using historical data
- **Fire Prevention Chatbot**: AI-powered assistant using Google Gemini for fire safety advice
- **Interactive Search**: Search for wildfires by location name
- **Real-time Data**: Get up-to-date wildfire information

## Setup Instructions

### Prerequisites
- Python 3.8+ installed
- Node.js 16+ installed
- Git installed

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/jymeng18/EnviroUp.git
   cd EnviroUp
   git checkout bc-wildfire-json
   ```

### Backend Setup

1. **Install Python dependencies**:
   ```bash
   # Install all required packages
   pip install -r requirements.txt
   
   # Or if using conda:
   conda install flask flask-cors pandas numpy scikit-learn -y
   conda install -c conda-forge google-generativeai python-dotenv -y
   ```

2. **Set up Gemini API Key**:
   - Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a `.env` file in the project root:
     ```bash
     echo "GOOGLE_API_KEY=your_actual_api_key_here" > .env
     ```
   - Replace `your_actual_api_key_here` with your real API key

3. **Run the backend**:
   ```bash
   cd backend
   GOOGLE_API_KEY=$(cat ../.env | grep API_KEY | cut -d'=' -f2) python run.py
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

## Troubleshooting

### Common Issues

1. **"ModuleNotFoundError: No module named 'flask_cors'"**:
   ```bash
   pip install flask-cors
   # or
   conda install flask-cors -y
   ```

2. **"ModuleNotFoundError: No module named 'google.generativeai'"**:
   ```bash
   pip install google-generativeai
   # or
   conda install -c conda-forge google-generativeai -y
   ```

3. **"Chatbot not available" error**:
   - Make sure your `.env` file exists and contains `GOOGLE_API_KEY=your_key_here`
   - Verify your API key is valid at [Google AI Studio](https://makersuite.google.com/app/apikey)

4. **Port already in use**:
   - Backend: Change port in `backend/run.py` (line 9)
   - Frontend: Vite will automatically find next available port

5. **CORS errors**:
   - Make sure backend is running on port 5001
   - Check that flask-cors is installed

### Environment Variables

The app supports both environment variable names:
- `GOOGLE_API_KEY` (preferred)
- `GEMINI_API_KEY` (fallback)

## Contributing

This project promotes environmental awareness and wildfire safety. Contributions are welcome!
