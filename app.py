from flask import Flask, request, jsonify
from flask_cors import CORS
from Bio import SeqIO
import io

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "GeneticCanvas API is running!"

@app.route('/upload', methods=['POST'])
def upload_fasta():
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'No file uploaded'}), 400

    try:
        content = file.read().decode('utf-8')
        fasta_io = io.StringIO(content)
        sequences = list(SeqIO.parse(fasta_io, "fasta"))

        response = {
            'message': 'FASTA file received',
            'sequence_count': len(sequences),
            'total_length': sum(len(seq.seq) for seq in sequences),
            'sample_ids': [seq.id for seq in sequences[:5]]  # Show first 5 IDs
        }
        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)