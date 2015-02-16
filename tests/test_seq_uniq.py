import unittest
from ..seq_uniq import add_prefix_to_file

class Test_add_prefix_to_file(unittest.TestCase):

    def test_empty_prefix(self):
        original = '/usr/bin/smth.dat'
        expected = '/usr/bin/smth.dat'
        self.assertEqual(add_prefix_to_file("", original), expected)

    def test_fails_for_prefix_with_spaces(self):
        original = '/usr/bin/smth.dat'
        self.assertRaises(ValueError, add_prefix_to_file, " staff ", original)

    def test_nonempty_prefix(self):
        original = '/usr/bin/smth.dat'
        expected = '/usr/bin/PREPEND_smth.dat'
        prefix = 'PREPEND_'
        self.assertEquals(add_prefix_to_file(prefix, original), expected)
