class Translator_to_decimal:
    EXPONENTA_LENGTH = 8
    MAGICAl=127
    def reverse(self,value):
        if value % 2 == 1:
            return 0
        else :
            return 1

    def binary_to_decimal_fixed(self,binary_str):
        if '.' in binary_str:
            int_part,fract_part = binary_str.split('.') #разделим на две части 
        else :
            int_part, fract_part = binary_str,False
        
        degree=0
        decimal_integer = 0
        decimal_fraction = 0
        for i in range(len(int_part)-1,0,-1):
            decimal_integer += int(int_part[i])*2**degree
            degree+=1
        if fract_part:
            for i in range(len(fract_part)):
                bit = fract_part[i] 
                decimal_fraction += int(bit) * (0.5 ** (i + 1))

        return decimal_integer + decimal_fraction   

    def binary_to_decimal(self,value):
        result =0
        degree=0
        for i in range(len(value)-1,-1,-1):
            result += int(value[i])*2**degree
            degree+=1
        return result
    def binary_to_decimal_fixed(self,binary_str):
        if '.' in binary_str:
            int_part,fract_part = binary_str.split('.') #разделим на две части 
        else :
            int_part, fract_part = binary_str,False
        
        degree=0
        decimal_integer = 0
        decimal_fraction = 0
        for i in range(len(int_part)-1,0,-1):
            decimal_integer += int(int_part[i])*2**degree
            degree+=1
        if fract_part:
            for i in range(len(fract_part)):
                bit = fract_part[i] 
                decimal_fraction += int(bit) * (0.5**(i + 1))

        return decimal_integer + decimal_fraction

    def direct_binary_to_decimal(self,value):
        value_sign = value[0]
        result =0
        degree=0
        for i in range(len(value)-1,0,-1):
            result += int(value[i])*2**degree
            degree+=1
        result_sign = '-' if value_sign=='1' else ''
        return result_sign + str(result)

    def reverse_binary_to_decimal(self,value):
        value_sign = value[0]
        result =0
        degree=0
        for i in range(len(value)-1,0,-1):
            result +=self.reverse(int(value[i]))*2**degree
            degree+=1
        result_sign = '-' if value_sign=='1' else ''
        return result_sign + str(result)

    def additional_binary_to_decimal(self,value):
        result= self.reverse_binary_to_decimal(value)
        if value[0]=='1':
            result=int(result)-1
        else:
            result=int(result)+1
        return str(result)

    def binary_float_to_decimal(self,value):
        sign, exp, mant = value[0], value[1:self.EXPONENTA_LENGTH+1], value[self.EXPONENTA_LENGTH+1:]
        exp_int = int(exp,2)-self.MAGICAl
        result_mant=0
        k=-1
        for i in range(len(mant)):
            result_mant+=int(mant[i]) *2**(k)
            k-=1
        return((-1)**int(sign) * (result_mant+1)*2**exp_int)


  
