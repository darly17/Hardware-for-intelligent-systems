import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import Logic_operator

class TestLogicOperatorTableOperations(unittest.TestCase):
    
    def test_and_operation(self):
        logic = Logic_operator("a&b")
        logic.build_table()
        self.assertEqual(logic.table[2][1], "0")  
        self.assertEqual(logic.table[2][2], "0") 
        self.assertEqual(logic.table[2][3], "0")  
        self.assertEqual(logic.table[2][4], "1")  
        
    def test_or_operation(self):
        logic = Logic_operator("a|b")
        logic.build_table()
        self.assertEqual(logic.table[2][1], "0")  
        self.assertEqual(logic.table[2][2], "1")  
        self.assertEqual(logic.table[2][3], "1")  
        self.assertEqual(logic.table[2][4], "1") 
        
    def test_implication(self):
        logic = Logic_operator("a>b")
        logic.build_table()
        self.assertEqual(logic.table[2][1], "1")  
        self.assertEqual(logic.table[2][2], "1")  
        self.assertEqual(logic.table[2][3], "0")  
        self.assertEqual(logic.table[2][4], "1")  

if __name__ == '__main__':
    unittest.main()