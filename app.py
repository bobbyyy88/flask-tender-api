from flask import Flask, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Load tenders.json from the same folder
try:
    with open('tenders.json', 'r', encoding='utf-8') as f:
        tenders_data = json.load(f)
except Exception as e:
    tenders_data = []
    print("Error loading tenders.json:", e)

# Root route
@app.route('/')
def home():
    return "Tender API is live. Use /api/tenders to fetch data."

# Get all tenders
@app.route('/api/tenders', methods=['GET'])
def get_tenders():
    return jsonify(tenders_data), 200

# Match tenders by keyword
@app.route('/api/match', methods=['GET'])
def match_tenders():
    keyword = request.args.get('seller', '').lower()
    if not keyword:
        return jsonify({"error": "Missing 'seller' query parameter."}), 400

    matches = [t for t in tenders_data if keyword in t.get('title', '').lower()]
    if not matches:
        return jsonify({"message": "No tenders found matching the keyword."}), 404

    return jsonify(matches), 200

# Summarize tender text
@app.route('/api/summarize', methods=['POST'])
def summarize_tender():
    data = request.get_json()
    tender_text = data.get('text', '')
    
    if not tender_text:
        return jsonify({"error": "No tender text provided."}), 400
    
    summary = tender_text[:100] + "..." if len(tender_text) > 100 else tender_text
    return jsonify({"summary": summary}), 200

if __name__ == '__main__':
    app.run(debug=True)
