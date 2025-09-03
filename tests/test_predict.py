import pandas as pd
import shap
import xgboost

# Load model and explainer once
model = xgboost.XGBClassifier()
model.load_model("model.json")

X_background = pd.read_csv("training_features.csv")
explainer = shap.Explainer(model, X_background)

def extract_features(sequence):
    gc_content = (sequence.count("G") + sequence.count("C")) / len(sequence)
    at_ratio = (sequence.count("A") + sequence.count("T")) / len(sequence)
    seq_length = len(sequence)
    return pd.DataFrame([{
        "gc_content": gc_content,
        "at_ratio": at_ratio,
        "seq_length": seq_length
    }])

def predict_with_explanation(sequence):
    features = extract_features(sequence)
    prediction = model.predict(features)[0]
    confidence = model.predict_proba(features)[0][1] * 100
    shap_values = explainer(features)
    contributions = dict(zip(features.columns, shap_values.values[0]))
    return prediction, round(confidence, 2), contributions