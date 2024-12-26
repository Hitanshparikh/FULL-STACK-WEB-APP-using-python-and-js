from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure the app environment
app.config["ENV"] = os.getenv("FLASK_ENV", "production")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///friends.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Enable CORS
CORS(app)

# Serve static files from the "dist" folder under the "frontend" directory
frontend_folder = os.path.abspath(os.path.join(os.getcwd(), "..", "frontend"))
dist_folder = os.path.join(frontend_folder, "dist")

@app.route("/", defaults={"filename": ""})
@app.route("/<path:filename>")
def index(filename):
    if not filename:
        filename = "index.html"
    return send_from_directory(dist_folder, filename)

# Initialize the database only in development
with app.app_context():
    if app.config["ENV"] == "development":
        db.create_all()

# Import routes after initializing app
from routes import *

if __name__ == "__main__":
    app.run(debug=True)
