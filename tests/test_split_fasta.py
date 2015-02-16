import unittest
import tempfile

from Bio import SeqIO

from ..split_fasta import split_fasta_on_seq_ids

class Test_split_fasta(unittest.TestCase):
    
    def setUp(self):
        self.fasta = tempfile.NamedTemporaryFile()
        self.fasta.write(">1\nATGC\n>2\nTTTTT\n>3\nAAGG\n>4\nCCCC\n>5\nTACG\n")
        self.fasta.seek(0)

        self.w_seq = tempfile.NamedTemporaryFile()
        self.w_no_seq = tempfile.NamedTemporaryFile()

    def test_fails_if_seq_are_empty(self):
        self.assertRaises(ValueError, split_fasta_on_seq_ids,
                [], self.fasta.name, "w_seq_id.fasta", "w_no_seq_id.fasta")

    def test_fails_if_seq_are_not_presented_in_fasta(self):
        self.assertRaises(ValueError, split_fasta_on_seq_ids,
                ["1", "non_existent_id"], self.fasta.name, 
                "w_seq_id.fasta", "w_no_seq_id.fasta")

    def test_extact_one_seq(self):
        (n_total, n_with, n_without) = split_fasta_on_seq_ids(["1"], 
            self.fasta.name, self.w_seq.name, self.w_no_seq.name)
        self.assertEqual(n_total, 5)
        w_seq_records = SeqIO.index(self.w_seq.name, "fasta")
        w_no_seq_records = SeqIO.index(self.w_no_seq.name, "fasta")

        self.assertEqual(len(w_seq_records), 1)
        self.assertEqual(n_with, 1)
        self.assertTrue("1" in w_seq_records)
        self.assertEqual(str(w_seq_records["1"].seq), "ATGC")

        self.assertEqual(len(w_no_seq_records), 4)
        self.assertEqual(n_without, 4)
        self.assertFalse("1" in w_no_seq_records)
        
    def test_extact_multiple_seq(self):
        (n_total, n_with, n_without) = split_fasta_on_seq_ids(["5", "3"], 
            self.fasta.name, self.w_seq.name, self.w_no_seq.name)
        self.assertEqual(n_total, 5)
        w_seq_records = SeqIO.index(self.w_seq.name, "fasta")
        w_no_seq_records = SeqIO.index(self.w_no_seq.name, "fasta")

        self.assertEqual(len(w_seq_records), 2)
        self.assertEqual(n_with, 2)
        self.assertTrue("5" in w_seq_records)
        self.assertTrue("3" in w_seq_records)
        self.assertEqual(str(w_seq_records["5"].seq), "TACG")
        self.assertEqual(str(w_seq_records["3"].seq), "AAGG")

        self.assertEqual(len(w_no_seq_records), 3)
        self.assertEqual(n_without, 3)
        self.assertTrue("1" in w_no_seq_records)
        self.assertTrue("2" in w_no_seq_records)
        self.assertTrue("4" in w_no_seq_records)
        self.assertEqual(str(w_no_seq_records["1"].seq), "ATGC")
        self.assertEqual(str(w_no_seq_records["4"].seq), "CCCC")

