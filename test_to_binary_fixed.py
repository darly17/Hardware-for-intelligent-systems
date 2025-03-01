import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from binary_translator import *
class TestBinaryTranslator(unittest.TestCase):
  def test_get_fixed_binary(self):
    binary = Binary_translator()
    self.assertEqual(binary.decimal_to_binary_fixed(10.5),'01010.1')

if __name__ == '__main__':
    unittest.main()