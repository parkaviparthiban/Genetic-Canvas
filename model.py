import pickle

# Load your trained model from disk
def load_model():
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    return model

# Extract features from a DNA sequence
def extract_features(sequence):
    sequence = sequence.upper()
    gc_count = sequence.count('G') + sequence.count('C')
    at_count = sequence.count('A') + sequence.count('T')
    total_length = len(sequence)

    gc_content = gc_count / total_length if total_length else 0
    at_ratio = at_count / total_length if total_length else 0

    return [gc_content, at_ratio, total_length]