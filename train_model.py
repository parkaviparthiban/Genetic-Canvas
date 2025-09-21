import joblib
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Example training data: [gc_content, at_ratio, total_length]
X = np.array([
    [0.5, 0.5, 100],
    [0.6, 0.4, 120],
    [0.4, 0.6, 90],
    [0.7, 0.3, 150]
])

# Example labels: 0 = non-coding, 1 = coding
y = np.array([0, 1, 0, 1])

# Train the model
model = RandomForestClassifier()
model.fit(X, y)

# Save the model
joblib.dump(model, 'rf_model.pkl')

print("✅ RandomForest model saved as rf_model.pkl")