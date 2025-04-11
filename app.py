from flask import Flask, request, jsonify
import openai
import requests
import base64
import os
from dotenv import load_dotenv

load_dotenv()  # Loads your .env file automatically

# Initialize Flask app
app = Flask(__name__)

# Set up OpenAI client with your API key
import os
client = openai.OpenAI(api_key=os.getenv("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"))

@app.route('/explain-diagram', methods=['POST'])
def explain_diagram():
    data = request.json
    image_url = data.get('image_url')

    if not image_url:
        return jsonify({"error": "No image URL provided"}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": image_url}
                        },
                        {
                            "type": "text",
                            "text": "Explain this educational diagram clearly and concisely for a student."
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
    app.run(debug=True, port=5000)
