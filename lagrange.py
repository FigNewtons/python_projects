import numpy as np
import operator as op
from sympy.abc import z
from sympy import Lambda, pprint
from functools import reduce

''' 
    Numerical Analysis: HW 2
    Lagrange interpolation solver

    Author: Daniel Gruszczynski
    Date: March 13, 2016

'''
def basis(x, i):
    "Return the Lagrange basis function at index i for numpy array x. "
    indices = np.nonzero(x[i] - x)
    exp = reduce(op.mul, z-x[indices]) / reduce(op.mul, x[i]-x[indices])
    return exp

def lagrange(x, y):
    "Return the lagrange polynomial for points (x,y) as a lambda function. "
    li = [basis(x, i) for i in range(len(x))] 
    return Lambda(z, np.dot(y, li))    

if __name__ == '__main__':

    x = np.linspace(0, .75, 4)
    y = [1.3, 1.7, 2.6, 0.9]

    p = lagrange(x, y)
    v = 0.6

    # Output
    print("The Lagrange polynomial is: ")
    pprint(p)
    print("The value at {v} is {pv}.\n".format(v=v, pv=p(v)))

