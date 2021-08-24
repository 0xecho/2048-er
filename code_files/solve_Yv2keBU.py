# 3
# 2
# 2 1
# 3 1
# 2
# 2 2
# 3 1
# 1
# 5 1
import math
def divs(n) : 
    lst = [] 
    for i in range(1, int(math.sqrt(n) + 1)) :
        if (n % i == 0) :
            lst.append(int(n / i))
    return lst
for  _ in range(int(input())):
    C = int(input())
    l = 1
    for __ in range(C):
        a,b = [int(i) for i in input().split()]
        for ___ in range(b):
            l*=a
    print(l)
    print(divs(l))