import math
def test(arg):
    arg_a = math.floor(arg)
    arg_b = math.floor((arg - arg_a)*10)
    arg_c = round((arg - arg_a - arg_b/10)*100)
    return arg_a, arg_b, arg_c

def reverse(a,b,c):
    floater = a 
    print(floater)
    floater += b/10
    print(floater)
    floater += c/100
    print(c/100)
    print(1.1+0.03)
    return round(floater, 2)

a,b,c = test(1.13)

print(a,b,c)

i = reverse(a,b,c)

print(i)

