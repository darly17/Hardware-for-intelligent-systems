from binary_translator import *
from decimal_translator import *
from binary_operations import * 

class Menu:
    translator_bin = Binary_translator()
    translator_dec = Translator_to_decimal()
    binary_op = Binary_operation()  
    
    def __init__(self):
        isCycle = True
        while(isCycle):
            choice = int(input("Choose operation:\n1.Get binary\n2.Get direct binary\n3.Get reverse binary\n4.Get additional binary\n5.Get binary with fixed point\n6.Get binary with floating point\n7.Get sum of additional binary\n8.Get subtraction of additional binary\n9.Get multiplication of direct binary\n10.Divide binary\n11.Get sum of binary with floating point\nEnter your choice (1-11, or any other number to exit): "))
            
            if choice == 1:
                value = int(input('Enter your value to translate: '))
                print(self.translator_bin.get_binary(value))
                print("for checking: ",self.translator_dec.binary_to_decimal(self.translator_bin.get_binary(value)))
                continue
                
            elif choice == 2:
                value = int(input('Enter your value to direct binary translate: '))
                print(self.translator_bin.get_direct_binary(value))
                print("for checking: ",self.translator_dec.direct_binary_to_decimal(self.translator_bin.get_direct_binary(value)))

                continue
                
            elif choice == 3:
                value = int(input('Enter your value to reverse binary translate: '))
                print(self.translator_bin.get_reverse_binary(value))
                print("for checking: ",self.translator_dec.reverse_binary_to_decimal(self.translator_bin.get_reverse_binary(value)))

                continue
                
            elif choice == 4:
                value = int(input('Enter your value to additional binary translate: '))
                print(self.translator_bin.get_additional_binary(value))
                print("for checking: ",self.translator_dec.additional_binary_to_decimal(self.translator_bin.get_additional_binary(value)))
                continue
                
            elif choice == 5:
                value = float(input('Enter your value to binary with fixed point translate: ')) 
                print(self.translator_bin.decimal_to_binary_fixed(value))
                print("for checking: ",self.translator_dec.binary_to_decimal_fixed(self.translator_bin.decimal_to_binary_fixed(value)))

                continue
                
            elif choice == 6:
                value = float(input('Enter your value to binary with floating point translate: '))
                print(self.translator_bin.decimal_to_binary_float(value))
                print("for checking: ",self.translator_dec.binary_float_to_decimal(self.translator_bin.decimal_to_binary_float(value)))

                continue
                
            elif choice == 7:
                value1 = int(input('Enter first value for sum: '))
                value2 = int(input('Enter second value for sum: '))
                print(self.binary_op.sum_additional_binary(value1, value2))
                continue
                
            elif choice == 8:
                value1 = int(input('Enter first value for subtraction: '))
                value2 = int(input('Enter second value to subtract: '))
                print(self.binary_op.substraction_additional_binary(value1, value2))
                continue
                
            elif choice == 9:
                value1 = int(input('Enter first value for multiplication: '))
                value2 = int(input('Enter second value for multiplication: '))
                print(self.binary_op.multiplication_direct_binary(value1, value2))
                continue
                
            elif choice == 10:
                value1 = int(input('Enter dividend: '))
                value2 = int(input('Enter divisor: '))
                print(self.binary_op.dividing_direct(value1, value2))
                continue
                
            elif choice == 11:
                value1 = float(input('Enter first value for floating point sum: '))
                value2 = float(input('Enter second value for floating point sum: '))
                print(self.binary_op.sum_float_binary(value1, value2))
                print(self.translator_dec.binary_float_to_decimal(self.binary_op.sum_float_binary(value1, value2)))

                continue
                
            else:
                isCycle = False
                print("Exiting program...")

if __name__ == "__main__":
    menu = Menu()   