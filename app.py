from flask import Flask, request, jsonify
import base64
import os
import google.generativeai as genai
from PIL import Image
from io import BytesIO

app = Flask(__name__)

# Load your Gemini API key
genai.configure(api_key=os.getenv("AIzaSyAfLxYeFljz-Dv-bNY4CjOqEFw9jpMRviY"))

# Initialize Gemini Vision model
model = genai.GenerativeModel(model_name="gemini-1.5-flash")


@app.route("/analyze", methods=["POST"])
def analyze():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    image_bytes = file.read()

    # Decode and convert to PIL image
    image = Image.open(BytesIO(image_bytes))

    try:
        response = model.generate_content([
            "Is there a human face in this image? Respond only 'Yes' or 'No'.",
            image
        ])
        result = response.text.strip().lower()

        if "yes" in result:
            return jsonify({"result": "face"})
        else:
            return jsonify({"result": "no_face"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
