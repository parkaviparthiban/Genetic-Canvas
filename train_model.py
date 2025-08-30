import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pickle
from encode import encode_sequences  # assuming you have this function

# Step 1: Load labeled data
df = pd.read_csv('labels.csv')  # columns: sequence,label

# Step 2: Encode DNA sequences
X = encode_sequences(df['sequence'])  # returns 3D array

# ✅ Step 3: Flatten encoded sequences
X = np.array(X).reshape(X.shape[0], -1)  # ← Add this line here

# Step 4: Extract labels
y = df['label']

# Step 5: Train model
model = RandomForestClassifier()
model.fit(X, y)

# Step 6: Save model
with open('dna_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("✅ Model trained and saved as dna_model.pkl")