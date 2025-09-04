import pickle
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Example training data: [gc_content, at_ratio, total_length]
X = np.array([
    [0.5, 0.5, 100],
    [0.6, 0.4, 120],
    [0.4, 0.6, 90],
    [0.7, 0.3, 150]
])

# Example labels (e.g., 0 = non-coding, 1 = coding)
y = np.array([0, 1, 0, 1])

# Train model
model = RandomForestClassifier()
model.fit(X, y)

# Save to model.pkl
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("✅ Model saved as model.pkl")