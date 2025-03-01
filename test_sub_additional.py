import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from binary_operations import *
class TestBinaryOperations(unittest.TestCase):
  def test_get_sub_additional(self):
    binary_op=Binary_operation()
    self.assertEqual(binary_op.substraction_additional_binary(2,5),'1101')

if __name__ == '__main__':
    unittest.main()