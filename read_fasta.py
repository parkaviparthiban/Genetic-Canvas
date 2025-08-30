from Bio import SeqIO

def read_fasta(file_path):
    """
    Reads a FASTA file and returns a list of SeqRecord objects.
    """
    try:
        sequences = list(SeqIO.parse(file_path, "fasta"))
        print(f"✅ Loaded {len(sequences)} sequences from {file_path}")
        return sequences
    except Exception as e:
        print(f"❌ Error reading FASTA file: {e}")
        return []