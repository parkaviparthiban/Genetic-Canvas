from flask import Flask, request, jsonify
import joblib
import numpy as np
from encode import one_hot_encode  # Make sure this function exists and works

app = Flask(__name__)

# 🔹 Route 1: Encode DNA sequence
@app.route('/encode', methods=['POST'])
def encode_sequence():
    data = request.get_json()
    sequence = data.get('sequence', '')

    if not sequence:
        return jsonify({'error': 'No sequence provided'}), 400

    encoded = one_hot_encode(sequence)
    return jsonify({'encoded': encoded})


# 🔹 Route 2: Predict label from DNA sequence
@app.route('/predict', methods=['POST'])
def predict_sequence():
    data = request.get_json()
    sequence = data.get('sequence', '')

    if not sequence:
        return jsonify({'error': 'No sequence provided'}), 400

    try:
        # Encode the sequence
        encoded = one_hot_encode(sequence)
        encoded = np.array(encoded).reshape(1, -1)  # Reshape for model input

        # Load the trained model
        model = joblib.load('dna_model.pkl')

        # Make prediction
        prediction = model.predict(encoded)

        return jsonify({'prediction': prediction[0]})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# 🔹 Run the app
if __name__ == '__main__':
    app.run(debug=True)