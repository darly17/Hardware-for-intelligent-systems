import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from binary_translator import *
class TestBinaryTranslator(unittest.TestCase):
  def test_get_direct_binary(self):
    binary = Binary_translator()
    self.assertEqual(binary.get_binary(15),'1111')

if __name__ == '__main__':
    unittest.main()