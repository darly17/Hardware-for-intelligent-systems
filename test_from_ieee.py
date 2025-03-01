import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from decimal_translator import *
class TestBinaryOperations(unittest.TestCase):
  def test_get_decimal_from_ieee_float(self):
    decimal=Translator_to_decimal()
    self.assertEqual(decimal.binary_float_to_decimal('01000001011101001100110011001100'),15.299999237060547)

if __name__ == '__main__':
    unittest.main()