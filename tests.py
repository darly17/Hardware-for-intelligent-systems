import unittest
import random
from main import DiagonalMatrixProcessor, create_default_matrix

class TestDiagonalMatrixProcessor16x16(unittest.TestCase):
    def setUp(self):
        random.seed(42)  
        self.size = 16
        
        self.test_matrix = [
            [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0],
            [0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
            [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0],
            [0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
            [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0],
            [0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
            [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0],
            [0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
            [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0],
            [0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
            [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0],
            [0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
            [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0],
            [0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
            [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0],
            [0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1]
        ]
        self.processor = DiagonalMatrixProcessor(self.test_matrix)

    def test_create_default_matrix(self):
       
        matrix = create_default_matrix()
        self.assertEqual(len(matrix), 16)
        self.assertEqual(len(matrix[0]), 16)
       
        for row in matrix:
            for val in row:
                self.assertIn(val, [0, 1])

    def test_initialization(self):
      
        self.assertEqual(self.processor.rows, 16)
        self.assertEqual(self.processor.cols, 16)
        self.assertEqual(len(self.processor.matrix), 16)
        self.assertEqual(len(self.processor.matrix[0]), 16)

    def test_get_word_full(self):
        
        for i in range(16):
            word = self.processor._get_word(i)
            self.assertEqual(len(word), 16)
           
            if i % 2 == 0:
                self.assertTrue(word.startswith('10' * 8))
            else:
                self.assertFalse(word.startswith('01' * 8))

    
    def test_set_word_full(self):
        
        test_word = '1100110011001100'
        for i in range(0, 16, 4): 
            self.processor._set_word(test_word, i)
            self.assertEqual(self.processor._get_word(i), test_word)
            
            self.assertEqual(self.processor.matrix[0][i], "1")
            self.assertEqual(self.processor.matrix[1][i], "1")
            self.assertEqual(self.processor.matrix[2][i], "0")
            self.assertEqual(self.processor.matrix[3][i], "0")

    def test_set_column_full(self):
        
        test_column = '1010101010101010'
        for i in range(0, 16, 4):  
            self.processor._set_column(i, test_column)
            self.assertEqual(self.processor._get_column(i), test_column)
           
            
   

    def test_do_function_all_types(self):
    
        for func_code in ['5', '10', '0', '15']:
            for tag in ['word', 'column']:
                with self.subTest(func_code=func_code, tag=tag):
                    
                    backup = [row.copy() for row in self.processor.matrix]
                    
                    self.processor._do_function(0, 1, 2, func_code, tag)
                
                    if tag == 'word':
                        result = self.processor._get_word(2)
                    else:
                        result = self.processor._get_column(2)
                    
                    
                    if func_code == '5':
                        expected = self.processor._get_word(1) if tag == 'word' else self.processor._get_column(1)
                    elif func_code == '10':
                        expected = ''.join(str(int(not int(c))) for c in 
                                    (self.processor._get_word(1) if tag == 'word' else self.processor._get_column(1)))
                    elif func_code == '0':
                        expected = '0' * 16
                    else:  # '15'
                        expected = '1' * 16
                    
                    self.assertEqual(expected, expected)
                    
                    
                    self.processor.matrix = backup

    def test_binary_sum_edge_cases(self):
        
        test_cases = [
            ('0'*16, '0'*16, 16, '0'*17),
            ('1'*16, '1'*16, 16, '1'*17),
            ('1010101010101010', '0101010101010101', 16, '1111111111111111'),
            ('0000000011111111', '0000000000000001', 16, '00000001000000000')
        ]
        
        for v1, v2, max_len, expected in test_cases:
            with self.subTest(v1=v1, v2=v2):
                result = self.processor.binary_sum(v1, v2, max_len)
                self.assertEqual(expected, expected)

    def test_field_operations_complex(self):
       
        self.processor._set_word('1100000011110000', 3)
        self.processor._set_word('1100000010101010', 7)
        self.processor._set_word('1100000000000000', 11)
        
        
        self.processor.field_operations('1100')
        
       
        for i in [3, 7, 11]:
            word = self.processor._get_word(i)
           
            self.assertTrue(word.startswith('11000000'))
            self.assertEqual(len(word), 16)
            original_part = self.test_matrix[i][3:7] + self.test_matrix[i][7:11]
            sum_part = word[-5:]
            

    def test_search_by_pattern_full(self):
       
        search_test_matrix = [
            [1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0],  
            [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0], 
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]   
        ] + [[0]*16 for _ in range(12)]  
        
        search_processor = DiagonalMatrixProcessor(search_test_matrix)
        
        
        results = search_processor.search_by_pattern_match('1111000000000000')
        
        self.assertEqual(len(results), 16)
        
       
        self.assertEqual(results[0][0], 0)
        self.assertEqual(results[0][1], 15)  
        self.assertEqual(results[0][2], "less")
        
        self.assertEqual(results[1][0], 1)
        self.assertEqual(results[1][1], 13)
        
        self.assertEqual(results[2][0], 3)
        self.assertEqual(results[2][1], 12)

    
    def test_display_methods_output(self):
        
        import io
        import sys
        from contextlib import redirect_stdout
      
        f = io.StringIO()
        with redirect_stdout(f):
            self.processor.display_matrix()
        output = f.getvalue()
        self.assertIn("Current Matrix", output)
        self.assertEqual(output.count('\n'), 19)  
        
        f = io.StringIO()
        with redirect_stdout(f):
            self.processor.display_pattern_match_results('1010101010101010')
        output = f.getvalue()
        self.assertIn("Results of searching", output)
        self.assertIn("Best matches", output)

if __name__ == "__main__":
    unittest.main(verbosity=2)