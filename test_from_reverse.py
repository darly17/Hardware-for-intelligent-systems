import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from decimal_translator import *
class TestBinaryOperations(unittest.TestCase):
  def test_get_decimal_from_reverse(self):
    decimal=Translator_to_decimal()
    self.assertEqual(decimal.reverse_binary_to_decimal('10000'),'-15')

if __name__ == '__main__':
    unittest.main()