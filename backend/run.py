import os
from dotenv import load_dotenv
from app import app

# Load environment variables from .env file
load_dotenv()

if __name__ == '__main__':
    app.run(debug=True, port=5001)
