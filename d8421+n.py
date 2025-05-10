from minimizer2 import *

class Formater():
    def __init__(self):
        self.truth_table()
        self.extend_truth_table()
        self.show_table()
        self.build_and_minimize_sdnf()
        
    def get_binary(self, value, length) -> str:
        result_direct_binary = ''
        abs_value = abs(value)
        while abs_value > 0:
            result_direct_binary = str(abs_value % 2) + result_direct_binary
            abs_value = abs_value // 2 
        if len(result_direct_binary) < length:
            result_direct_binary = result_direct_binary.zfill(length)
        return result_direct_binary
    
    def show_table(self):
        
        header = " ".join([row[0].ljust(3) for row in self.table])
        print(header)
        
        
        for i in range(1, len(self.table[0])):
            row_data = []
            for j in range(len(self.table)):
                row_data.append(str(self.table[j][i]).ljust(3))
            print(" ".join(row_data))
       
    def truth_table(self):
        self.letters_list = ["1", "2", "3", "4"]
        self.table = []
        for i in range(0, 4, 1):
            self.table.append([0] * (pow(2, 4) + 1))
            self.table[i][0] = self.letters_list[i]
            
        for i in range(0, pow(2, 4), 1):
            binary_value = self.get_binary(i, 4)
            for j in range(0, 4, 1):
                self.table[j][i + 1] = binary_value[j]
        
    def extend_truth_table(self):
        self.letters_list1 = ["y1", "y2", "y3", "y4"]
        for i in range(4, 8, 1):
            self.table.append([0] * 17)
            self.table[i][0] = self.letters_list1[i - 4]

        for i in range(0, pow(2, 4), 1):
            if i < 10:
                binary_value = self.get_binary(i + 4, 4)
                for j in range(4, 8, 1):
                    self.table[j][i + 1] = binary_value[j - 4]
            else:
                for j in range(4, 8, 1):
                    self.table[j][i + 1] = "-"
    
    
    def build_sdnf(self, y_number):
        sdnf = []
        for stroka_number in range(0, 10, 1):
            if self.table[4 + y_number][stroka_number + 1] == "1":
                for stolbik_number in range(0, 4, 1):
                    if self.table[stolbik_number][stroka_number + 1] == "0":
                        sdnf.append("!")
                    sdnf.append(self.table[stolbik_number][0])
                    sdnf.append("&")
                sdnf.pop()
                sdnf.append("|")
        if sdnf != []:
            sdnf.pop()
            sdnf_str = ''
            for i in range(0, len(sdnf), 1):
                sdnf_str += sdnf[i]
        else:
            sdnf_str = 0
        return str(sdnf_str)             
    
    def build_and_minimize_sdnf(self):
        print("СДНФ для y1:\n")
        print(self.build_sdnf(0))
        minimizer = LogicMinimizer1(self.build_sdnf(0))
        print("Минимизация СДНФ для y1: \n")
        print(minimizer.minimize_sdnf_karnaugh())
        
        print("СДНФ для y2:\n")
        print(self.build_sdnf(1))
        minimizer = LogicMinimizer1(self.build_sdnf(1))
        print("Минимизация СДНФ для y2: \n")
        print(minimizer.minimize_sdnf_karnaugh())
        
        print("СДНФ для y3:\n")
        print(self.build_sdnf(2))
        minimizer = LogicMinimizer1(self.build_sdnf(2))
        print("Минимизация СДНФ для y3: \n")
        print(minimizer.minimize_sdnf_karnaugh())
        
        print("СДНФ для y4:\n")
        print(self.build_sdnf(3))
        minimizer = LogicMinimizer1(self.build_sdnf(3))
        print("Минимизация СДНФ для y4: \n")
        print(minimizer.minimize_sdnf_karnaugh())
        
if __name__ == "__main__":
    formater = Formater()
