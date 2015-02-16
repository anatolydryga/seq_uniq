import unittest

from ..run_blast import At_least_part_seq_aligned

class Test_at_least_half_seq_aligned(unittest.TestCase):
    
    def setUp(self):
        percentage = 50.0
        self.sim = At_least_part_seq_aligned(percentage)

    def test_empty_line_raises(self):
        self.assertRaises(ValueError, self.sim.is_similar, "")

    def test_not_correct_number_of_columns(self):
        self.assertRaises(ValueError, self.sim.is_similar, "1")
        self.assertRaises(ValueError, self.sim.is_similar, "1\t2\t3")
        self.assertRaises(ValueError, self.sim.is_similar, "1\t2\t3\t4\t5")
        self.assertTrue(self.sim.similar_ids() == None)

    def test_not_similar_pident_only_30(self):
        self.assertTrue(not self.sim.is_similar("qseq\tsseq\t10\t20\t100.00\t3"))
        self.assertTrue(self.sim.similar_ids() == None)

    def test_not_similar_pident_only_30_rev(self):
        self.assertTrue(not self.sim.is_similar("qseq\tsseq\t20\t10\t100.00\t3"))
        self.assertTrue(self.sim.similar_ids() == None)

    def test_similar_pident_60(self):
        self.assertTrue(self.sim.is_similar("qseq\tsseq\t10\t20\t100.00\t6"))
        self.assertTrue(self.sim.similar_ids() == ("qseq", "sseq"))

    def test_similar_pident_60_rev(self):
        self.assertTrue(self.sim.is_similar("qseq\tsseq\t20\t10\t100.00\t6"))
        self.assertTrue(self.sim.similar_ids() == ("qseq", "sseq"))
