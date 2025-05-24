import random
class DiagonalMatrixProcessor:
    def __init__(self, matrix):
        self.matrix = matrix
        self.rows = len(matrix)
        self.cols = len(matrix[0]) if self.rows > 0 else 0
    
    
    def _f5(self,x1, x2):
        return x2
    
    
    def _f10(self,x1, x2):
        return "".join(str(1-int(i)) for i in x2)
    
    
    def _f0(self,x1, x2):
    
        return "".join("0" for i in range(self.rows))
    
    
    def _f15(self,x1, x2):
        return "".join("1" for i in range(self.rows))
    
    def _do_function(self,code_1,code_2,code_res,func_code, tag ):
        if tag=="word":
            x1=self._get_word(code_1)
            x2=self._get_word(code_2)
            match func_code:
                case "5": 
                    result=self._f5(x1,x2)
                case "10":
                    result=self._f10(x1,x2)
                case "0":
                    result=self._f0(x1,x2)
                case "15":
                    result=self._f15(x1,x2)
            
            self._set_word(result,code_res)
        elif tag=="column":
            x1=self._get_column(code_1)
            x2=self._get_column(code_2)
            match func_code:
                case "5": 
                    result=self._f5(x1,x2)
                case "10":
                    result=self._f10(x1,x2)
                case "0":
                    result=self._f0(x1,x2)
                case "15":
                    result=self._f15(x1,x2)
            self._set_column(code_res,result)
            
    
   
    def  _get_word(self,code):
        column = [self.matrix[i][code] for i in range(self.rows)]
        lower = column[code:]
        upper = column[:code]
        result = lower + upper
        return ''.join(str(x) for x in result)
    
    def  _get_column (self,code):
        return ''.join(str(self.matrix[(i + code) % self.rows][i])
                for i in range(self.rows))
        
    def  _set_word(self,new_column, code):
        lower = str(new_column)[:(self.rows-int(code))]
        upper = str(new_column)[(self.rows-int(code)):]
        result = upper+lower
        for i in  range(self.rows):
            self.matrix[i][code]=result[i]
            
    def  _set_column (self,code,new_str):
        for i in range(self.rows):  
            self.matrix[(i + code) % self.rows][i]= new_str[i]
      
    def binary_sum(self,value1,value2,max_len):
        result=''
        carry=0
        
        for i in range(max_len-1,-1,-1) :
            bit1 = int(value1[i])  
            bit2 = int(value2[i])
            sum_bit=bit1+bit2 +carry
            result =  str(sum_bit % 2) +result
            carry = sum_bit // 2 
        if carry== 1:
            result=str(carry)+result
        if len(result)<max_len+1:
            result="0"+result
        return result               
    
    def field_operations(self,pattern):
        matched_=[]
        for i in range(self.rows):
            current_word=self._get_word(i)
            if current_word.startswith(pattern):
                summ=self.binary_sum(current_word[3:7],current_word[7:11],4)
                current_word=current_word[:self.rows-5]
                current_word=current_word+summ
                matched_.append(current_word)
                self._set_word(current_word,i)
        if matched_==[]:
            print("No matches")
    def display_matrix(self):
       
        print("\nCurrent Matrix:")
        for row in self.matrix:
            print(" ".join(str(x) for x in row))
        print()
    
    def search_by_pattern_match(self, search_pattern):

        results = []
        
        for word_idx in range(self.rows):
            word = self._get_word(word_idx)
            match_count = 0
            
           
            g = [0] * (self.rows + 1)  
            l = [0] * (self.rows + 1)  
            
            
            for i in range(self.rows - 1, -1, -1):
                a_i = int(search_pattern[i])
                S_ji = int(word[i])
               
                g[i] = g[i+1] or ((1 - a_i) and S_ji and (1 - l[i+1]))
                l[i] = l[i+1] or (a_i and (1 - S_ji) and (1 - g[i+1]))
                
                if a_i == S_ji:
                    match_count += 1
            
           
            if g[0] == 0 and l[0] == 0:
                relation = "exact"
            elif g[0] == 1 and l[0] == 0:
                relation = "greater"
            elif g[0] == 0 and l[0] == 1:
                relation = "less"
            else:
                relation = "error"
            
            results.append((word_idx, match_count, relation))
        
       
        results.sort(key=lambda x: x[1], reverse=True)
        return results

    def display_pattern_match_results(self, search_pattern):
       
        try:
            results = self.search_by_pattern_match(search_pattern)
            
            print(f"\nResults of searching '{search_pattern}':")
            print("Index | Matches | Relation | Word")
            print("-" * 50)
            
            for word_idx, count, relation in results:
                word = self._get_word(word_idx)
                print(f"{word_idx:6} | {count:9} | {relation:8} | {word}")
            
            
            if results:
                max_count = results[0][1]
                best_matches = [r for r in results if r[1] == max_count]
                
                print("\nBest matches:")
                for match in best_matches:
                    word = self._get_word(match[0])
                    print(f"Word {match[0]}: {word} ({match[1]} matches, {match[2]})")
                
              
                exact = [r for r in best_matches if r[2] == "exact"]
                greater = [r for r in best_matches if r[2] == "greater"]
                less = [r for r in best_matches if r[2] == "less"]
                
                if exact:
                    print("\nExact matches was found")
                elif greater:
                    print("\nGreater matches was found")
                elif less:
                    print("\nLess matches was found")
        
        except ValueError as e:
            print(f"Error: {e}")
def create_default_matrix(size=16):
    
     return [[random.randint(0, 1) for _ in range(size)] for _ in range(size)]

def main():
    
    matrix = create_default_matrix()
    processor = DiagonalMatrixProcessor(matrix)
    
    while True:
        print("\nDiagonal Matrix Processor Menu:")
        print("1. Display Matrix")
        print("2. Get Word")
        print("3. Get Column")
        print("4. Set Word")
        print("5. Set Column")
        print("6. Perform Function on Words")
        print("7. Perform Function on Columns")
        print("8. Field Operations")
        print("9. Pattern Search ")
        print("0. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            processor.display_matrix()
            
        elif choice == "2":
            try:
                code = int(input("Enter word index (0-15): "))
                if 0 <= code < processor.rows:
                    word = processor._get_word(code)
                    print(f"Word at index {code}: {word}")
                else:
                    print("Invalid index!")
            except ValueError:
                print("Please enter a valid number!")
                
        elif choice == "3":
            try:
                code = int(input("Enter column index (0-15): "))
                if 0 <= code < processor.cols:
                    column = processor._get_column(code)
                    print(f"Column at index {code}: {column}")
                else:
                    print("Invalid index!")
            except ValueError:
                print("Please enter a valid number!")
                
        elif choice == "4":
            try:
                code = int(input("Enter word index to set (0-15): "))
                if 0 <= code < processor.rows:
                    new_word = input("Enter new word (16 bits): ")
                    if len(new_word) == processor.rows and all(c in '01' for c in new_word):
                        processor._set_word(new_word, code)
                        print("Word updated.")
                        processor.display_matrix()
                    else:
                        print("Invalid word format! Must be 16 bits of 0s and 1s.")
                else:
                    print("Invalid index!")
            except ValueError:
                print("Please enter a valid number!")
                
        elif choice == "5":
            try:
                code = int(input("Enter column index to set (0-15): "))
                if 0 <= code < processor.cols:
                    new_column = input("Enter new column (16 bits): ")
                    if len(new_column) == processor.rows :
                        processor._set_column(code, new_column)
                        print("Column updated.")
                        processor.display_matrix()
                    else:
                        print("Invalid column format! Must be 16 bits of 0s and 1s.")
                else:
                    print("Invalid index!")
            except ValueError:
                print("Please enter a valid number!")
                
        elif choice == "6":
            try:
                code1 = int(input("Enter first word index (0-15): "))
                code2 = int(input("Enter second word index (0-15): "))
                code_res = int(input("Enter result word index (0-15): "))
                func = input("Enter function code (0, 5, 10, 15): ")
                
                if (0 <= code1 < processor.rows and 0 <= code2 < processor.rows and 
                    0 <= code_res < processor.rows and func in ["0", "5", "10", "15"]):
                    processor._do_function(code1, code2, code_res, func, "word")
                    print("Function applied to words.")
                    processor.display_matrix()
                else:
                    print("Invalid input!")
            except ValueError:
                print("Please enter valid numbers!")
                
        elif choice == "7":
            try:
                code1 = int(input("Enter first column index (0-15): "))
                code2 = int(input("Enter second column index (0-15): "))
                code_res = int(input("Enter result column index (0-15): "))
                func = input("Enter function code (0, 5, 10, 15): ")
                
                if (0 <= code1 < processor.cols and 0 <= code2 < processor.cols and 
                    0 <= code_res < processor.cols and func in ["0", "5", "10", "15"]):
                    processor._do_function(code1, code2, code_res, func, "column")
                    print("Function applied to columns.")
                    processor.display_matrix()
                else:
                    print("Invalid input!")
            except ValueError:
                print("Please enter valid numbers!")
                
    
        elif choice == "8":
            pattern = input("Enter pattern to match (binary string): ")
            if all(c in '01' for c in pattern):
                processor.field_operations(pattern)
                print("Field operations applied to matching words.")
                processor.display_matrix()
            else:
                print("Invalid pattern! Only 0s and 1s allowed.")
        elif choice == "9":
            pattern = input("Enter pattern to match: ")
            processor.display_pattern_match_results(pattern)        
        elif choice == "0":
            print("Exiting program.")
            break
            
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()            
                
    