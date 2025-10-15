import numpy as np
from numpy import random

def dexp(lambdaa, alpha):
    t = random.rand()
    return -(1/lambdaa) * np.log(1 - t**(1/alpha))

def first_type_error(t0, n = 10, lambdaa = 1, alpha = 1):
    ext = [dexp(lambdaa, alpha) for _ in range(n)]
    for i in range(len(ext)):
        if ext[i] > t0:
            ext[i] = t0
    return ext

print(first_type_error(1))

def second_type_error(m, n = 10, lambdaa = 1, alpha = 1):
    ext = [dexp(lambdaa, alpha) for _ in range(n)]
    ext.sort()
    ext = ext[:m]
    ext += [max(ext) for _ in range(n - m)]
    return ext

print(second_type_error(5))