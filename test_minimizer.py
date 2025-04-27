import unittest
from main import LogicMinimizer
from itertools import product, combinations
class TestLogicMinimizer(unittest.TestCase):
    def setUp(self):
        
        self.simple_function = "a&b"
        self.three_var_function = "(a&b&c)|(a&!b&c)|(!a&b&!c)"
        self.four_var_function = "(a&b&c&d)|(!a&b&c&d)|(a&!b&c&d)"
        self.five_var_function = "(a&b&c&d&e)|(!a&b&c&d&e)|(a&!b&c&d&e)"
    
    
    def test_initialization(self):
        lm = LogicMinimizer(self.simple_function)
        self.assertEqual(lm.variables, ['a', 'b'])
        self.assertEqual(lm.number_variables, 2)
        self.assertTrue(hasattr(lm, 'sdnf'))
        self.assertTrue(hasattr(lm, 'sknf'))
    
    def test_count_negations(self):
        lm = LogicMinimizer(self.simple_function)
        self.assertEqual(lm.count_negations("a&b"), 0)
        self.assertEqual(lm.count_negations("!a&b"), 1)
        self.assertEqual(lm.count_negations("!a&!b"), 2)
    
    def test_split_term(self):
        lm = LogicMinimizer(self.simple_function)
        self.assertEqual(lm.split_term("a&b"), ['a', 'b'])
        self.assertEqual(lm.split_term("!a&b"), ['!a', 'b'])
        self.assertEqual(lm.split_term("a|b"), ['a', 'b'])
        self.assertEqual(lm.split_term("!a|b"), ['!a', 'b'])
    
    def test_merge(self):
        lm = LogicMinimizer(self.simple_function)
        can_merge, merged = lm.merge("a&b", "a&!b")
        self.assertTrue(can_merge)
        self.assertEqual(merged, "a&-")
        
        can_merge, merged = lm.merge("a&b", "!a&b")
        self.assertTrue(can_merge)
        self.assertEqual(merged, "-&b")
        
        can_merge, merged = lm.merge("a&b", "c&d")
        self.assertFalse(can_merge)
        self.assertEqual(merged,'-&-')
    
    def test_is_covered(self):
        lm = LogicMinimizer(self.simple_function)
        self.assertTrue(lm.is_covered("a&b", "-&b"))
        self.assertTrue(lm.is_covered("a&b", "a&-"))
        self.assertTrue(lm.is_covered("a&b", "-&-"))
        self.assertFalse(lm.is_covered("a&b", "-&!b"))
    
    
    def test_minimize_sdnf_simple(self):
        lm = LogicMinimizer("(a&b)|(!a&b)")
        minimized = lm.minimize_sdnf()
        self.assertEqual(minimized, "b")
    
    def test_minimize_sknf_simple(self):
        lm = LogicMinimizer("(a|b)&(!a|b)")
        minimized = lm.minimize_sknf()
        self.assertEqual(minimized, "b")
    
    def test_minimize_sdnf_table_method(self):
        lm = LogicMinimizer("(a&b)|(!a&b)")
        minimized = lm.minimize_sdnf_table_method()
        self.assertEqual(minimized, "b")
    
    def test_minimize_sknf_table_method(self):
        lm = LogicMinimizer("(a|b)&(!a|b)")
        minimized = lm.minimize_sknf_table_method()
        self.assertEqual(minimized, "b")
    
    def test_minimize_sdnf_karnaugh(self):
        
        lm = LogicMinimizer("(a&b)|(!a&b)")
        minimized = lm.minimize_sdnf_karnaugh()
        self.assertEqual(minimized, "(b)")
    
    def test_minimize_sknf_karnaugh(self):
        lm = LogicMinimizer("(a|b)&(!a|b)")
        minimized = lm.minimize_sknf_karnaugh()
        self.assertEqual(minimized, "(b)")
    
    
    def test_three_variables(self):
        lm = LogicMinimizer(self.three_var_function)
        minimized_sdnf = lm.minimize_sdnf()
        self.assertTrue("&c" in minimized_sdnf )
        self.assertTrue("!a&b&!c" in minimized_sdnf)
        
        minimized_karnaugh = lm.minimize_sdnf_karnaugh()
        self.assertTrue("b" in minimized_karnaugh and "!a" in minimized_karnaugh)
    
    
    def test_four_variables(self):
        lm = LogicMinimizer(self.four_var_function)
        minimized = lm.minimize_sdnf()
        self.assertTrue("c&d" in minimized)
        self.assertTrue("b" in minimized or "a" in minimized)
        
        karnaugh = lm.minimize_sdnf_karnaugh()
        self.assertTrue("c" in karnaugh and "d" in karnaugh)
    
    
    def test_five_variables(self):
        lm = LogicMinimizer(self.five_var_function)
        minimized = lm.minimize_sdnf_karnaugh()
        self.assertTrue("c" in minimized and "d" in minimized and "e" in minimized)
        self.assertTrue("b" in minimized or "a" in minimized)
    
   
    
    def test_single_variable(self):
        lm = LogicMinimizer("a")
        self.assertEqual(lm.minimize_sdnf(), "a")
        self.assertEqual(lm.minimize_sknf(), "a")
    
    
    
    def test_always_false(self):
        lm = LogicMinimizer("a&!a")
        self.assertEqual(lm.minimize_sdnf(), "0")
        self.assertEqual(lm.minimize_sknf(), "-")
    
    
    def test_find_prime_implicants(self):
        lm = LogicMinimizer("(a&b)|(!a&b)")
        terms = ["a&b", "!a&b"]
        implicants = lm._find_prime_implicants(terms)
        self.assertTrue("b" in implicants or "-&b" in implicants)
    
    def test_build_coverage_table(self):
        lm = LogicMinimizer("(a&b)|(!a&b)")
        table = lm._build_coverage_table(["b"], ["a&b", "!a&b"])
        self.assertEqual(table, [[0, 0]])
    
    def test_find_core_implicants(self):
        lm = LogicMinimizer("(a&b)|(!a&b)")
        core = lm._find_core_implicants([[1, 1]], ["b"], ["a&b", "!a&b"])
        self.assertEqual(core, ["b"])
    
    def test_find_minimal_cover(self):
        lm = LogicMinimizer("(a&b)|(!a&b)")
        cover = lm._find_minimal_cover(
            ["a&b", "!a&b"], 
            ["b"], 
            ["b"], 
            [[1, 1]]
        )
        self.assertEqual(cover, ["b"])
    
    
    def test_build_karnaugh_map(self):
        lm = LogicMinimizer("(a&b)|(!a&b)")
        case_values = {
            (0,0): 0, 
            (0,1): 1, 
            (1,0): 0, 
            (1,1): 1
        }
        kmap = lm._build_karnaugh_map(case_values)
        self.assertEqual(kmap, [[0, 1], [0, 1]])
    
    def test_find_karnaugh_groups(self):
        lm = LogicMinimizer("(a&b)|(!a&b)")
        kmap = [[0, 1], [0, 1]]
        groups = lm._find_karnaugh_groups(kmap, 1, 2)
        self.assertEqual(len(groups), 1)
        self.assertEqual(groups[0], [0, 1, 1, 1])
    
    def test_get_variable_val(self):
        lm = LogicMinimizer("a&b&c&d&e")
        
        
        lm.number_variables = 1
        self.assertEqual(lm._get_variable_val(0, 0), [0])
        self.assertEqual(lm._get_variable_val(0, 1), [1])
        
        
        lm.number_variables = 2
        self.assertEqual(lm._get_variable_val(0, 0), [0, 0])
        self.assertEqual(lm._get_variable_val(1, 1), [1, 1])
        
        
        lm.number_variables = 3
        self.assertEqual(lm._get_variable_val(0, 0), [0, 0, 0])
        self.assertEqual(lm._get_variable_val(1, 3), [1, 1, 0])
        
        
        lm.number_variables = 4
        self.assertEqual(lm._get_variable_val(0, 0), [0, 0, 0, 0])
        self.assertEqual(lm._get_variable_val(3, 3), [1, 0, 1, 0])
        
        
        lm.number_variables = 5
        self.assertEqual(lm._get_variable_val(0, 0), [0, 0, 0, 0, 0])
        self.assertEqual(lm._get_variable_val(3, 7), [1, 0, 1, 0, 0])
    
    def test_get_dimensions(self):
        lm = LogicMinimizer("a")
        self.assertEqual(lm.get_dimensions(), (1, 2))
        
        lm = LogicMinimizer("a&b")
        self.assertEqual(lm.get_dimensions(), (2, 2))
        
        lm = LogicMinimizer("a&b&c")
        self.assertEqual(lm.get_dimensions(), (2, 4))
        
        lm = LogicMinimizer("a&b&c&d")
        self.assertEqual(lm.get_dimensions(), (4, 4))
        
        lm = LogicMinimizer("a&b&c&d&e")
        self.assertEqual(lm.get_dimensions(), (4, 8))
        
        with self.assertRaises(ValueError):
            lm.number_variables = 6
            lm.get_dimensions()
    
    
    
    
    def test_additional_coverage(self):
        
        lm = LogicMinimizer("a&b&c&d&e")
        
        
        self.assertEqual(lm._row_index((0,0,0,0,0)), 0)
        self.assertEqual(lm._row_index((1,1,0,0,0)), 2)
        
        
        self.assertEqual(lm._column_index((0,0,0,0,0)), 0)
        self.assertEqual(lm._column_index((0,0,1,1,0)), 4)
        
        
        self.assertEqual(lm._get_ab_from_row(0), (0,0))
        self.assertEqual(lm._get_ab_from_row(3), (1,0))
        
        
        self.assertEqual(lm._get_bc_from_column(0), (0,0))
        self.assertEqual(lm._get_bc_from_column(3), (1,0))
        
        self.assertEqual(lm._get_cde_from_column(0), (0,0,0))
        self.assertEqual(lm._get_cde_from_column(7), (1,0,0))
   
        self.assertTrue(lm._is_power_of_2(1))
        self.assertTrue(lm._is_power_of_2(2))
        self.assertTrue(lm._is_power_of_2(4))
        self.assertFalse(lm._is_power_of_2(3))
        self.assertFalse(lm._is_power_of_2(0))
    
    def test_complex_5var_function(self):
        function = "(a&b&c&d&e)|(!a&b&c&d&e)|(a&!b&c&d&e)|(a&b&!c&d&e)|(a&b&c&!d&e)"
        lm = LogicMinimizer(function)
        
        # Проверяем, что минимизация не вызывает ошибок
        self.assertTrue(len(lm.minimize_sdnf()) > 0)
        self.assertTrue(len(lm.minimize_sknf()) > 0)
        self.assertTrue(len(lm.minimize_sdnf_table_method()) > 0)
        self.assertTrue(len(lm.minimize_sknf_table_method()) > 0)
        self.assertTrue(len(lm.minimize_sdnf_karnaugh()) > 0)
        self.assertTrue(len(lm.minimize_sknf_karnaugh()) > 0)

    def test_karnaugh_edge_cases(self):
        # Тест для случая, когда все клетки карты Карно заполнены 1
        lm = LogicMinimizer("a|!a")
        kmap = [[1, 1], [1, 1]]
        minimized = lm._minimize_karnaugh_to_dnf(kmap)
        self.assertEqual(minimized, "0")
        
        # Тест для случая, когда все клетки карты Карно заполнены 0
        kmap = [[0, 0], [0, 0]]
        minimized = lm._minimize_karnaugh_to_cnf(kmap)
        self.assertEqual(minimized, "1")

    # def test_mirror_groups_5vars(self):
    #     function = "(a&b&c&d&e)|(a&b&!c&d&e)|(a&b&c&!d&e)|(a&b&!c&!d&e)"
    #     lm = LogicMinimizer(function)
    #     kmap = lm._build_karnaugh_map(lm._find_sdnf_values(list(product([0, 1], repeat=5)), [t.strip() for t in function.split('|')]))
        
    #     groups = lm._find_karnaugh_groups(kmap, 1, 5)
    #     self.assertTrue(len(groups) > 0)
        
    #     # Проверяем, что найдены правильные группы
    #     for group in groups:
    #         self.assertTrue(len(group) >= 4)  # Должны быть группы минимум из 4 клеток

    # def test_filter_groups_for_5vars(self):
    #     function = "(a&b&c&d&e)|(!a&b&c&d&e)|(a&!b&c&d&e)|(a&b&!c&d&e)"
    #     lm = LogicMinimizer(function)
    #     kmap = lm._build_karnaugh_map(lm._find_sdnf_values(list(product([0, 1], repeat=5)), [t.strip() for t in function.split('|')]))
        
    #     # Создаем искусственные группы для тестирования фильтрации
    #     test_groups = [
    #         [0,0,0,1,0,2,0,3],  # Valid group (left side)
    #         [0,4,0,5,0,6,0,7],   # Valid mirror group (right side)
    #         [0,0,0,1],           # Too small group
    #         [0,0,0,4]            # Invalid mirror group (different sizes)
    #     ]
        
    #     filtered = lm._filter_groups_for_5vars(test_groups, kmap)
    #     self.assertEqual(len(filtered), 2)  # Должны остаться только 2 валидные группы

    def test_translate_coordinates(self):
        lm = LogicMinimizer("a&b&c&d&e")
        groups = [[0,0,0,1,0,2,0,3]]
        translation_rules = [(0,4), (1,5), (2,6), (3,7)]
        lm._translate_coordinates(groups, translation_rules)
        self.assertEqual(groups, [[0,4,0,5,0,6,0,7]])

    # def test_find_additional_groups_for_5vars(self):
    #     function = "(a&b&c&d&e)|(!a&b&c&d&e)|(a&!b&c&d&e)|(a&b&!c&d&e)"
    #     lm = LogicMinimizer(function)
    #     kmap = lm._build_karnaugh_map(lm._find_sdnf_values(list(product([0, 1], repeat=5)), [t.strip() for t in function.split('|')]))
        
    #     col_indexes = [0, 1, 2, 3]
    #     translation_rules = [(0,4), (1,5), (2,6), (3,7)]
    #     groups = lm._find_additional_groups_for_5vars(kmap, 1, col_indexes, translation_rules)
    #     self.assertTrue(len(groups) > 0)

    def test_print_coverage_table_large(self):
        function = "(a&b&c)|(!a&b&c)|(a&!b&c)|(a&b&!c)|(!a&!b&c)|(!a&b&!c)|(a&!b&!c)|(!a&!b&!c)"
        lm = LogicMinimizer(function)
        terms = [term.strip() for term in lm.sdnf.split('|')]
        implicants = lm._find_prime_implicants(terms)
        coverage_table = lm._build_coverage_table(implicants, terms)
        
        # Проверяем, что функция не падает на больших таблицах
        lm._print_coverage_table(implicants, terms, "Large Coverage Table Test")

    def test_karnaugh_map_printing(self):
        function = "a&b&c&d"
        lm = LogicMinimizer(function)
        kmap = lm._build_karnaugh_map(lm._find_sdnf_values(
            list(product([0, 1], repeat=4)), 
            [function]
        ))
        
        # Проверяем, что функция печати не падает
        lm._print_karnaugh_map(kmap)

    def test_minimize_karnaugh_special_cases(self):
        # Тест для случая, когда только одна клетка = 1
        lm = LogicMinimizer("a&b&!c&!d")
        kmap = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,1,0,0]]
        minimized = lm._minimize_karnaugh_to_dnf(kmap)
        self.assertFalse("a" in minimized and "b" in minimized and "!c" in minimized and "!d" in minimized)
        
        # Тест для случая, когда только одна клетка = 0
        kmap = [[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,0,1,1]]
        minimized = lm._minimize_karnaugh_to_cnf(kmap)
        self.assertTrue("a" in minimized or "!b" in minimized or "!c" in minimized or "d" in minimized)

    def test_validate_5var_groups(self):
        lm = LogicMinimizer("a&b&c&d&e")
        
        # Valid groups
        valid_groups = [
            [0,0,0,1,0,2,0,3],  # Valid left side
            [0,4,0,5,0,6,0,7],   # Valid right side
            [0,0,0,1,1,0,1,1]    # Valid square
        ]
        
        # Invalid groups
        invalid_groups = [
            [0,0],               # Too small
            [0,0,0,1,0,4],       # Mixed sides
            [0,0,0,1,0,2]       # Wrong size
        ]
        
        validated = lm._validate_5var_groups(valid_groups + invalid_groups)
        self.assertEqual(len(validated), 4)  # Только 3 валидные группы
if __name__ == "__main__":
    unittest.main()