import json
from feature_extractor import extract_features
import math

def load_profile(filename):
    """Load a student profile from JSON."""
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def calculate_similarity_score(new_essay_text, profile_data):
    """
    Compare new essay against profile.
    Returns a score from 0-100 (100 = perfect match).
    """
    # Extract features from new essay
    new_features = extract_features(new_essay_text)
    
    profile = profile_data['profile']
    
    # Calculate z-scores for each feature
    z_scores = []
    feature_details = []
    
    for feature_name, new_value in new_features.items():
        if feature_name in profile:
            mean = profile[feature_name]['mean']
            stdev = profile[feature_name]['stdev']
            
            # Calculate z-score (how many std devs away from mean)
            if stdev > 0:
                z_score = abs((new_value - mean) / stdev)
            else:
                # If stdev is 0, check if value matches exactly
                z_score = 0 if new_value == mean else 999
            
            z_scores.append(z_score)
            feature_details.append({
                'feature': feature_name,
                'new_value': new_value,
                'baseline_mean': mean,
                'baseline_stdev': stdev,
                'z_score': z_score
            })
    
    # Average z-score across all features
    avg_z_score = sum(z_scores) / len(z_scores) if z_scores else 0
    
    # Convert to similarity score (0-100)
    # Z-score of 0 = 100%, z-score of 3+ = very suspicious
    similarity = max(0, 100 - (avg_z_score * 20))
    
    return similarity, feature_details

# Test it out
if __name__ == "__main__":
    # Load the profile we created
    profile = load_profile('test_student_profile.json')
    
# Test with AI-generated essay
    with open('ai_generated.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    
    score, details = calculate_similarity_score(text, profile)
    
    print(f"\nSimilarity Score: {score:.1f}%")
    print(f"\nTop 5 feature comparisons:")
    for detail in details[:5]:
        print(f"  {detail['feature']}: {detail['new_value']:.3f} (baseline: {detail['baseline_mean']:.3f}, z-score: {detail['z_score']:.2f})")