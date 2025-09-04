import pickle

# Load your trained model from disk
import os
import pickle

def load_model():
    base_dir = os.path.dirname(__file__)  # Folder where model.py lives
    model_path = os.path.join(base_dir, 'model.pkl')
    with open(model_path, 'rb') as f:
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