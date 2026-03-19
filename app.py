from flask import Flask, render_template, request, jsonify
import os
from feature_extractor import extract_features
from compare_essay import calculate_similarity_score
import statistics
import json
from file_reader import read_file

app = Flask(__name__)

# Store uploaded baseline essays temporarily
baseline_essays = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_baseline', methods=['POST'])
def add_baseline():
    """Add a baseline essay."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Read the file using our file reader
    text, error = read_file(file)
    
    # DEBUG: Print what we extracted
    print(f"DEBUG: Read {file.filename} - {len(text)} characters, first 100 chars: {text[:100]}")
    
    if error:
        return jsonify({'error': error}), 400
    
    if not text.strip():
        return jsonify({'error': 'File appears to be empty'}), 400
    
    baseline_essays.append(text)
    
    return jsonify({
        'success': True,
        'count': len(baseline_essays),
        'filename': file.filename,
        'message': f'Added baseline essay {len(baseline_essays)} ({file.filename})'
    })

@app.route('/clear_baselines', methods=['POST'])
def clear_baselines():
    """Clear all baseline essays."""
    baseline_essays.clear()
    return jsonify({'success': True, 'message': 'Baselines cleared'})

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze a test essay against baselines."""
    if len(baseline_essays) < 2:
        return jsonify({'error': 'Need at least 2 baseline essays'}), 400
    
    if 'file' not in request.files:
        return jsonify({'error': 'No test file uploaded'}), 400
    
    file = request.files['file']
    
    # Read the file using our file reader
    test_text, error = read_file(file)
    
    if error:
        return jsonify({'error': error}), 400
    
    if not test_text.strip():
        return jsonify({'error': 'File appears to be empty'}), 400
    
    # Create profile from baselines
    baseline_features = [extract_features(essay) for essay in baseline_essays]
    
    # Calculate mean and stdev for each feature
    feature_names = baseline_features[0].keys()
    profile = {}
    
    for feature_name in feature_names:
        values = [essay[feature_name] for essay in baseline_features]
        profile[feature_name] = {
            'mean': statistics.mean(values),
            'stdev': statistics.stdev(values) if len(values) > 1 else 0
        }
    
    # Create profile data structure
    profile_data = {
        'student_name': 'Test',
        'profile': profile
    }
    
    # Compare test essay
    score, details = calculate_similarity_score(test_text, profile_data)
    
    # Sort features by z-score (most different first)
    details_sorted = sorted(details, key=lambda x: x['z_score'], reverse=True)
    
    return jsonify({
        'similarity_score': round(score, 1),
        'num_baselines': len(baseline_essays),
        'features': details_sorted[:10]  # Top 10 most different features
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)