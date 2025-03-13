import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Load Pixabay API key from environment variables
PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY")

@app.route("/fetch_pixabay_images", methods=["GET"])
def fetch_pixabay_images():
    query = request.args.get("query", "")
    per_page = 5  # Fetch more images and filter out non-landscape ones
    url = f"https://pixabay.com/api/?key={PIXABAY_API_KEY}&q={query}&image_type=photo&per_page={per_page}&safesearch=true"

    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        landscape_images = []

        # Filter for landscape images (width > height)
        for image in data.get("hits", []):
            if image["imageWidth"] > image["imageHeight"]:
                landscape_images.append({
                    "image_url": image["largeImageURL"]
                })

            # Stop collecting images after getting 2 landscape ones
            if len(landscape_images) == 2:
                break

        if landscape_images:
            return jsonify({"images": landscape_images})
        else:
            return jsonify({"error": "No landscape images found"}), 404

    else:
        return jsonify({"error": "Failed to fetch images", "response": response.text}), response.status_code

# 🚀 NEW: Health Check Route
@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "alive"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
