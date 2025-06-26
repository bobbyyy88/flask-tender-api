from flask import Flask, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Load tender data from file
with open('tenders.json', 'r') as f:
    tenders_data = json.load(f)

# ✅ Route: Get all tenders
@app.route('/api/tenders', methods=['GET'])
def get_tenders():
    return jsonify(tenders_data), 200

# ✅ Route: Match tenders with seller keyword
@app.route('/api/match', methods=['GET'])
def match_tenders():
    keyword = request.args.get('seller', '').lower()
    if not keyword:
        return jsonify({"error": "Missing 'seller' query parameter."}), 400

    matching = [t for t in tenders_data if keyword in t['title'].lower()]
    return jsonify(matching if matching else {"message": "No tenders found"}), 200

# ✅ Route: Summarize tender
@app.route('/api/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    text = data.get('text', '')
    if not text:
        return jsonify({"error": "Missing 'text' field"}), 400

    summary = text[:100] + '...' if len(text) > 100 else text
    return jsonify({"summary": summary}), 200

# ✅ Home route (optional)
@app.route('/')
def home():
    return "Tender API is running. Try /api/tenders"

if __name__ == '__main__':
    app.run(debug=True)
