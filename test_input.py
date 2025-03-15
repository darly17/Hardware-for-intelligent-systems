import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import Logic_operator

class TestLogicOperator(unittest.TestCase):
    
    def test_init_simple_expression(self):
        logic = Logic_operator("a&b")
        
        self.assertEqual(logic.letters_list, ['a', 'b'])
        self.assertEqual(logic.operations, ["&", ">", "|", "!", "~"])
        self.assertEqual(len(logic.table), 3)  
        self.assertEqual(len(logic.table[0]), 5)  

    def test_table_creation(self):
        logic = Logic_operator("a|b")
        self.assertEqual(logic.table[0][0], 'a')
        self.assertEqual(logic.table[1][0], 'b')
        self.assertEqual(logic.table[0][1], '0')
        self.assertEqual(logic.table[1][1], '0')
        self.assertEqual(logic.table[0][4], '1')
        self.assertEqual(logic.table[1][4], '1')

    def test_invalid_expression(self):
        with self.assertRaises(Exception):
            Logic_operator("x&y")

if __name__ == '__main__':
    unittest.main()