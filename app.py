from flask import Flask, render_template, request
from io import StringIO
from Bio import SeqIO

app = Flask(__name__)

# 🧬 Home route with FASTA upload
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        fasta_file = request.files.get("fasta_file")
        if not fasta_file or fasta_file.filename == "":
            return render_template("index.html", error="No file selected")

        try:
            fasta_io = StringIO(fasta_file.read().decode("utf-8"))
            sequences = list(SeqIO.parse(fasta_io, "fasta"))
            if not sequences:
                return render_template("index.html", error="No sequences found")

            # Use first sequence for demo prediction
            seq = sequences[0]
            sequence_id = seq.id
            input_sequence = str(seq.seq)
            prediction = "Class A"
            confidence = 91.4

            return render_template("results.html",
                                   sequence_id=sequence_id,
                                   input_sequence=input_sequence,
                                   prediction=prediction,
                                   confidence=confidence)
        except Exception as e:
            return render_template("index.html", error=f"Error parsing FASTA: {str(e)}")

    return render_template("index.html")

# 📊 Dashboard route
@app.route("/dashboard")
def dashboard():
    models = ["DNAClassifier-v1", "GeneticNet", "BioSeqAI"]
    selected_model = models[0]
    metrics = {
        "accuracy": "92.5%",
        "precision": "90.1%",
        "recall": "89.7%",
        "f1-score": "89.9%"
    }
    roc_curve = {
        "fpr": "[0.0, 0.1, 0.2]",
        "tpr": "[0.0, 0.85, 0.95]"
    }
    batch_results = [
        {"id": "seq1", "prediction": "Class A", "confidence": 93.2},
        {"id": "seq2", "prediction": "Class B", "confidence": 88.7}
    ]
    return render_template("dashboard.html",
                           models=models,
                           selected_model=selected_model,
                           metrics=metrics,
                           roc_curve=roc_curve,
                           batch_results=batch_results)

# 📁 Results route (optional direct access)
@app.route("/results")
def results():
    return render_template("results.html")

if __name__ == "__main__":
    app.run(debug=True)