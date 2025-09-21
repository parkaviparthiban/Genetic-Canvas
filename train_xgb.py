import joblib
from xgboost import XGBClassifier
import numpy as np

# Example training data: [gc_content, at_ratio, total_length]
X = np.array([
    [0.5, 0.5, 100],
    [0.6, 0.4, 120],
    [0.4, 0.6, 90],
    [0.7, 0.3, 150]
])
y = np.array([0, 1, 0, 1])  # Labels: 0 = non-coding, 1 = coding

# Train the model
model = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
model.fit(X, y)

# Save the model
joblib.dump(model, 'xgb_model.pkl')

print("✅ XGBoost model saved as xgb_model.pkl")