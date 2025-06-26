from flask import Flask, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # Enables cross-origin requests

# Load tender data once when the server starts
with open('tenders.json', 'r') as f:
    tenders_data = json.load(f)

# ✅ Route 1: Get all tenders
@app.route('/api/tenders', methods=['GET'])
def get_tenders():
    return jsonify(tenders_data), 200

# ✅ Route 2: Match tender title with keyword
@app.route('/api/match', methods=['GET'])
def match_tenders():
    keyword = request.args.get('seller', '').lower()
    
    if not keyword:
        return jsonify({"error": "Missing 'seller' query parameter."}), 400
    
    matching_tenders = [t for t in tenders_data if keyword in t['title'].lower()]
    
    if not matching_tenders:
        return jsonify({"message": "No tenders found matching the keyword."}), 404
    
    return jsonify(matching_tenders), 200

# ✅ Route 3: Summarize a tender description
@app.route('/api/summarize', methods=['POST'])
def summarize_tender():
    data = request.get_json()
    tender_text = data.get('text', '')
    
    if not tender_text:
        return jsonify({"error": "No tender text provided."}), 400
