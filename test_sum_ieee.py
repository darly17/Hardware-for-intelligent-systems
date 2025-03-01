import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from binary_operations import *
from binary_translator import *

class TestBinaryOperations(unittest.TestCase):
    def test_get_sum_ieee(self):
      binary_op=Binary_operation()
      self.assertEqual(binary_op.sum_float_binary(0.5, 1.5), '01000000000000000000000000000000')
if __name__ == '__main__':
    unittest.main()