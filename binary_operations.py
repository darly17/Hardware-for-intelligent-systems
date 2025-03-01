from decimal_translator import *
from binary_translator import *

class Binary_operation:
    ACCURACY=5
    MANTISSA_LENGTH = 23
    dec_translator = Translator_to_decimal()
    translator = Binary_translator()
    
    def binary_sum(self,value1,value2,max_len):
        result=''
        carry=0
        value1=value1.ljust(max_len,'0')
        value2=value2.ljust(max_len,'0')
        for i in range(max_len-1,-1,-1) :
            bit1 = int(value1[i])  
            bit2 = int(value2[i])
            sum_bit=bit1+bit2 +carry
            result =  str(sum_bit % 2) +result
            carry = sum_bit // 2 
        if carry== 1:
            result=str(carry)+result
        return result
    
    def sum_additional_binary(self,value1, value2):
        add_val_1= self.translator.get_additional_binary(value1) 
        add_val_2= self.translator.get_additional_binary(value2)
        max_len = max(len(add_val_1), len(add_val_2))
        if value1 > 0:
            add_val_1 = add_val_1.zfill(max_len)  
        else :
            add_val_1 = add_val_1.rjust(max_len,'1') 
        if value2 > 0:  
            add_val_2 = add_val_2.zfill(max_len)
        else :
            add_val_2 = add_val_2.rjust(max_len,'1') 
        result=self.binary_sum(add_val_1,add_val_2,max_len)
        result = result[-8:]
        return result

    def substraction_additional_binary(self,value1,value2):
        value2=0-value2
        return self.sum_additional_binary(value1,value2)

    def multiplication_direct_binary(self,value1,value2):
        dir_value_1=self.translator.get_binary(value1)
        dir_value_2=self.translator.get_binary(value2)
        product=''
        current_value=''
        for i in range(len(dir_value_1)-1,-1,-1):
            bit1 = int(dir_value_1[i])  

            if bit1 == 1: 
                current_value=dir_value_2
                for j in range(i,len(dir_value_1)-1 ,1):
                    current_value=current_value +'0'

                product=product.zfill(len(current_value)) 
                product=self.binary_sum(current_value,product,len(current_value))
            else:
                product='0'+product

        if (value1>0 and value2>0) or (value1>0 and value2>0):
            product='0'+product
        else:
            product='1'+product

        return product

    def dividing_direct(self,value1, value2):
        dir_value1=self.translator.get_binary(value1)
        dir_value2=self.translator.get_binary(value2)
        result_sign = '1' if value1*value2 < 0 else '0'
        carry = ''
        result = ''
        for i in range(len(dir_value1)):
            carry += dir_value1[i]  
            if self.dec_translator.binary_to_decimal(carry) < self.dec_translator.binary_to_decimal(dir_value2):
                result += '0'
            else:
                result += '1'
                carry = self.translator.get_binary(self.dec_translator.binary_to_decimal(carry) - self.dec_translator.binary_to_decimal(dir_value2))

        # делаем точность 
        if self.dec_translator.binary_to_decimal(carry) != 0:
                result += '.'
                for _ in range(self.ACCURACY):
                    carry += '0'
                    if self.dec_translator.binary_to_decimal(carry) < self.dec_translator.binary_to_decimal(dir_value2):
                        result += '0'
                    else:
                        result += '1'
                        carry = self.translator.get_binary(self.dec_translator.binary_to_decimal(carry) - self.dec_translator.binary_to_decimal(dir_value2))
        result = result.lstrip('0.') #лишние нули в начале
        return result_sign+result 

    def sum_float_binary(self,value1, value2):
        value1= self.translator.decimal_to_binary_float(value1)
        value2= self.translator.decimal_to_binary_float(value2)
        sign1, exp1, mant1 = value1[0], value1[1:9], value1[9:]
        sign2, exp2, mant2 = value2[0], value2[1:9], value2[9:]
        exp1_int = int(exp1, 2)
        exp2_int = int(exp2, 2)
        result_mant=''
        mant2 = '1' + mant2
        mant1= '1' + mant1

        if exp1_int > exp2_int:
            shift = exp1_int - exp2_int
            for i in range (0,shift-2,1):
                mant2 = '0'+ mant2 
            mant2 = '0' + mant2
            exp2_int = exp1_int
        
        elif exp2_int > exp1_int:
            shift = exp2_int - exp1_int
            
            for i in range (0,shift-2,1):
                mant1 = '0'+ mant1
            mant1 = '0' + mant1
            exp1_int = exp2_int

        result_mant =self.binary_sum(mant1, mant2,max(len(mant1),len(mant2)))
        result_sign = sign1
        if len(result_mant) > max(len(mant1),len(mant2)):
            shift_1= len(result_mant)-max(len(mant1),len(mant2))
            exp1_int+=shift_1
        result_mant=result_mant[1:]

        #округление
        if len(result_mant) > self.MANTISSA_LENGTH :
            if (result_mant[self.MANTISSA_LENGTH ] == '1'):
                result_mant=result_mant[:self.MANTISSA_LENGTH ]
                one_to_add='1'
                one_to_add=one_to_add.zfill(len(result_mant))
                result_mant=self.binary_sum(result_mant,one_to_add,len(result_mant))
            result_mant=result_mant[:self.MANTISSA_LENGTH ]
        
        if result_mant == '0':
            result_mant = '0' * self.MANTISSA_LENGTH 
            exp1_int = 0
        
        result_exp = self.translator.get_binary(exp1_int)
        return f"{result_sign}{result_exp}{result_mant}"


# test = Binary_operation()
# test.dividing_direct(43,6)