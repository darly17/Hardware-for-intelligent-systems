import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from binary_translator import *
class TestBinaryOperations(unittest.TestCase):
  def test_get_ieee_from_decimal(self):
    binary = Binary_translator()
    self.assertEqual(binary.decimal_to_binary_float(15.67),'01000001011110101011100001010001')

if __name__ == '__main__':
    unittest.main()