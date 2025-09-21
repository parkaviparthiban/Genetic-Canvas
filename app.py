from flask import Flask, render_template, request, redirect, flash, session
import joblib

app = Flask(__name__)
app.secret_key = 'your-secret-key'

def extract_features(sequence):
    gc = sequence.count('G') + sequence.count('C')
    at = sequence.count('A') + sequence.count('T')
    total = len(sequence)
    gc_content = gc / total if total else 0
    at_ratio = at / total if total else 0
    return [gc_content, at_ratio, total]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    selected_model = request.form.get('selected_model', 'RandomForest')
    try:
        model = joblib.load(f'{selected_model.lower()}_model.pkl')
    except Exception as e:
        flash(f"Error loading model: {str(e)}")
        return redirect('/')

    if 'fasta_files' not in request.files:
        flash('No file uploaded.')
        return redirect('/')

    files = request.files.getlist('fasta_files')
    results = []

    for file in files:
        try:
            sequence = file.read().decode('utf-8')
            sequence = ''.join(line for line in sequence.splitlines() if not line.startswith('>')).strip()
            features = extract_features(sequence)
            prediction = model.predict([features])[0]
            results.append({
                'filename': file.filename,
                'prediction': int(prediction),
                'confidence': '95%'  # Placeholder
            })
        except Exception as e:
            results.append({
                'filename': file.filename,
                'prediction': f'Error - {str(e)}',
                'confidence': 'N/A'
            })

    session['batch_results'] = results
    session['selected_model'] = selected_model
    flash(f'Prediction completed using {selected_model}.')
    return render_template('index.html', predictions=results)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    models = ['RandomForest', 'XGBoost']
    selected_model = request.form.get('selected_model') or session.get('selected_model', 'RandomForest')
    batch_results = session.get('batch_results', [])

    correct = sum(1 for r in batch_results if r['prediction'] == 1)
    total = len(batch_results)
    accuracy = f"{(correct / total * 100):.2f}%" if total else "N/A"

    metrics = {
        'accuracy': accuracy,
        'precision': 'N/A',
        'recall': 'N/A'
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