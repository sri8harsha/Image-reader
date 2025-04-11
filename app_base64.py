from flask import Flask, request, jsonify
import openai
import requests
import base64
import os
from dotenv import load_dotenv

# Load the API key from .env file
load_dotenv()

app = Flask(__name__)

# Initialize OpenAI client securely
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/explain-image', methods=['POST'])
def explain_image():
    data = request.json
    image_url = data.get('image_url')
    user_prompt = data.get('prompt')

    if not image_url:
        return jsonify({"error": "No image URL provided"}), 400

    # Use default prompt if none is provided
    instruction = user_prompt or "Describe what is shown in this image in simple, clear terms."

    try:
        # Download the image
        image_response = requests.get(image_url)
        if image_response.status_code != 200:
            return jsonify({"error": "Failed to download image"}), 400

        # Convert image to base64
        image_base64 = base64.b64encode(image_response.content).decode('utf-8')
        image_data_url = f"data:image/png;base64,{image_base64}"

        # Call GPT-4o Vision
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": image_data_url}
                        },
                        {
                            "type": "text",
                            "text": instruction
                        }
                    ]
                }
            ],
            max_tokens=500
        )

        explanation = response.choices[0].message.content
        return jsonify({"explanation": explanation})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
