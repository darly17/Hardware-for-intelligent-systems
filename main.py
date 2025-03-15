class Logic_operator:
    def __init__(self,function_str:str):
        self.operations=["&",">","|","!","~"]
        self.alphabet=["a","b","c","d"]
        self.function_str=function_str
        self.letters_list=[]

        for i in self.function_str:
            if (i not in self.operations) & (i not in self.letters_list)&(i in self.alphabet):
                self.letters_list.append(i)
        self.table = []
        #заполняем нулями, пример: [a, 0,0,0,0,0]
        for i in range(0,len(self.letters_list),1):
            self.table.append([0]*(pow(2,len(self.letters_list))+1))
            self.table[i][0]=self.letters_list[i]
        

        print(f"Итоговая таблица с переменными:\n{''.join(self.letters_list)}")

        for i in range(0,pow(2,len(self.letters_list)),1):
            binarry_value=self.get_binary(i,len(self.letters_list))
            #print(binarry_value)
            for j in range(0,len(self.letters_list),1):
                self.table[j][i+1]=binarry_value[j]
        print(self.table)

        #create OPZ
        self.turn_into_opz()
        print(f"OPZ:{self.opz_str}")
        #table of all
        self.build_table()
        self.show_table()


  
    def get_binary(self,value,length)->str:
        result_direct_binary = ''
        abs_value= abs(value)
        while abs_value > 0 :
            result_direct_binary= str(abs_value % 2)+result_direct_binary
            abs_value = abs_value // 2 
        if len(result_direct_binary)<length:
            result_direct_binary=result_direct_binary.zfill(length)
        return result_direct_binary


    def turn_into_opz(self):
        def prior(char):
            match char:
                case '>':return 2
                case '&':return 2
                case '|':return 2
                case '~':return 2
                case '!':return 3
                case '(':return 1
            return 0
        stack=[]
        self.opz_str=""
        for char in self.function_str:
            if char =='(' :
                stack.append(char)
            if char==')':
                while(stack[-1]!='('):
                    self.opz_str=self.opz_str+stack[-1]
                    stack.pop()
                stack.pop()
            if char in self.letters_list:
                self.opz_str=self.opz_str+char
            if char in self.operations:
                while stack!=[] and prior(stack[-1])>=prior(char):
                    self.opz_str=self.opz_str+stack[-1]
                    stack.pop()
                stack.append(char)
        while stack!=[]:
            self.opz_str=self.opz_str+stack[-1]
            stack.pop()
        return self.opz_str

    def build_table(self):
        stack=[]
        val_dict={}
        
        for stroka_number in range(1,len(self.table[0]),1):
            count_operations=len(self.letters_list)-1
            for stolbik in range(0,len(self.table),1):
                val_dict[self.table[stolbik][0]]=self.table[stolbik][stroka_number]
            for char in self.opz_str :
                if char in self.letters_list:
                    stack.append(char)
                elif char=='!':
                    op1=int(val_dict[stack[-1]])
                    if op1==1 : 
                        rez = "0" 
                    else: 
                        rez="1"
                    if stroka_number==1:
                        self.table.append([0]*(pow(2,len(self.letters_list))+1))
                        self.table[len(self.table )-1][0]=char+stack[-1]
                    count_operations+=1
                    self.table[count_operations][stroka_number]=rez
                    val_dict[self.table[count_operations][0]]=self.table[count_operations][stroka_number]
                    stack.append(char+stack[-1])
                    stack.pop(-2)
                    
                else:
                    op1=int(val_dict[stack[0]])
                    op2=int(val_dict[stack[1]])
                    match(char):
                        case '&': rez=str(op1 * op2)
                        case'|': rez= str(op1 | op2)
                        case'>': rez=str(int(not (bool(op1)) or bool(op2)))
                        case'~':rez=str(int(op1==op2))
                    if stroka_number==1:
                        self.table.append([0]*(pow(2,len(self.letters_list))+1))
                        self.table[len(self.table)-1][0]=stack[0]+char+stack[1]
                    count_operations+=1
                    self.table[count_operations][stroka_number]=rez
                    val_dict[self.table[count_operations][0]]=self.table[count_operations][stroka_number]
                    stack.append(stack[0]+char+stack[1])
                    stack.pop(1)
                    stack.pop(0)
            stack.clear()
            val_dict.clear()
    def show_table(self):
        table_header = str(self.table[0][0])
        for i in range(1,len(self.table),1):
            table_header+=' ' +self.table[i][0]
        print(table_header)
        for i in range(1, len(self.table[0])): 
                row_values =''  
                for row in self.table:
                    row_values += row[i] + ' '  
                print(row_values.rstrip())


    def build_sdnf(self):
        sdnf_value_form=["("]
        sdnf=[]
        for stroka_number in range(0,len(self.table[0])-1,1):
            if self.table[len(self.table)-1][stroka_number+1]=="1":
                sdnf_value_form.append(str(stroka_number))
                sdnf_value_form.append(",")
                sdnf.append("(")
                for stolbik_number in range(0,len((self.letters_list)),1):
                    if self.table[stolbik_number][stroka_number+1]== "0":
                        sdnf.append("!")
                    sdnf.append(self.table[stolbik_number][0])
                    sdnf.append("&")
                sdnf.pop()
                sdnf.append(")")
                sdnf.append("|")
        sdnf.pop()
        sdnf_value_form.pop()
        sdnf_value_form.append(")")
        sdnf_value_form.append("|")
        print(str(sdnf_value_form))
        return str(sdnf)
         
   
    def build_sknf(self):
        sknf_value_form=["("]
        sknf=[]
        for stroka_number in range(0,len(self.table[0])-1,1):
            if self.table[len(self.table)-1][stroka_number+1]=="0":
                sknf_value_form.append(str(stroka_number))
                sknf_value_form.append(",")
                sknf.append("(")
                for stolbik_number in range(0,len((self.letters_list)),1):
                    if self.table[stolbik_number][stroka_number+1]== "1":
                        sknf.append("!")
                    sknf.append(self.table[stolbik_number][0])
                    sknf.append("|")
                sknf.pop()
                sknf.append(")")
                sknf.append("&")
        sknf.pop()
        sknf_value_form.pop()
        sknf_value_form.append(")")
        sknf_value_form.append("&")
        print(str(sknf_value_form))   
        return str(sknf)
        
    def binary_to_decimal(self,value):
        result =0
        degree=0
        for i in range(len(value)-1,-1,-1):
            result += int(value[i])*2**degree
            degree+=1
        return result
    def rez_index_form(self):
        rez=""
        for stroka_number in range(1,len(self.table[0]),1):
            rez+=self.table[len(self.table)-1][stroka_number]

        return self.binary_to_decimal(rez)








logic = Logic_operator(input("function\n"))
print(logic.build_sdnf())
print(logic.build_sknf())
print(logic.rez_index_form())

