import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Load the API key from environment variables
PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY")

@app.route("/fetch_pixabay_images", methods=["GET"])
def fetch_pixabay_images():
    query = request.args.get("query", "")
    url = f"https://pixabay.com/api/?key={PIXABAY_API_KEY}&q={query}"
    
    response = requests.get(url)
    if response.status_code == 200:
        return jsonify(response.json())  # Return image data
    else:
        return jsonify({"error": "Failed to fetch images"}), response.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
