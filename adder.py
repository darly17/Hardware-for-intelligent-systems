from logic_operator import *
from minimizer2 import *
class Adder():
    def __init__(self):
        self.table = []
        self._init_fill_table()
        self.show_table()
        
        
        self.minim=LogicMinimizer1(self.build_sdnf(1))
        print(self.minim.minimize_sdnf_karnaugh())
        
        
        self.minim=LogicMinimizer1(self.build_sdnf(2))
        print(self.minim.minimize_sdnf_karnaugh())
        
        
        self.minim=LogicMinimizer1(self.build_sdnf(3))
        print(self.minim.minimize_sdnf_karnaugh())
        
        
    
    def _init_fill_table(self):
        self.letters_list = ["1", "2", "3", "V", "q1", "q2", "q3", "h1", "h2", "h3"]
        n = 3  
        rows = pow(2, n) * 2  
        
        
        self.table = []
        
        
        for i in range(len(self.letters_list)):
            self.table.append([0] * (rows + 1))
            self.table[i][0] = self.letters_list[i]
        
        
        for i in range(rows // 2):
            binary_value = self.get_binary(i, n)
            for j in range(n):
                self.table[j][i * 2 + 1] = int(binary_value[j])
                self.table[j][i * 2 + 2] = int(binary_value[j])
            self.table[3][i * 2 + 1] = 0  
            self.table[3][i * 2 + 2] = 1  
        
        
        prev_q = [None, None, None]  
        for i in range(1, rows + 1):
            v = self.table[3][i]
            current_q = [0, 0, 0]
            
            if v == 0:
                for j in range(3):
                    current_q[j] = self.table[j][i]
            else:
                
                carry = 1
                for j in [2, 1, 0]:  
                    sum_bit = self.table[j][i] + carry
                    current_q[j] = sum_bit % 2
                    carry = sum_bit // 2
            
            
            for j in range(3):
                self.table[j + 4][i] = current_q[j]
            
            
            if prev_q[0] is not None:  
                for j in range(3):
                    self.table[j + 7][i] = 1 if prev_q[j] != current_q[j] else 0
            
            prev_q = current_q.copy()
    
    def show_table(self):
        
        header = '   '.join(str(col[0]) for col in self.table)
        print(header)
        
        
        for i in range(1, len(self.table[0])):
            row = '    '.join(str(col[i]) for col in self.table)
            print(row)
    
    def get_binary(self, value, length) -> str:
        result_direct_binary = ''
        abs_value= abs(value)
        while abs_value > 0 :
            result_direct_binary= str(abs_value % 2)+result_direct_binary
            abs_value = abs_value // 2 
        if len(result_direct_binary)<length:
            result_direct_binary=result_direct_binary.zfill(length)
        return result_direct_binary
    def build_sdnf(self,x):
        sdnf=[]
        for stroka_number in range(0,len(self.table[0])-1,1):
            
            if self.table[len(self.table)-x][stroka_number+1]==1:
                for stolbik_number in range(0,4,1):
                    if self.table[stolbik_number][stroka_number+1]== 0:
                        sdnf.append("!")
                    sdnf.append(self.table[stolbik_number][0])
                    sdnf.append("&")
                sdnf.pop()
                sdnf.append("|")
        if sdnf!=[]:
            sdnf.pop()
            sdnf_str=''
            for i in range(0,len(sdnf),1):
                sdnf_str+=sdnf[i]
        else:
            sdnf_str=0
        
        return str(sdnf_str)
  
v = Adder()