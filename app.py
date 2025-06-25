from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# Load tender data
with open('tenders.json', 'r') as f:
    tenders_data = json.load(f)

# Endpoint to get all tenders
@app.route('/api/tenders', methods=['GET'])
def get_tenders():
    return jsonify(tenders_data), 200

# Endpoint to match tender title with keyword
@app.route('/api/match', methods=['GET'])
def match_tenders():
    # Extract the keyword from the query parameters
    keyword = request.args.get('seller', '').lower()
    
    if not keyword:
        return jsonify({"error": "Missing 'seller' query parameter."}), 400
    
    # Filter tenders based on keyword in title (case-insensitive)
    matching_tenders = [tender for tender in tenders_data if keyword in tender['title'].lower()]
    
    # If no tenders match the keyword
    if not matching_tenders:
        return jsonify({"message": "No tenders found matching the keyword."}), 404
    
    return jsonify(matching_tenders), 200

# Endpoint to summarize tender text (this will be a POST endpoint)
@app.route('/api/summarize', methods=['POST'])
def summarize_tender():
    data = request.get_json()
    tender_text = data.get('text', '')
    
    if not tender_text:
        return jsonify({"error": "No tender text provided."}), 400
    
    # Here, you would use GPT-4 API or another method to summarize the text.
    # For now, we simulate summarization by just returning the first 100 characters.
    summary = tender_text[:100] + "..." if len(tender_text) > 100 else tender_text
    
    return jsonify({"summary": summary}), 200

if __name__ == '__main__':
    app.run(debug=True)
