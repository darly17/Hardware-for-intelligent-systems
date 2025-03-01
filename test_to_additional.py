import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from binary_translator import *
class TestBinaryOperations(unittest.TestCase):
  def test_get_additional_binary(self):
    binary = Binary_translator()
    self.assertEqual(binary.get_additional_binary(-15),'10001')

if __name__ == '__main__':
    unittest.main()