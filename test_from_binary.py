import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from decimal_translator import *
class TestTranslatortoDecimal(unittest.TestCase):
  def test_get_decimal_from_binary(self):
    decimal=Translator_to_decimal()
    self.assertEqual(decimal.binary_to_decimal('1111'),15)

if __name__ == '__main__':
    unittest.main()