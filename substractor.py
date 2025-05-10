from minimizer import *
D_function="a/b/c"
B_out_function='(!a&b)|(!a&c)|(b&c)'
if __name__ == "__main__":
    minimizer=LogicMinimizer(D_function)
    print("Минимизация первой выходной функции:\n")
    print(minimizer.minimize_sdnf_karnaugh())
    minimizer=LogicMinimizer(B_out_function)
    print("Минимизация второй выходной функции:\n")
    print(minimizer.minimize_sdnf_karnaugh())
    
    