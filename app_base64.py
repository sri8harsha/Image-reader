from flask import Flask, request, jsonify
import openai
import requests
import base64
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/explain-image', methods=['POST'])  # ✅ This must be exact
def explain_image():
    data = request.json
    image_url = data.get('image_url')
    user_prompt = data.get('prompt')

    if not image_url:
        return jsonify({"error": "No image URL provided"}), 400

instruction = user_prompt or "You are an educational assistant. Describe this labeled educational diagram in detail. Explain each visible part, name all components if text is readable, and summarize how these parts are connected. Make sure to reference labels or symbols seen in the image directly."

    try:
        image_response = requests.get(image_url)
        if image_response.status_code != 200:
            return jsonify({"error": "Failed to download image"}), 400

        image_base64 = base64.b64encode(image_response.content).decode('utf-8')
        image_data_url = f"data:image/png;base64,{image_base64}"

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": image_data_url}},
                        {"type": "text", "text": instruction}
                    ]
                }
            ],
            max_tokens=500
        )

        explanation = response.choices[0].message.content
        return jsonify({ "result": { "explanation": explanation } })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
