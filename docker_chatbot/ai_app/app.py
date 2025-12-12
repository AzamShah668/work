import os
import json
import requests
from flask import Flask, render_template, request, jsonify
import time

# --- Configuration ---
# The Flask app will look for templates in a 'templates' folder.
app = Flask(__name__)

# Model and API Endpoint Configuration
MODEL_NAME = "gemini-2.5-flash-preview-09-2025"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent"

# --- Flask Routes ---

@app.route('/')
def home():
    """Renders the main HTML template (assuming it's in templates/index.html)."""
    # NOTE: You must have a 'templates/index.html' file for this route to work.
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate_content():
    """Handles the AI generation request to the Gemini API."""
    
    # 1. API Key Check
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return jsonify({
            "error": "API Key Missing",
            "text": "The GEMINI_API_KEY environment variable is not set on the server."
        }), 500

    # 2. Get User Query
    try:
        data = request.get_json()
        user_query = data.get("query")
    except Exception:
        return jsonify({"error": "Invalid JSON payload"}), 400

    if not user_query:
        return jsonify({"error": "Missing query parameter"}), 400

    # 3. Construct Gemini API Payload
    # This system instruction guides the model's behavior.
    system_prompt = "You are a friendly, concise, and helpful AI assistant. Base your response on the most up-to-date information available."
    
    payload = {
        "contents": [{ "parts": [{ "text": user_query }] }],
        # Enable Google Search grounding for fresh, up-to-date answers
        "tools": [{ "google_search": {} }],
        "systemInstruction": { "parts": [{ "text": system_prompt }] },
    }

    headers = {
        'Content-Type': 'application/json'
    }
    
    # 4. Exponential Backoff/Retry Logic
    MAX_RETRIES = 5
    retry_delay = 1
    
    for attempt in range(MAX_RETRIES):
        try:
            # Append API key to the URL
            api_url_with_key = f"{GEMINI_API_URL}?key={api_key}"
            
            # Make the request to the Gemini API
            response = requests.post(api_url_with_key, headers=headers, json=payload, timeout=30)
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)

            result = response.json()
            
            # 5. Process the Response
            candidate = result.get('candidates', [{}])[0]
            
            # Extract generated text
            generated_text = candidate.get('content', {}).get('parts', [{}])[0].get('text', 'No text generated.')

            # Extract grounding sources (citations)
            sources = []
            grounding_metadata = candidate.get('groundingMetadata', {})
            if grounding_metadata and grounding_metadata.get('groundingAttributions'):
                sources = [
                    {
                        "uri": attr.get('web', {}).get('uri'),
                        "title": attr.get('web', {}).get('title'),
                    }
                    for attr in grounding_metadata['groundingAttributions']
                    if attr.get('web', {}).get('uri') and attr.get('web', {}).get('title')
                ]

            return jsonify({"text": generated_text, "sources": sources})

        except requests.exceptions.RequestException as e:
            if attempt < MAX_RETRIES - 1:
                # Retry logic: wait and increase delay exponentially
                time.sleep(retry_delay)
                retry_delay *= 2
            else:
                # After all retries fail, return the final error
                print(f"Failed to call Gemini API after {MAX_RETRIES} attempts. Error: {e}")
                return jsonify({"error": "Gemini API call failed", "text": "The AI service is unreachable or returned an error. Please check your API key and quotas."}), 500
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return jsonify({"error": "Internal server error", "text": "An unexpected error occurred."}), 500


if __name__ == '__main__':
    # Ensure you set the GEMINI_API_KEY environment variable before running!
    if not os.environ.get("GEMINI_API_KEY"):
        print("!!! WARNING: GEMINI_API_KEY is not set. The app will fail to generate content. !!!")
    
    # Run the application
    app.run(host='0.0.0.0', port=5000)
