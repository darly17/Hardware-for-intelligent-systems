from itertools import product, combinations
from tabulate import tabulate
from logic_operator import *


class LogicMinimizer:
    def __init__(self, function):
        self.logic = Logic_operator(function)
        self.sdnf = self.logic.build_sdnf()
        self.sknf = self.logic.build_sknf()
        self.variables = sorted(self.logic.letters_list)
        self.number_variables = len(self.variables)

    def count_negations(self, term):
        return term.count('!')

    def split_term(self, term):
        vars = []
        i = 0
        while i < len(term):
            if term[i] == '&' or term[i] == '|':
                i += 1
                continue
            if term[i] == '!':
                vars.append(term[i:i + 2])
                i += 2
            else:
                vars.append(term[i])
                i += 1
        return vars

    def merge(self, term1, term2):
        vars1 = self.split_term(term1)
        vars2 = self.split_term(term2)
        if len(vars1) != len(vars2):
            return False, None
        diff = 0
        merged = []
        for variable1, variable2 in zip(vars1, vars2):
            if variable1 == variable2:
                merged.append(variable1)
            else:
                diff += 1
                merged.append('-')

        return diff == 1, '&'.join(
            merged) if '&' in term1 else '|'.join(merged)

    def is_covered(self, term1, term2):
        vars1 = self.split_term(term1)
        vars2 = self.split_term(term2)
        for var1, var2 in zip(vars1, vars2):
            if var2 != '-' and var1 != var2:
                return False
        return True

    def minimize_sdnf(self):
        
            
        terms = [term.strip() for term in self.sdnf.split('|')]
        print("\n=== Минимизация СДНФ методом Квайна ===")
        print("Исходная СДНФ:", " | ".join(terms))
        final_terms = []
        iteration = 1

        while True:
            print(f"\n=== Стадия склеивания {iteration} ===")
            groups = {}
            for term in terms:
                group_num = self.count_negations(term)
                if group_num not in groups:
                    groups[group_num] = []
                groups[group_num].append(term)

            print("\nГруппировка термов:")
            for group_num, group in sorted(groups.items()):
                print(f"Группа {group_num}: {group}")

            sorted_groups = sorted(groups.items())
            merged_terms = set()
            new_terms = []
            merge_found = False

            print("\nРезультаты склеивания:")
            for i in range(len(sorted_groups) - 1):
                group_num1, group1 = sorted_groups[i]
                group_num2, group2 = sorted_groups[i + 1]

                if group_num2 - group_num1 != 1:
                    continue

                for term1 in group1:
                    for term2 in group2:
                        can, merged = self.merge(term1, term2)
                        if can:
                            merge_found = True
                            merged_terms.add(term1)
                            merged_terms.add(term2)
                            if merged not in new_terms:
                                new_terms.append(merged)
                                print(f"{term1} + {term2} -> {merged}")

            for term in terms:
                if term not in merged_terms and term not in new_terms:
                    new_terms.append(term)

            if not merge_found:
                print("\nСклеивание завершено")
                final_terms = terms.copy()
                break

            terms = new_terms
            iteration += 1

            print("\nТермы после склеивания:")
            print(" | ".join(terms))

            unique_terms = []
            for term in terms:
                if term not in unique_terms:
                    unique_terms.append(term)

            final_terms = []
            for i in range(len(unique_terms)):
                is_redundant = False
                for j in range(len(unique_terms)):
                    if i != j and self.is_covered(
                            unique_terms[i], unique_terms[j]):
                        is_redundant = True
                        break
                if not is_redundant:
                    final_terms.append(unique_terms[i])
            if not final_terms:
                final_terms = unique_terms.copy()

        print("\n=== Результат минимизации СДНФ ===")
        if final_terms:
            result= " | ".join(final_terms)
            result = result.replace("-&", "")
            return result
        else:
            return "0"
        

    def minimize_sknf(self):
        terms = [term.strip() for term in self.sknf.split('&')]
        print("\n=== Минимизация СКНФ методом Квайна ===")
        print("Исходная СКНФ:", " & ".join(terms))
        final_terms = []
        iteration = 1

        while True:
            print(f"\n=== Стадия склеивания {iteration} ===")
            groups = {}
            for term in terms:
                group_num = self.count_negations(term)
                if group_num not in groups:
                    groups[group_num] = []
                groups[group_num].append(term)

            print("\nГруппировка термов:")
            for group_num, group in sorted(groups.items()):
                print(f"Группа {group_num}: {group}")

            sorted_groups = sorted(groups.items())
            merged_terms = set()
            new_terms = []
            merge_found = False

            print("\nРезультаты склеивания:")
            for i in range(len(sorted_groups) - 1):
                group_num1, group1 = sorted_groups[i]
                group_num2, group2 = sorted_groups[i + 1]

                if group_num2 - group_num1 != 1:
                    continue

                for term1 in group1:
                    for term2 in group2:
                        can, merged = self.merge(term1, term2)
                        if can:
                            merge_found = True
                            merged_terms.add(term1)
                            merged_terms.add(term2)
                            if merged not in new_terms:
                                new_terms.append(merged)
                                print(f"{term1} + {term2} -> {merged}")

            for term in terms:
                if term not in merged_terms and term not in new_terms:
                    new_terms.append(term)

            if not merge_found:
                print("\nСклеивание завершено")
                final_terms = terms.copy()
                break

            terms = new_terms
            iteration += 1

            print("\nТермы после склеивания:")
            print(" & ".join(terms))

            unique_terms = []
            for term in terms:
                if term not in unique_terms:
                    unique_terms.append(term)

            final_terms = []
            for i in range(len(unique_terms)):
                is_redundant = False
                for j in range(len(unique_terms)):
                    if i != j and self.is_covered(
                            unique_terms[i], unique_terms[j]):
                        is_redundant = True
                        break
                if not is_redundant:
                    final_terms.append(unique_terms[i])
            if not final_terms:
                final_terms = unique_terms.copy()

        print("\n=== Результат минимизации СКНФ ===")
        if final_terms:
            result= " & ".join(final_terms)
            result = result.replace("-|", "")
            return result
        else:
            return "1"

    def minimize_sknf_table_method(self):
        terms = [term.strip() for term in self.sknf.split('&')]
        terms = list(set(terms))
        
        if not terms:
            return "1"
        
        print("\n=== Минимизация СКНФ расчетно-табличным методом ===")
        print(f"Исходных термов: {len(terms)}")
        print("Исходная СКНФ:", " & ".join(terms))
        
        prime_implicants = self._find_prime_implicants(terms, is_dnf=False)
        print(f"\nВсего простых импликант: {len(prime_implicants)}")
        
        coverage_table = self._build_coverage_table(prime_implicants, terms)
        self._print_coverage_table(prime_implicants, terms, "Таблица покрытий СКНФ")
        
        core_implicants = self._find_core_implicants(coverage_table, prime_implicants, terms)
        print(f"\nЯдровые импликанты ({len(core_implicants)}):")
        for imp in core_implicants:
            print(f"- {imp}")
        
        minimal_cover = self._find_minimal_cover(terms, prime_implicants, core_implicants, coverage_table)
        result= " & ".join(minimal_cover)

        result = result.replace("-|", "")
        print("\n=== Результат минимизации СКНФ ===")
        return result

    def minimize_sdnf_table_method(self):
        terms = [term.strip() for term in self.sdnf.split('|')]
        if not terms:
            return "0"

        print(f"Исходных термов: {len(terms)}")
        print("Исходная СДНФ:", " | ".join(terms))

        prime_implicants = self._find_prime_implicants(terms)
        print(f"\nВсего простых импликант: {len(prime_implicants)}")

        coverage_table = self._build_coverage_table(prime_implicants, terms)
        self._print_coverage_table(
            prime_implicants, terms, "Таблица покрытий СДНФ")

        core_implicants = self._find_core_implicants(
            coverage_table, prime_implicants, terms)
        print(f"\nЯдровые импликанты ({len(core_implicants)}):")
        for imp in core_implicants:
            print(f"- {imp}")

        minimal_cover = self._find_minimal_cover(
            terms, prime_implicants, core_implicants, coverage_table)
        
        result= " | ".join(minimal_cover)

        result = result.replace("-&", "")

        print("\n=== Результат минимизации СДНФ ===")
        return  result
    
    def _find_prime_implicants(self, terms, is_dnf=True):
        prime_implicants = set()
        current_terms = terms.copy()
        iteration = 1

        while True:
            print(f"\n=== Стадия склеивания {iteration} ===")
            new_terms = []
            merged_terms = set()
            merge_found = False


            groups = {}
            for term in current_terms:
                group_num = self.count_negations(term)
                if group_num not in groups:
                    groups[group_num] = []
                groups[group_num].append(term)

            print("\nГруппировка термов:")
            for group_num, group in sorted(groups.items()):
                print(f"Группа {group_num}: {group}")

            sorted_groups = sorted(groups.items())
            print("\nРезультаты склеивания:")
            for i in range(len(sorted_groups) - 1):
                group_num1, group1 = sorted_groups[i]
                group_num2, group2 = sorted_groups[i + 1]

                if group_num2 - group_num1 != 1:
                    continue

                for term1 in group1:
                    for term2 in group2:
                        can_merge, merged = self.merge(term1, term2)
                        merged = merged
                        if can_merge:
                            merge_found = True
                            merged_terms.add(term1)
                            merged_terms.add(term2)
                            if merged not in new_terms:
                                new_terms.append(merged)
                                print(f"{term1} + {term2} -> {merged}")

            for term in current_terms:
                if term not in merged_terms:
                    prime_implicants.add(term)

            if not merge_found:
                print("\nСклеивание завершено")
                break

            current_terms = new_terms
            iteration += 1

        print("\nВсе простые импликанты:")
        for imp in prime_implicants:
            print(f"- {imp}")

        return list(prime_implicants)

    def _build_coverage_table(self, implicants, terms):
        return [
            [1 if self.is_covered(term, imp) else 0
             for term in terms]
            for imp in implicants
        ]

    def _find_core_implicants(self, coverage_table, implicants, terms):
        core = []
        print("\nПоиск ядровых импликант:")
        for j in range(len(terms)):
            column = [row[j] for row in coverage_table]
            if sum(column) == 1:
                index = column.index(1)
                if implicants[index] not in core:
                    core.append(implicants[index])
                    print(
                        f"Терм {
                            terms[j]} покрывается только {
                            implicants[index]} -> ядровая"
                            )
        return core

    def _find_minimal_cover(self, terms, implicants,
                            core_implicants, coverage_table):
        covered_terms = set()
        core_indices = [implicants.index(imp) for imp in core_implicants]

        for i in core_indices:
            for j in range(len(terms)):
                if coverage_table[i][j] == 1:
                    covered_terms.add(j)

        remaining_terms = [
            j for j in range(
                len(terms)) if j not in covered_terms]
        if not remaining_terms:
            print("\nВсе термы покрыты ядровыми импликантами")
            return core_implicants

        print(f"\nОсталось покрыть {len(remaining_terms)} термов:")
        for j in remaining_terms:
            print(f"- {terms[j]}")

        additional_implicants = []
        remaining_terms_set = set(remaining_terms)
        available_imps = [i for i in range(len(implicants))
                          if implicants[i] not in core_implicants]

        print("\nДобавление дополнительных импликант:")
        while remaining_terms_set:
            best_imp_idx = None
            best_cover = set()

            for i in available_imps:
                cover = {
                    j for j in remaining_terms_set if coverage_table[i][j] == 1}
                if len(cover) > len(best_cover):
                    best_cover = cover
                    best_imp_idx = i

            if best_imp_idx is not None:
                additional_implicants.append(implicants[best_imp_idx])
                print(
                    f"Добавляем {
                        implicants[best_imp_idx]} (покрывает {
                        len(best_cover)} термов)")
                remaining_terms_set -= best_cover
            else:
                break

        return core_implicants + additional_implicants

    def _print_coverage_table(self, implicants, terms, title):
        term_ids = {term: f"T{i + 1}" for i, term in enumerate(terms)}
        imp_ids = {imp: f"I{i + 1}" for i, imp in enumerate(implicants)}

        table_data = []

        if len(terms) < 20:
            for imp in implicants:
                row = [imp_ids[imp], imp]
                row.extend(
                    "×" if self.is_covered(
                        term, imp) else "" for term in terms)
                table_data.append(row)
            headers = ["ID", "Импликанты"] + [term_ids[term] for term in terms]
            print(f"\n{title}")
            print(
                tabulate(
                    table_data,
                    headers=headers,
                    tablefmt="grid",
                    stralign="center"))
        else:
            table_data2 = []
            for imp in implicants:
                row = [imp_ids[imp], imp]
                row.extend("×" if self.is_covered(term, imp)
                           else "" for term in terms[:20])
                table_data.append(row)
            headers = ["ID", "Импликанты"] + [term_ids[term]
                                              for term in terms[:20]]
            print(f"\n{title}")
            print(
                tabulate(
                    table_data,
                    headers=headers,
                    tablefmt="grid",
                    stralign="center"))

            for imp in implicants:
                row = [imp_ids[imp], imp]
                row.extend("×" if self.is_covered(term, imp)
                           else "" for term in terms[20:])
                table_data2.append(row)
            headers = ["ID", "Импликанты"] + [term_ids[term]
                                              for term in terms[20:]]
            print(f"\n{title}")
            print(
                tabulate(
                    table_data2,
                    headers=headers,
                    tablefmt="grid",
                    stralign="center"))

        print("\nПояснения:")
        for i, term in enumerate(terms):
            print(f"{term_ids[term]} = {term}")


    def minimize_sdnf_karnaugh(self):
        terms = [term.strip() for term in self.sdnf.split('|')]
        if not terms or terms[0] == '':
            return "0"

        print("\n=== Минимизация СДНФ методом Карно ===")
        print("Исходная СДНФ:", " | ".join(terms))

        if self.number_variables > 5:
            print("Поддерживается до 5 переменных")
            return " | ".join(terms)

        cases = list(product([0, 1], repeat=self.number_variables))

        case_values = self._find_sdnf_values(cases, terms)

        karnaugh_map = self._build_karnaugh_map(case_values)
        self._print_karnaugh_map(karnaugh_map)

        minimized = self._minimize_karnaugh_to_dnf(
            karnaugh_map)
        return minimized

    def minimize_sknf_karnaugh(self):
        terms = [term.strip() for term in self.sknf.split('&')]
        if not terms or terms[0] == '':
            return "1"

        print("Исходная СКНФ:", " & ".join(terms))
        if self.number_variables > 5:
            print("Поддерживается до 5 переменных")
            return " & ".join(terms)

        cases = list(product([0, 1], repeat=self.number_variables))

        case_values = self._find_sknf_values(cases, terms)

        karnaugh_map = self._build_karnaugh_map(case_values)
        self._print_karnaugh_map(karnaugh_map)

        minimized = self._minimize_karnaugh_to_cnf(
            karnaugh_map)
        return minimized

    def _find_sdnf_values(self, cases, terms):
        results = {}
        for case in cases:
            case_satisfied = False
            for term in terms:
                term_satisfied = True
                vars_in_term = self.split_term(term)
                for var in vars_in_term:
                    if var[0] == '!':
                        var_name = var[1]
                        var_index = self.variables.index(var_name)
                        if case[var_index] != 0:
                            term_satisfied = False
                            break
                    else:
                        var_name = var
                        var_index = self.variables.index(var_name)
                        if case[var_index] != 1:
                            term_satisfied = False
                            break
                if term_satisfied:
                    case_satisfied = True
                    break
            results[tuple(case)] = 1 if case_satisfied else 0
        return results

    def _find_sknf_values(self, cases, terms):

        results = {}
        for case in cases:
            case_satisfied = True
            for term in terms:
                term_satisfied = False
                vars_in_term = self.split_term(term)
                for var in vars_in_term:
                    if var[0] == '!':
                        var_name = var[1]
                        var_index = self.variables.index(var_name)
                        if case[var_index] == 0:
                            term_satisfied = True
                            break
                    else:
                        var_name = var
                        var_index = self.variables.index(var_name)
                        if case[var_index] == 1:
                            term_satisfied = True
                            break
                if not term_satisfied:
                    case_satisfied = False
                    break
            results[tuple(case)] = 1 if case_satisfied else 0
        return results

    def _build_karnaugh_map(self, case_values):
        rows, cols = self.get_dimensions()
        karnaugh_map = [[0 for _ in range(cols)] for _ in range(rows)]

        for case, value in case_values.items():
            row = self._row_index(case)
            column = self._column_index(case)
            karnaugh_map[row][column] = value

        return karnaugh_map

    def get_dimensions(self):
        if self.number_variables == 1:
            return (1, 2)
        elif self.number_variables == 2:
            return (2, 2)
        elif self.number_variables == 3:
            return (2, 4)
        elif self.number_variables == 4:
            return (4, 4)
        elif self.number_variables == 5:
            return (4, 8)
        else:
            raise ValueError("Поддерживается до 5 переменных")

    def _row_index(self, case):
        if self.number_variables == 1:
            return 0
        elif self.number_variables == 2:
            return case[0]
        elif self.number_variables == 3:
            return case[0]
        elif self.number_variables == 4 or self.number_variables == 5:
            first_bit = case[0]
            next_bit = case[1]
            gray_code = (first_bit << 1) | next_bit
            gray_order = [0, 1, 3, 2]
            return gray_order.index(gray_code)
        else:
            raise ValueError("Unsupported number of variables")

    def _column_index(self, case):
        if self.number_variables == 1:
            return case[0]
        elif self.number_variables == 2:
            return case[1]
        elif self.number_variables == 3:
            first_bit = case[1]
            next_bit = case[2]
            binary_value = (first_bit << 1) | next_bit
            gray_order = [0, 1, 3, 2]
            return gray_order.index(binary_value)
        elif self.number_variables == 4:
            first_bit = case[2]
            second_bit = case[3]
            binary_value = (first_bit << 1) | second_bit
            gray_order = [0, 1, 3, 2]
            return gray_order.index(binary_value)
        elif self.number_variables == 5:
            first_bit = case[2]
            second_bit = case[3]
            next_bit = case[4]
            binary_value = (first_bit << 2) | (second_bit << 1) | next_bit
            gray_order = [0, 1, 3, 2, 6, 7, 5, 4]
            return gray_order.index(binary_value)
        else:
            raise ValueError("Unsupported number of variables")

    def _print_karnaugh_map(self, kmap):
        print("\nКарта Карно:")

        if self.number_variables == 1:
            row_vars = ""
            col_vars = self.variables[0]
        elif self.number_variables == 2:
            row_vars = self.variables[0]
            col_vars = self.variables[1]
        elif self.number_variables == 3:
            row_vars = self.variables[0]
            col_vars = f"{self.variables[1]}{self.variables[2]}"
        elif self.number_variables == 4:
            row_vars = f"{self.variables[0]}{self.variables[1]}"
            col_vars = f"{self.variables[2]}{self.variables[3]}"
        elif self.number_variables == 5:
            row_vars = f"{self.variables[0]}{self.variables[1]}"
            col_vars = f"{
                self.variables[2]}{
                self.variables[3]}{
                self.variables[4]}"
        else:
            row_vars = ""
            col_vars = ""

        cols = len(kmap[0])
        if cols == 2:
            gray_headers = ["0", "1"]
        elif cols == 4:
            gray_headers = ["00", "01", "11", "10"]
        elif cols == 8:
            gray_headers = [
                "000",
                "001",
                "011",
                "010",
                "110",
                "111",
                "101",
                "100"]
        else:
            gray_headers = [str(i) for i in range(cols)]

        rows = len(kmap)
        if rows == 2:
            gray_row_headers = ["0", "1"]
        elif rows == 4:
            gray_row_headers = ["00", "01", "11", "10"]
        else:
            gray_row_headers = [str(i) for i in range(rows)]

        table_data = []
        for i in range(rows):
            row_data = [gray_row_headers[i]] + kmap[i]
            table_data.append(row_data)

        headers = [f"{row_vars}\\{col_vars}"] + gray_headers

        print(
            tabulate(
                table_data,
                headers=headers,
                tablefmt="grid",
                stralign="center"))
 
    def _find_mirror_groups_5vars(self, kmap, target_value):
        mirror_groups = []
        left_cols = [0, 1, 2, 3]
        right_cols = [4, 5, 6, 7]
        
        
        for row in range(4):
            for left_col in left_cols:
                right_col = left_col + 4
                if (kmap[row][left_col] == target_value and 
                    kmap[row][right_col] == target_value):
                    
                    mirror_groups.append([row, left_col, row, right_col])
        
        
        merged_groups = []
        used = set()
        
        for i, group1 in enumerate(mirror_groups):
            if i in used:
                continue
            merged = group1.copy()
            
            for j, group2 in enumerate(mirror_groups[i+1:], i+1):
                if j in used:
                    continue
                
                if (group1[0] == group2[0] and  
                    group1[1] == group2[1] - 1 and  
                    group1[3] == group2[3] - 1):    
                    merged.extend([group2[2], group2[3]])
                    used.add(j)
            
            merged_groups.append(merged)
        
        return merged_groups

    def _validate_5var_groups(self, groups):
        valid_groups = []
        
        for group in groups:
            cols = {group[i+1] for i in range(0, len(group), 2)}
            rows = {group[i] for i in range(0, len(group), 2)}
            
            
            left_cols = {c for c in cols if c < 4}
            right_cols = {c for c in cols if c >= 4}
            
            if left_cols and right_cols:
               
                if len(left_cols) == len(right_cols) and self._is_power_of_2(len(rows)):
                    valid_groups.append(group)
            else:
                
                if self._is_power_of_2(len(cols)) and self._is_power_of_2(len(rows)):
                    valid_groups.append(group)
        
        return valid_groups
    def _find_karnaugh_groups(self, kmap, target_value, number):
        rows = len(kmap)
        cols = len(kmap[0])
        groups = []
        unique_groups = set()

        dimensions = self._get_possible_group_sizes(rows, cols)

        for hight, width in dimensions:
            start_rows = [0] if hight == rows else list(range(rows))

            for starting_row in start_rows:
                for column in range(cols):
                    cells = []
                    is_valid = True

                    for row in range(starting_row, starting_row + hight):
                        current_row = row % rows
                        for i in range(width):
                            current_col = (column + i) % cols
                            if kmap[current_row][current_col] != target_value:
                                is_valid = False
                                break
                            cells.append((current_row, current_col))
                        if not is_valid:
                            break

                    if is_valid and cells:

                        sorted_cells = sorted(cells)
                        key = ",".join(f"{row},{column}" for row, column in sorted_cells)

                        
                        if key not in unique_groups:
                            unique_groups.add(key)

                            flat_group = []
                            for row, column in sorted_cells:
                                flat_group.append(row)
                                flat_group.append(column)
                            groups.append(flat_group)
                        

        if number== 5:
            groups.extend(
                self._find_additional_groups_for_5vars(
                    kmap, target_value, [
                        0, 3, 4, 7], [
                        (0, 0), (1, 3), (2, 4), (3, 7)]))
            groups.extend(
                self._find_additional_groups_for_5vars(
                    kmap, target_value, [
                        1, 2, 5, 6], [
                        (0, 1), (1, 2), (2, 5), (3, 6)]))
        print("uheggs",groups)
        return self._filter_groups(groups, kmap, target_value)
    def _find_additional_groups_for_5vars(
            self, kmap, target_value, col_indexes, translation_rules):
        sub_kmap = [[0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                sub_kmap[j][i] = kmap[j][col_indexes[i]]

        groups = self._find_karnaugh_groups(sub_kmap, target_value, 4)
        self._translate_coordinates(groups, translation_rules)
        return groups

    def _translate_coordinates(self, groups, translation_rules):
        for group in groups:
            for i in range(1, len(group), 2):
                col = group[i]
                for src, dst in translation_rules:
                    if col == src:
                        group[i] = dst
                        break

    def _get_possible_group_sizes(self, rows, cols):
        sizes = []
        row_sizes = [1] if rows == 1 else [1, 2, 4]
        row_sizes = [x for x in row_sizes if x <= rows]
        col_sizes = [1, 2, 4, 8]
        col_sizes = [x for x in col_sizes if x <= cols]

        for row in row_sizes:
            for col in col_sizes:
                if row * col >= 1:
                    sizes.append((row, col))
        return sizes

    def _filter_groups(self, groups, kmap, target_value):
        groups.sort(key=lambda group: len(group), reverse=True)

        filtered_groups = []
        covered_cells = set()

        for group in groups:

            group_cells = set()
            for i in range(0, len(group), 2):
                group_cells.add((group[i], group[i + 1]))

            if not group_cells.issubset(covered_cells):
                filtered_groups.append(group)
                covered_cells.update(group_cells)

        if self.number_variables== 5:
            filtered_groups = self._filter_groups_for_5vars(
                filtered_groups, kmap)

        final_groups = []
        for i, group in enumerate(filtered_groups):
            group_cells = set((group[j], group[j + 1])
                              for j in range(0, len(group), 2))
            other_cells = set()
            for j, other_group in enumerate(filtered_groups):
                if i != j:
                    other_cells.update(
                        (other_group[k], other_group[k + 1]) for k in range(0, len(other_group), 2))

            if not group_cells.issubset(other_cells):
                final_groups.append(group)
                
        print("/", final_groups)
        return final_groups

    def _filter_groups_for_5vars(self, groups, kmap):
        valid_groups = []
        
        for group in groups:
            cols = set(group[i] for i in range(1, len(group), 2))
            rows = set(group[i] for i in range(0, len(group), 2))

           
            left_cols = {column for column in cols if column < 4}
            right_cols = {column for column in cols if column >= 4}

            
            if left_cols and right_cols:
                
                if (self._is_power_of_2(len(left_cols)) and 
                    self._is_power_of_2(len(right_cols)) and 
                    self._is_power_of_2(len(rows)) and 
                    len(left_cols) == len(right_cols)):
                    valid_groups.append(group)
            else:
                
                if self._is_power_of_2(len(cols)) and self._is_power_of_2(len(rows)):
                    valid_groups.append(group)
        
       
        final_groups = []
        covered = set()
        
       
        valid_groups.sort(key=lambda g: -len(g))
        
        for group in valid_groups:
            group_cells = {(group[i], group[i+1]) for i in range(0, len(group), 2)}
            if not group_cells.issubset(covered):
                final_groups.append(group)
                covered.update(group_cells)
        
        return final_groups

    def _is_power_of_2(self, value):
        return (value > 0 and (value & (value - 1)) == 0) or value==1

    def _minimize_karnaugh_to_dnf(self, kmap):
        
        ones_count = sum(sum(row) for row in kmap)
        total_cells = len(kmap) * len(kmap[0])
        
        
        if ones_count == total_cells - 1:
            
            zero_pos = None
            for i, row in enumerate(kmap):
                for j, val in enumerate(row):
                    if val == 0:
                        zero_pos = (i, j)
                        break
                if zero_pos:
                    break
                    
            if zero_pos:
                
                row, col = zero_pos
                values = self._get_variable_val(row, col)
                
                term_parts = []
                for var, val in zip(self.variables, values):
                    term_parts.append(f"!{var}" if val else var)
                return " | ".join(term_parts)
        
        
        groups = self._find_karnaugh_groups(kmap, 1, self.number_variables)
        terms = []
        
        for group in groups:
            var_values = [set() for _ in range(self.number_variables)]
            for i in range(0, len(group), 2):
                row = group[i]
                col = group[i + 1]
                values = self._get_variable_val(row, col)
                for j in range(self.number_variables):
                    var_values[j].add(values[j])
            
            term_parts = []
            for j in range(self.number_variables):
                if len(var_values[j]) == 1:
                    val = var_values[j].pop()
                    term_parts.append(self.variables[j] if val else f"!{self.variables[j]}")
            
            if term_parts:
                terms.append("(" + " & ".join(term_parts) + ")")
        
        return " | ".join(terms) if terms else "0"

    def _minimize_karnaugh_to_cnf(self, kmap):
        
        zeros_count = sum(sum(1 for val in row if val == 0) for row in kmap)
        total_cells = len(kmap) * len(kmap[0])
        
       
        if zeros_count == total_cells - 1:
            
            one_pos = None
            for i, row in enumerate(kmap):
                for j, val in enumerate(row):
                    if val == 1:
                        one_pos = (i, j)
                        break
                if one_pos:
                    break
                    
            if one_pos:
                
                row, col = one_pos
                values = self._get_variable_val(row, col)
                
                term_parts = []
                for var, val in zip(self.variables, values):
                    term_parts.append(var if val else f"!{var}")
                return " & ".join(term_parts)
        
        
        groups = self._find_karnaugh_groups(kmap, 0, self.number_variables)
        terms = []
        
        for group in groups:
            var_values = [set() for _ in range(self.number_variables)]
            for i in range(0, len(group), 2):
                row = group[i]
                col = group[i + 1]
                values = self._get_variable_val(row, col)
                for j in range(self.number_variables):
                    var_values[j].add(values[j])
            
            term_parts = []
            for j in range(self.number_variables):
                if len(var_values[j]) == 1:
                    val = var_values[j].pop()
                    term_parts.append(f"!{self.variables[j]}" if val else self.variables[j])
            
            if term_parts:
                terms.append("(" + " | ".join(term_parts) + ")")
        
        return " & ".join(terms) if terms else "1"
    def _get_variable_val(self, row, col):

        values = []
        if self.number_variables == 1:
            values.append(col)
        elif self.number_variables == 2:
            values.append(row)
            values.append(col)
        elif self.number_variables == 3:
            values.append(row)
            b, c = self._get_bc_from_column(col)
            values.append(b)
            values.append(c)
        elif self.number_variables == 4:
            a, b = self._get_ab_from_row(row)
            values.append(a)
            values.append(b)
            c, d = self._get_cd_from_column(col)
            values.append(c)
            values.append(d)
        elif self.number_variables == 5:
            a, b = self._get_ab_from_row(row)
            values.append(a)
            values.append(b)
            c, d, e = self._get_cde_from_column(col)
            values.append(c)
            values.append(d)
            values.append(e)
        return values

    def _get_ab_from_row(self, row):

        if row == 0:
            return (0, 0)
        if row == 1:
            return (0, 1)
        if row == 2:
            return (1, 1)
        if row == 3:
            return (1, 0)
        raise ValueError("Invalid row index")

    def _get_bc_from_column(self, col):

        if col == 0:
            return (0, 0)
        if col == 1:
            return (0, 1)
        if col == 2:
            return (1, 1)
        if col == 3:
            return (1, 0)
        raise ValueError("Invalid column index")

    def _get_cd_from_column(self, col):
        return self._get_bc_from_column(col)

    def _get_cde_from_column(self, col):
        if col == 0:
            return (0, 0, 0)
        if col == 1:
            return (0, 0, 1)
        if col == 2:
            return (0, 1, 1)
        if col == 3:
            return (0, 1, 0)
        if col == 4:
            return (1, 1, 0)
        if col == 5:
            return (1, 1, 1)
        if col == 6:
            return (1, 0, 1)
        if col == 7:
            return (1, 0, 0)
        raise ValueError("Invalid column index")


if __name__ == "__main__":
    function = input("Введите логическую функцию: ")
    minimizer = LogicMinimizer(function)
    
    while True:
        print("\n=== Меню выбора метода минимизации ===")
        print("1. Минимизация СДНФ расчетным методом")
        print("2. Минимизация СКНФ расчетным методом")
        print("3. Минимизация СДНФ расчетно-табличным методом")
        print("4. Минимизация СКНФ расчетно-табличным методом")
        print("5. Минимизация СДНФ методом карт Карно")
        print("6. Минимизация СКНФ методом карт Карно")
        print("0. Выход")
        
        choice = input("Выберите метод (0-6): ")
        
        if choice == '1':
            print("\n=== Минимизация СДНФ расчетным методом ===")
            print("Результат:", minimizer.minimize_sdnf())
        elif choice == '2':
            print("\n=== Минимизация СКНФ расчетным методом ===")
            print("Результат:", minimizer.minimize_sknf())
        elif choice == '3':
            print("\n=== Минимизация СДНФ расчетно-табличным методом ===")
            print("Результат:", minimizer.minimize_sdnf_table_method())
        elif choice == '4':
            print("\n=== Минимизация СКНФ расчетно-табличным методом ===")
            print("Результат:", minimizer.minimize_sknf_table_method())
        elif choice == '5':
            print("\n=== Минимизация СДНФ методом карт Карно ===")
            print("Результат:", minimizer.minimize_sdnf_karnaugh())
        elif choice == '6':
            print("\n=== Минимизация СКНФ методом карт Карно ===")
            print("Результат:", minimizer.minimize_sknf_karnaugh())
        elif choice == '0':
            print("Выход из программы")
            break
        else:
            print("Неверный выбор. Пожалуйста, введите число от 0 до 6.")