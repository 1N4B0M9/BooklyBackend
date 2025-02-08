from flask import Flask, request, jsonify
from google_vision_ocr import extract_text_with_google_vision
from ai_recommender import get_recommendations
from flask_cors import CORS
import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["https://yourfrontend.com", "http://localhost:3000"]}})  # Restrict to frontend domain
limiter = Limiter(get_remote_address, app=app, default_limits=["50 per hour"])


UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
@limiter.limit("10 per minute")  # 10 image uploads per minute per user
def upload_image():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    image_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(image_path)

    try:
        extracted_titles = extract_text_with_google_vision(image_path)
        # Optionally, further processing can be done here to isolate actual book titles.
        return jsonify({"extracted_titles": extracted_titles})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/recommend", methods=["POST"])
def recommend_books():
    try:
        data = request.get_json()
        titles = data.get("titles", [])
        user_preference = data.get("user_preference", "")

        if not user_preference:
            return jsonify({"error": "User preference is required"}), 400

        recommendations = get_recommendations(titles, user_preference)
        return jsonify({"recommendations": recommendations})
    
    except Exception as e:
        print(f"Error: {e}")  # Log error internally
        return jsonify({"error": "An unexpected error occurred"}), 500

@app.route("/")
def home():
    return jsonify({"message": "Bookshelf AI with Google Vision OCR is running!"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)