# 🔥 Firewatch

> **Raising awareness about environmental issues and promoting the UN Sustainable Development Goals**

A wildfire prediction and awareness platform inspired by the beautiful game **Firewatch** by Campo Santo. This project combines machine learning with interactive mapping to help users understand and track potential wildfire risks in their areas.

![Background Credit: Firewatch by Campo Santo](https://img.shields.io/badge/Background%20Image-Firewatch%20by%20Campo%20Santo-orange?style=for-the-badge)

## UN Sustainable Development Goals

This project directly supports:
- **Goal 13**: Climate Action
- **Goal 15**: Life on Land
- **Goal 11**: Sustainable Cities and Communities

## Features

- **Location-based Search** - Search for wildfire predictions by location
- **Interactive Maps** - Visualize predicted fire zones with Leaflet maps
- **ML Predictions** - Machine learning model trained on real wildfire data
- **Risk Assessment** - Severity and confidence scoring for each prediction
- **AI Chatbot** - Gemini AI-powered chatbot for environmental education and wildfire information
- **Beautiful UI** - Inspired by Firewatch's aesthetic

## Tech Stack

### Frontend
![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![Leaflet](https://img.shields.io/badge/Leaflet-199900?style=for-the-badge&logo=leaflet&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

### Backend
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)

### AI & Machine Learning
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)

## Quick Start

### Prerequisites
- **Node.js** (v16 or higher)
- **Python** (v3.8 or higher)
- **Git**

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/EnviroUp.git
   cd EnviroUp
   ```

2. **Set up the Backend**
   ```bash
   # Install Python dependencies
   pip install -r requirements.txt
   
   # Start the Flask server
   cd backend
   python run.py
   ```
   The backend will run on `http://localhost:5001`

3. **Set up the Frontend**
   ```bash
   # In a new terminal, navigate to frontend
   cd frontend
   
   # Install dependencies
   npm install
   
   # Start the development server
   npm run dev
   ```
   The frontend will run on `http://localhost:5173`

4. **Open your browser**
   Navigate to `http://localhost:5173` and start exploring!

## How to Use

1. **Search for a location** - Try searching for "Vancouver", "Kamloops", or "British Columbia"
2. **View predictions** - The map will display predicted fire zones with severity levels
3. **Explore details** - Click on markers to see confidence scores and raw data
4. **Learn about risks** - Each prediction includes severity assessment and confidence metrics
5. **Chat with AI** - Use the Gemini AI chatbot to ask questions about wildfires, environmental safety, and climate action


## AI Chatbot

The platform features a **Gemini AI-powered chatbot** that provides:

- **Environmental Education** - Learn about climate change, wildfires, and environmental safety
- **Wildfire Information** - Get answers about fire prevention, safety tips, and emergency procedures
- **Interactive Learning** - Ask questions about sustainable development goals and environmental awareness
- **Real-time Assistance** - Get instant responses to your environmental and safety questions

## Machine Learning

The project uses a **Random Forest Classifier** trained on real wildfire data from VIIRS (Visible Infrared Imaging Radiometer Suite) satellites. The model predicts wildfire probability based on:

- Geographic coordinates
- Historical fire patterns
- Environmental factors
- Seasonal data

## Design Inspiration

The visual design and atmosphere are inspired by **Firewatch**, the critically acclaimed indie game by Campo Santo. The game's beautiful art style and environmental storytelling served as the primary inspiration for this project's aesthetic.

*Background imagery credit: Firewatch by Campo Santo*


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credit

- **Campo Santo** for the beautiful Firewatch game that inspired this project
- **NASA** for the VIIRS wildfire data
- **UN Sustainable Development Goals** for the environmental mission
- **OpenStreetMap** for map tiles

---

**Made with ❤️ for environmental awareness and climate action*
