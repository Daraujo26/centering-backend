from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from app.coref_model import process_text
from app.centering import extract_centering

app = Flask(__name__)

# Enable CORS
CORS(app, resources={
    r"/center": {
        "origins": [
            <ENTER ORIGINS>
        ]
    }
})

@app.route('/<ROUTE>', methods=['POST'])
def center():
    data = request.json
    if not data or 'text' not in data:
        app.logger.warning('Invalid input received: %s', data)
        return jsonify({'error': 'Invalid input'}), 400

    text = data['text']
    app.logger.info('Input text received: %s', text)  

    try:
        grouped_sentences, clusters, tokens = process_text(text)  # Use grouped sentences
        results = extract_centering(grouped_sentences, clusters, tokens)  # Process grouped utterances

        app.logger.info('Processed results: %s', results) 
        return jsonify({'sentences': grouped_sentences, 'results': results})

    except Exception as e:
        app.logger.error('Error processing input: %s', e)
        return jsonify({'error': 'An error occurred during processing'}), 500
