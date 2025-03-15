import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import Logic_operator

class TestLogicOperatorOPZ(unittest.TestCase):
    
    def test_simple_opz(self):
        logic = Logic_operator("a&b")
        logic.turn_into_opz()
        self.assertEqual(logic.opz_str, "ab&")
        
    def test_complex_opz(self):
        logic = Logic_operator("(a&b)|c")
        logic.turn_into_opz()
        self.assertEqual(logic.opz_str, "ab&c|")
        
  
        
    def test_triple_opz(self):
        logic = Logic_operator("(a|(b&c))")
        logic.turn_into_opz()
        self.assertEqual(logic.opz_str, "abc&|")
    def test_negative_opz(self):
        logic = Logic_operator("!a&b")
        
        self.assertEqual(logic.opz_str, "a!b&")

if __name__ == '__main__':
    unittest.main()