import pandas as pd
import xgboost as xgb

# Dummy training data
df = pd.DataFrame({
    "gc_content": [0.4, 0.6, 0.5],
    "at_ratio": [0.6, 0.4, 0.5],
    "seq_length": [100, 150, 120],
    "label": [0, 1, 0]
})

# Features and labels
X = df[["gc_content", "at_ratio", "seq_length"]]
y = df["label"]

# Train model
model = xgb.XGBClassifier()
model.fit(X, y)

# Save model to file
model.save_model("model.json")
print("✅ Model saved as model.json")