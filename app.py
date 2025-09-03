from flask import Flask, request, jsonify
import pandas as pd
from model import load_model, extract_features

app = Flask(__name__)
model = load_model()  # Load trained model from model.pkl

@app.route('/')
def home():
    return "✅ GeneticCanvas API is live and ready!"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    sequence = data.get('sequence')

    if not sequence:
        return jsonify({'error': 'No DNA sequence provided'}), 400

    features = extract_features(sequence)
    prediction = model.predict([features])[0]

    return jsonify({'prediction': prediction})

@app.route('/batch_predict', methods=['POST'])
def batch_predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    df = pd.read_csv(file)

    if 'sequence' not in df.columns:
        return jsonify({'error': 'CSV must contain a "sequence" column'}), 400

    features = df['sequence'].apply(extract_features)
    feature_df = pd.DataFrame(features.tolist())
    df['prediction'] = model.predict(feature_df)

    return df[['sequence', 'prediction']].to_json(orient='records')

if __name__ == '__main__':
    app.run(debug=True)