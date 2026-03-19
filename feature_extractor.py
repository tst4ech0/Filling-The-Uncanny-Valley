import spacy
from collections import Counter

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_features(text):
    """Extract stylometric features from text."""
    
    # Process the text with spaCy
    doc = nlp(text)
    
    # Get sentences and tokens
    sentences = list(doc.sents)
    tokens = [token for token in doc if not token.is_space]
    words = [token for token in tokens if token.is_alpha]
    
    # Calculate basic features
    features = {}
    
    # 1. Average sentence length
    if sentences:
        features['avg_sentence_length'] = len(tokens) / len(sentences)
    else:
        features['avg_sentence_length'] = 0
    
    # 2. Lexical diversity (unique words / total words)
    if words:
        features['lexical_diversity'] = len(set([w.text.lower() for w in words])) / len(words)
    else:
        features['lexical_diversity'] = 0
    
    # 3. Average word length
    if words:
        features['avg_word_length'] = sum(len(w.text) for w in words) / len(words)
    else:
        features['avg_word_length'] = 0
    
    # 4. Part-of-speech distribution
    pos_counts = Counter([token.pos_ for token in doc if token.is_alpha])
    total_pos = sum(pos_counts.values())
    
    if total_pos > 0:
        features['noun_ratio'] = pos_counts.get('NOUN', 0) / total_pos
        features['verb_ratio'] = pos_counts.get('VERB', 0) / total_pos
        features['adj_ratio'] = pos_counts.get('ADJ', 0) / total_pos
        features['adv_ratio'] = pos_counts.get('ADV', 0) / total_pos
    else:
        features['noun_ratio'] = 0
        features['verb_ratio'] = 0
        features['adj_ratio'] = 0
        features['adv_ratio'] = 0
    
    # 5. Punctuation features
    punctuation = [token for token in doc if token.is_punct]
    if tokens:
        features['comma_ratio'] = len([p for p in punctuation if p.text == ',']) / len(tokens)
        features['semicolon_ratio'] = len([p for p in punctuation if p.text == ';']) / len(tokens)
    else:
        features['comma_ratio'] = 0
        features['semicolon_ratio'] = 0
    
    print(f"Processed {len(words)} words in {len(sentences)} sentences")
    
    return features

# Test it out
if __name__ == "__main__":
    # Read from file
    with open('sample_essay.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    
    features = extract_features(text)
    print("\nExtracted features:")
    for name, value in features.items():
        print(f"  {name}: {value:.3f}")