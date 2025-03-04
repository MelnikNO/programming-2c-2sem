import unittest
from bintree import gen_bin_rec_tree, gen_bin_nec_tree

class TestBinaryTreeFunctions(unittest.TestCase):

    def test_gen_bin_rec_tree(self):
        expected_result = {0: [{0: [{}, {}]}, {-2: [{}, {}]}]}
        result = gen_bin_rec_tree(root=0, height=2)
        self.assertEqual(result, expected_result)

    def test_gen_bin_nec_tree(self):
        expected_result = {'0': [{'0': []}, {'-2': []}, {'0': []}, {'-2': []}], '-2': [{'4': []}, {'-4': []}], '4': [], '-4': []}
        result = gen_bin_nec_tree(root=0, height=3)
        self.assertEqual(result, expected_result)

    def test_empty_tree(self):
        self.assertEqual(gen_bin_rec_tree(root=0, height=0), {})
        self.assertEqual(gen_bin_nec_tree(height=0, root=0), {})

if __name__ == "__main__":
    unittest.main()
