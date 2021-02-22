# The algorithm for doing simplex on a linear programming problem in standard form
# A: the coefficients to all of the variables and the slack variables
# b: the right hand side of the inequalities, ie the constants
# c: the optimization equation that we want to MAXIMIZE, and add filler 0's for the slack variables
import numpy as np
def simplex(A, b, c):
    matrix = convert_to_matrix(A,b,c)
    while has_positive(matrix):
        pivotAbout(matrix)
    p = primal(matrix)
    o = objective(matrix)
    print("Primal Solution", p)
    print("Objective value", o)
# creates the initial tableau based on the linear programming problem given.
def convert_to_matrix(A, b, c):
    matrix = []
    for i in range(len(A)):
        A[i].append(b[i])
        matrix.append(A[i])
    matrix.append(c+[0])
    return matrix

def primal(matrix):
    columns = np.transpose(matrix)
    indices = [j for j, col in enumerate(columns[:-1]) if isPivotCol(col)]
    return list(zip(indices, columns[-1]))

def isPivotCol(col):
    return col[-1] == 0

# returns the objective value, which is in the value in the last row, last column of the
# augmented matrix
def objective(matrix):
    return -(matrix[-1][-1])
# checks if the matrix has positive values in the last row
def has_positive(matrix):
    for i in matrix[-1]:
        if i > 0:
            return True
    return False

# find the index to pivot using pivot rules
def findPivot(matrix):
    # pick first nonzero index of the last row
    column = [i for i,x in enumerate(matrix[-1][:-1]) if x > 0][0]
    quotients = [(i, r[-1] / r[column]) for i,r in enumerate(matrix[:-1]) if r[column] > 0]

    # pick row index minimizing the quotient
    row = min(quotients, key=lambda x: x[1])[0]
    return row, column

# pivots about the index you've chosen using findPivotIndex
def pivotAbout(matrix):
    pivot = findPivot(matrix)
    i,j = pivot
    pivotDenom = matrix[i][j]
    matrix[i] = [x / pivotDenom for x in matrix[i]]

    # do the row operations
    for k,row in enumerate(matrix):
        if k != i:
            pivotRowMultiple = [y * matrix[k][j] for y in matrix[i]]
            matrix[k] = [x - y for x,y in zip(matrix[k], pivotRowMultiple)]

# This is the problem ninjas want me to solve
# The output is ([(0, 0.5), (2, 4.0), (3, 7.5)], 62.0)
# primal solutions are the list of the tuples.
# the first value corresponds to the column/variable while the second value represents its value
# 62.0 is the objective values
    return

A = [[1,1,1,1,0,0], [5,4,0,0,1,0],[0,9,2,0,0,1]]
b = [12,20,15]
c = [8,-6,4,0,0,0]
simplex(A,b,c)
