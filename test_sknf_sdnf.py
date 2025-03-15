import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import Logic_operator

class TestLogicOperatorSDNF_SKNF(unittest.TestCase):
    
    def test_sdnf_simple(self):
        logic = Logic_operator("a&b")
        logic.build_sdnf()
        print(logic.build_sdnf())
        self.assertTrue("a" in ''.join(logic.table[len(logic.table)-1]))
        self.assertTrue("b" in ''.join(logic.table[len(logic.table)-1]))
        self.assertTrue("&" in ''.join(logic.table[len(logic.table)-1]))
    def test_sdnf_hard(self):
        logic = Logic_operator("a|b")
        sdnf = logic.build_sdnf()
        result = ' '
        for item in sdnf:
            result += item         # Для отладки: посмотрим список
        self.assertTrue("'!', 'a'" in result or "a!" in result)
        self.assertTrue("'b'" in result or "'!', 'b'" in result)
        self.assertTrue("&" in result)
        
    def test_sdnf_complex(self):
        logic = Logic_operator("(a&b)|c")
        logic.build_sdnf()
        result = ''.join(logic.table[len(logic.table)-1])
        self.assertTrue("c" in result)  
        
if __name__ == '__main__':
    unittest.main()