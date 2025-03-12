import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Load the API key from environment variables
PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY")

@app.route("/fetch_pixabay_images", methods=["GET"])
def fetch_pixabay_images():
    query = request.args.get("query", "sunset")  # Default query for testing
    # Construct the URL for Pixabay API
    url = f"https://pixabay.com/api/?key={PIXABAY_API_KEY}&q={query}&image_type=photo&per_page=3&safesearch=true"  # per_page set to 3

    # Log the constructed URL for debugging
    print("Constructed URL:", url)

    # Make the API request
    response = requests.get(url)
    print("Response Status Code:", response.status_code)  # Log status code
    print("Response Content:", response.text)  # Log the full response content

    # Check the response status and return the image data or error
    if response.status_code == 200:
        return jsonify(response.json())  # Return image data if successful
    else:
        return jsonify({"error": "Failed to fetch images", "response": response.text}), response.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
