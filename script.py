import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Load the API key from environment variables
PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY")

# Print the API key to check if it's loaded correctly
print("Pixabay API Key:", PIXABAY_API_KEY)  # Debug print statement

@app.route("/fetch_pixabay_images", methods=["GET"])
def fetch_pixabay_images():
    query = request.args.get("query", "")
    # For testing, you can hardcode the query value if needed
    # query = "sunset"  # Uncomment for testing without URL parameters

    url = f"https://pixabay.com/api/?key={PIXABAY_API_KEY}&q={query}&image_type=photo&per_page=1&safesearch=true"

    print("Constructed URL:", url)  # Debug print statement to check the full URL

    response = requests.get(url)
    print("Response Status Code:", response.status_code)  # Debug response status
    print("Response Content:", response.text)  # Debug the content of the response

    if response.status_code == 200:
        return jsonify(response.json())  # Return image data
    else:
        return jsonify({"error": "Failed to fetch images", "response": response.text}), response.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
