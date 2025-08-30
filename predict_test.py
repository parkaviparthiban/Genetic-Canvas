import pickle
import numpy as np
from encode import encode_sequences

# Load model
with open('dna_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Sample DNA sequence
sample = ['ATCGTACGATCG']
X = encode_sequences(sample)
X = np.array(X).reshape(X.shape[0], -1)

# Predict
prediction = model.predict(X)
print("Prediction:", prediction[0])