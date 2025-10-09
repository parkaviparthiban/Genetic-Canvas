import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score
import joblib

# 🔬 Feature extraction function
def extract_features(sequence):
    gc = sequence.count('G') + sequence.count('C')
    at = sequence.count('A') + sequence.count('T')
    total = len(sequence)
    gc_content = gc / total if total else 0
    at_ratio = at / total if total else 0
    return [gc_content, at_ratio, total]

# 📄 Load dataset
df = pd.read_csv('dna_dataset.csv')  # Make sure this file exists
X = [extract_features(seq) for seq in df['sequence']]
y = df['label']

# 🧪 Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 🌲 Train RandomForest
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 📊 Evaluate
y_pred = model.predict(X_test)
print("✅ Model Performance:")
print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
print(f"Precision: {precision_score(y_test, y_pred):.2f}")
print(f"Recall: {recall_score(y_test, y_pred):.2f}")

# 💾 Save model
joblib.dump(model, 'rf_model.pkl')
print("✅ RandomForest model saved as rf_model.pkl")