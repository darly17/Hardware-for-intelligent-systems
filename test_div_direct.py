import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from binary_operations import *
class TestBinaryOperations(unittest.TestCase):
    def test_get_div_direct(self):
        binary_op=Binary_operation()
        self.assertEqual(binary_op.dividing_direct(43, 6), '0111.00101')
if __name__ == '__main__':
    unittest.main()