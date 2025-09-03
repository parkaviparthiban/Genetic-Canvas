# model_utils.py
import xgboost
import pandas as pd
import shap

def load_model():
    model = xgboost.XGBClassifier()
    model.load_model("model.json")
    return model

def predict_sequence(model, sequence):
    gc_content = (sequence.count("G") + sequence.count("C")) / len(sequence)
    at_ratio = (sequence.count("A") + sequence.count("T")) / len(sequence)
    seq_length = len(sequence)

    features = pd.DataFrame([{
        "gc_content": gc_content,
        "at_ratio": at_ratio,
        "seq_length": seq_length
    }])

    prediction = model.predict(features)[0]
    confidence = model.predict_proba(features)[0][1]
    return prediction, confidence

def explain_prediction(model, sequence):
    gc_content = (sequence.count("G") + sequence.count("C")) / len(sequence)
    at_ratio = (sequence.count("A") + sequence.count("T")) / len(sequence)
    seq_length = len(sequence)

    features = pd.DataFrame([{
        "gc_content": gc_content,
        "at_ratio": at_ratio,
        "seq_length": seq_length
    }])

    explainer = shap.Explainer(model, features)
    shap_values = explainer(features)
    return dict(zip(features.columns, shap_values.values[0]))