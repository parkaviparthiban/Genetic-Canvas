import unittest
from app.utils.fasta_parser import parse_fasta

class TestFastaParser(unittest.TestCase):

    def test_single_sequence(self):
        fasta_content = """>seq1
        ATCGTACGATCG"""
        result = parse_fasta(fasta_content)
        self.assertEqual(len(result), 1)
        self.assertEqual(result['seq1'], "ATCGTACGATCG")

    def test_multiple_sequences(self):
        fasta_content = """>seq1
        ATCG
        >seq2
        GCTA"""
        result = parse_fasta(fasta_content)
        self.assertEqual(len(result), 2)
        self.assertEqual(result['seq1'], "ATCG")
        self.assertEqual(result['seq2'], "GCTA")

    def test_empty_input(self):
        fasta_content = ""
        result = parse_fasta(fasta_content)
        self.assertEqual(result, {})

    def test_invalid_format(self):
        fasta_content = "ATCG without header"
        with self.assertRaises(ValueError):
            parse_fasta(fasta_content)

if __name__ == '__main__':
    unittest.main()