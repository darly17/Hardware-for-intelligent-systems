import binary_translator  
import decimal_translator
import binary_operations
class Menu:
    translator_bin=Binary_translator()
    translator_dec=Translator_to_decimal()
    def __init__(self):
        isCycle=True
        while(isCycle):
            choice=int(input("Choose operation:\n1.Get binary\n2.Get direct binary\n3.Get reverse binary\n4.Get additional binary\n5.Get binary with fixed point\n6.Get  binary with floating point\n7.Get sum of additional binary\n8.Get substraction of additional binary\n9.Get multiplication of direct binary\n10.Divide binary\n11.Get sum of binary with floating point"))
                continue
            if choice==1:
                value =int(input('Enter your value to translate'))
                print(translator.get_binary(value))
                
                continue
            elif choice==2:
                 value =int(input('Enter your value to direct binary translate'))
                 print(translator.get_direct_binary(value))
                 continue
            elif choice==3:
                value =int(input('Enter your value to reverse binary translate'))
                print(translator.get_reverse_binary(value))
                continue
            elif choice==4:
                value =int(input('Enter your value to additional binary translate'))
                print(translator.get_additional_binary(value))
                continue
            elif choice==5:
                value =int(input('Enter your value to binary with fix point translate'))
                print(translator.decimal_to_binary_fixed(value))
                continue
            elif choice==6:
            
                continue
            if choice==7:
            
                continue
            elif choice==8:
                
                continue
            elif choice==9:

                continue
            elif choice==10:
            
                continue
            elif choice==11:
                
                continue
            else:
                isCycle=False