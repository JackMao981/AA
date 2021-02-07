# courtesy of https://jeremykun.com/2014/12/01/linear-programming-and-the-simplex-algorithm/
# The following code is not mine, but I will be commenting the code to explain what it means

# The algorithm for doing simplex on a linear programming problem in standard form
# c: the optimization equation that we want to MAXIMIZE, and add filler 0's for the slack variables
# A: the coefficients to all of the variables and the slack variables
# b: the right hand side of the inequalities, ie the constants
import numpy as np
def simplex(c, A, b):
    # First step in simplex, which is to convert our
    # inputs into the tableau.
    tableau = initialTableau(c, A, b)
    # while the tableau has positive numbers of the bottom most row
    # (not including the augmented column), find a pivot and try to get rid of
    # the positive numbers.
    while canImprove(tableau):
        # Sets the pivot
        pivot = findPivotIndex(tableau)
        # using the pivot, update the tableau
        pivotAbout(tableau, pivot)

    return primalSolution(tableau), objectiveValue(tableau)

# creates the initial tableau based on the linear programming problem given.
def initialTableau(c, A, b):
    # creates the "augmented matrix" with A and b
    tableau = [row[:] + [x] for row, x in zip(A, b)]
    # tags on the optimization equation on the bottom.
    tableau.append(c[:] + [0])
    return tableau

def primalSolution(tableau):
   # the pivot columns denote which variables are used
    columns = np.transpose(tableau)
    indices = [j for j, col in enumerate(columns[:-1]) if isPivotCol(col)]
    return list(zip(indices, columns[-1]))

# This is the only function I wrote myself. It checks if the col is a pivot
# column by checking if the last value of the transposed tableau row is 0
# if it is 0, then it is a pivot column
def isPivotCol(col):
    return col[-1] == 0

# returns the objective value, which is in the value in the last row, last column of the
# augmented matrix
def objectiveValue(tableau):
    return -(tableau[-1][-1])

# checks if the tableau can be improved upon
def canImprove(tableau):
    lastRow = tableau[-1]
    # checks if there is any value in the last row that has positive values
    return any(x > 0 for x in lastRow[:-1])

# find the index to pivot using pivot rules
def findPivotIndex(tableau):
    # pick first nonzero index of the last row
    column = [i for i,x in enumerate(tableau[-1][:-1]) if x > 0][0]
    quotients = [(i, r[-1] / r[column]) for i,r in enumerate(tableau[:-1]) if r[column] > 0]

    # pick row index minimizing the quotient
    row = min(quotients, key=lambda x: x[1])[0]
    return row, column

# pivots about the index you've chosen using findPivotIndex
def pivotAbout(tableau, pivot):
    i,j = pivot

    pivotDenom = tableau[i][j]
    tableau[i] = [x / pivotDenom for x in tableau[i]]

    # do the row operations
    for k,row in enumerate(tableau):
        if k != i:
            pivotRowMultiple = [y * tableau[k][j] for y in tableau[i]]
            tableau[k] = [x - y for x,y in zip(tableau[k], pivotRowMultiple)]
# This is the problem ninjas want me to solve
c = [8,-6,4,0,0,0]
b = [12,20,15]
A = [[1,1,1,1,0,0], [5,4,0,0,1,0],[0,9,2,0,0,1]]
print(simplex(c,A,b))
