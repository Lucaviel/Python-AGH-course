import unittest
from main import search, build

class AhoCorasick(unittest.TestCase):

    def test_normal(self):
        self.assertEqual(search(build(['abcd', 'bc']), 'abcd'), [0, 1]) #abc aabc
        self.assertEqual(search(build(['he','she','hers','his']), 'ahishers'), [1, 3, 4, 4]) #abc aabc

    def test_wrong_input(self):
        with self.assertRaises(TypeError):
            search(build([5353, 543, 5343]), 42543)
            search(build(['abc', 'aab', 'cba']), None)
