''' Created by: FigNewtons

	Takes an A.C.M from a text file
	and outputs its row-reduced echelon
	form.
'''

from sympy import Matrix

filename = "matrix.txt"
f = open(filename)
matrix = [ [float(num) for num in line.split()] for line in f]
print(Matrix(matrix).rref())
