import json
from feature_extractor import extract_features
import statistics

class StudentProfile:
    def __init__(self, student_name):
        self.student_name = student_name
        self.baseline_features = []
        self.profile = {}
    
    def add_baseline_essay(self, text):
        """Add a baseline essay and extract its features."""
        features = extract_features(text)
        self.baseline_features.append(features)
        print(f"Added baseline essay {len(self.baseline_features)} for {self.student_name}")
    
    def compute_profile(self):
        """Calculate mean and std dev for each feature across baseline essays."""
        if len(self.baseline_features) < 2:
            print("Warning: Need at least 2 baseline essays for reliable statistics")
        
        # Get all feature names from first essay
        feature_names = self.baseline_features[0].keys()
        
        for feature_name in feature_names:
            # Get all values for this feature across baseline essays
            values = [essay[feature_name] for essay in self.baseline_features]
            
            # Calculate mean and standard deviation
            mean = statistics.mean(values)
            
            if len(values) > 1:
                stdev = statistics.stdev(values)
            else:
                stdev = 0
            
            self.profile[feature_name] = {
                'mean': mean,
                'stdev': stdev
            }
        
        print(f"\nProfile created for {self.student_name}")
        print(f"Based on {len(self.baseline_features)} baseline essays")
    
    def save_profile(self, filename):
        """Save profile to JSON file."""
        data = {
            'student_name': self.student_name,
            'num_baselines': len(self.baseline_features),
            'profile': self.profile
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Saved profile to {filename}")

# Test it out
if __name__ == "__main__":
    # Create a profile
    profile = StudentProfile("Test Student")
    
    # Add three DIFFERENT baseline essays
    for i in range(1, 4):
        filename = f'baseline{i}.txt'
        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read()
        print(f"\nReading {filename}: {len(text)} characters")
        profile.add_baseline_essay(text)
    
    # Compute the profile statistics
    profile.compute_profile()
    
    # Save it
    profile.save_profile('test_student_profile.json')
    
    print("\nProfile sample:")
    for feature, stats in list(profile.profile.items())[:3]:
        print(f"  {feature}: mean={stats['mean']:.3f}, stdev={stats['stdev']:.3f}")