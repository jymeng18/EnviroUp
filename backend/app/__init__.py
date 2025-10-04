from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Frontend fetches data from backend

from app import routes

app.register_blueprint(routes.bp)