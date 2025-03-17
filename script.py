import os
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS  # 🔥 Import CORS

app = Flask(__name__)
CORS(app)  # 🔥 Enable CORS for all routes

# Load Pixabay API key from environment variables
PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY")

@app.route("/fetch_pixabay_images", methods=["GET"])
def fetch_pixabay_images():
    query = request.args.get("query", "")
    url = f"https://pixabay.com/api/?key={PIXABAY_API_KEY}&q={query}&image_type=photo&per_page=5&safesearch=true"

    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        landscape_images = [
            img["webformatURL"] for img in data.get("hits", [])
            if img["imageWidth"] > img["imageHeight"]  # Ensure landscape format
        ]
        return jsonify({"images": landscape_images[:6]})  # Return first 2 images
    else:
        return jsonify({"error": "Failed to fetch images"}), response.status_code

# 🚀 NEW: Health Check Route
@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "alive"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
