class Binary_translator:
    EXPONENTA_LENGTH = 8
    MANTISSA_LENGTH = 23
    def reverse(self,value):
        if value % 2 == 1:
            return 0
        else :
            return 1

    def get_binary(self,value):
        result_direct_binary = ''
        abs_value= abs(value)
        while abs_value > 0 :
            result_direct_binary= str(abs_value % 2)+result_direct_binary
            abs_value = abs_value // 2 


        return result_direct_binary
    
    def get_direct_binary(self,value):
        result_direct_binary=self.get_binary(value)
        if value < 0:
            result_direct_binary='1'+result_direct_binary
        else :
            result_direct_binary='0'+result_direct_binary

        return result_direct_binary   

    def get_reverse_binary (self,value):
        result_reverse_binary = ''
        abs_value= abs(value)
        while abs_value > 0 :
            if value < 0:
                result_reverse_binary=str(self.reverse(abs_value))+result_reverse_binary
            else:
                result_reverse_binary= str(abs_value % 2)+result_reverse_binary
            abs_value = abs_value // 2
        if value < 0:
            result_reverse_binary='1'+result_reverse_binary
        else :
            result_reverse_binary='0'+result_reverse_binary
        return result_reverse_binary

    def get_additional_binary (self,value):
        result_additional_binary=''
        result_direct_binary=''
        abs_value= abs(value)
        abs_negative_value_increased_by_one= abs_value-1 
        while abs_value > 0 :
            result_direct_binary= str(abs_value % 2)+result_direct_binary
            if value < 0:
                result_additional_binary=str(self.reverse( abs_negative_value_increased_by_one))+result_additional_binary
            abs_value = abs_value // 2
            abs_negative_value_increased_by_one =  abs_negative_value_increased_by_one // 2   
        if value < 0:
            result_additional_binary='1'+result_additional_binary
        
        else :
            result_additional_binary='0'+result_direct_binary
        return result_additional_binary

    def decimal_to_binary_fixed(self,decimal_num):
        result_sign = '1' if decimal_num < 0 else '0'
        decimal_num = abs(decimal_num)
        int_part = int(decimal_num)
        binary_integer = ''
        if int_part == 0:
            binary_integer = '0'
        else:
            while int_part > 0:
                binary_integer = str(int_part % 2) + binary_integer
                int_part = int_part // 2
        fract_part = decimal_num - int(decimal_num)
        binary_fraction = ''

        while fract_part != 0:
            fract_part *= 2
            bit = int(fract_part)
            binary_fraction += str(bit)
            fract_part -= bit
        return result_sign + binary_integer + ('.' + binary_fraction if binary_fraction else '')

    def decimal_to_binary_float (self,value):
        result_sign = '1' if value < 0 else '0'
        binary_value =self.decimal_to_binary_fixed(value)[1:]
        index_of_point = binary_value.index('.')
        #находим экспоненту как длину смещения точки в самое начало -1 
        if binary_value[0] == '0':
            # если целая часть равна 0, сдвигаем точку вправо
            first_one_index = binary_value.index('1')
            exponent = -(first_one_index - index_of_point)
            mantissa = binary_value[first_one_index + 1:]
        else:
            exponent = (len(binary_value[:index_of_point])-1)
            mantissa = binary_value[1:index_of_point]+binary_value[index_of_point+1:]
        exponent+=127
        exponent_bin = ''
        for _ in range(self.EXPONENTA_LENGTH):  
            exponent_bin = str(exponent % 2) + exponent_bin
            exponent = exponent // 2
        
        mantissa=mantissa.ljust(self.MANTISSA_LENGTH, '0')[:self.MANTISSA_LENGTH]
        return result_sign + exponent_bin + mantissa