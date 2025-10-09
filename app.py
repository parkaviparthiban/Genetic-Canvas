from flask import Flask, render_template, request, redirect, flash, session
import joblib
import os
from sklearn.metrics import accuracy_score, precision_score, recall_score

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# Map display names to actual filenames
def get_model_filename(name):
    return {
        'RandomForest': 'rf_model.pkl',
        'XGBoost': 'xgb_model.pkl'
    }.get(name, 'rf_model.pkl')  # default fallback

# Feature extraction from DNA sequence
def extract_features(sequence):
    gc = sequence.count('G') + sequence.count('C')
    at = sequence.count('A') + sequence.count('T')
    total = len(sequence)
    gc_content = gc / total if total else 0
    at_ratio = at / total if total else 0
    return [gc_content, at_ratio, total]

# Parse FASTA with optional label in header
def parse_fasta_with_label(content):
    sequences = []
    lines = content.splitlines()
    for i in range(0, len(lines), 2):
        header = lines[i]
        sequence = lines[i+1].strip()
        label = None
        if 'label=' in header:
            try:
                label = int(header.split('label=')[-1])
            except:
                label = None
        sequences.append({'sequence': sequence, 'label': label})
    return sequences

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    selected_model = request.form.get('selected_model', 'RandomForest')
    model_path = get_model_filename(selected_model)

    if not os.path.exists(model_path):
        flash(f"Error loading model: File '{model_path}' not found.")
        return redirect('/')

    try:
        model = joblib.load(model_path)
    except Exception as e:
        flash(f"Error loading model: {str(e)}")
        return redirect('/')

    if 'fasta_files' not in request.files:
        flash('No file uploaded.')
        return redirect('/')

    files = request.files.getlist('fasta_files')
    results = []
    fasta_sequences = []

    for file in files:
        try:
            content = file.read().decode('utf-8')
            parsed = parse_fasta_with_label(content)
            for entry in parsed:
                features = extract_features(entry['sequence'])
                prediction = model.predict([features])[0]
                prob = model.predict_proba([features])[0][1]  # Confidence for class 1
                results.append({
                    'filename': file.filename,
                    'prediction': int(prediction),
                    'confidence': f"{prob * 100:.2f}%",
                    'label': entry['label']
                })
                fasta_sequences.append({
                    'filename': file.filename,
                    'sequence': entry['sequence'],
                    'label': entry['label']
                })
        except Exception as e:
            results.append({
                'filename': file.filename,
                'prediction': f'Error - {str(e)}',
                'confidence': 'N/A'
            })

    session['batch_results'] = results
    session['fasta_sequences'] = fasta_sequences
    session['selected_model'] = selected_model
    flash(f'Prediction completed using {selected_model}.')
    return render_template('index.html', predictions=results)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    models = ['RandomForest', 'XGBoost']
    selected_model = request.form.get('selected_model') or session.get('selected_model', 'RandomForest')
    fasta_sequences = session.get('fasta_sequences', [])
    batch_results = []

    model_path = get_model_filename(selected_model)
    true_labels = []
    predicted_labels = []

    if os.path.exists(model_path) and fasta_sequences:
        try:
            model = joblib.load(model_path)
            for item in fasta_sequences:
                features = extract_features(item['sequence'])
                prediction = model.predict([features])[0]
                prob = model.predict_proba([features])[0][1]
                batch_results.append({
                    'filename': item['filename'],
                    'prediction': int(prediction),
                    'confidence': f"{prob * 100:.2f}%"
                })
                if item.get('label') is not None:
                    true_labels.append(item['label'])
                    predicted_labels.append(int(prediction))
        except Exception as e:
            flash(f"Error loading model: {str(e)}")

    session['batch_results'] = batch_results
    session['selected_model'] = selected_model

    # Calculate metrics
    if true_labels:
        accuracy = f"{accuracy_score(true_labels, predicted_labels) * 100:.2f}%"
        precision = f"{precision_score(true_labels, predicted_labels):.2f}"
        recall = f"{recall_score(true_labels, predicted_labels):.2f}"
    else:
        accuracy = "N/A"
        precision = "N/A"
        recall = "N/A"

    metrics = {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall
    }

    roc_curve = {
        'fpr': 'N/A',
        'tpr': 'N/A'
    }

    return render_template('dashboard.html',
                           models=models,
                           selected_model=selected_model,
                           metrics=metrics,
                           roc_curve=roc_curve,
                           batch_results=batch_results)

if __name__ == '__main__':
    app.run(debug=True)