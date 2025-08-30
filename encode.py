import numpy as np

def one_hot_encode(seq):
    """
    One-hot encodes a single DNA sequence.
    """
    mapping = {'A': [1,0,0,0], 'C': [0,1,0,0], 'G': [0,0,1,0], 'T': [0,0,0,1]}
    return [mapping.get(base, [0,0,0,0]) for base in seq]

def integer_encode(seq):
    """
    Integer encodes a single DNA sequence.
    """
    mapping = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    return [mapping.get(base, -1) for base in seq]

def encode_sequences(sequences):
    """
    Encodes a list of DNA sequences using one-hot encoding.
    Returns a 3D NumPy array: (samples, sequence_length, 4)
    """
    encoded = [one_hot_encode(seq) for seq in sequences]
    return np.array(encoded)