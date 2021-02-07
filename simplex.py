# courtesy of https://jeremykun.com/2014/12/01/linear-programming-and-the-simplex-algorithm/
# The following code is not mine, but I will be commenting the code to explain what it means

# The algorithm for doing simplex on a linear programming problem in standard form
# c: the optimization equation that we want to MAXIMIZE, and add filler 0's for the slack variables
# A: the coefficients to all of the variables and the slack variables
# b: the right hand side of the inequalities, ie the constants
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
    columns = transpose(tableau)
    indices = [j for j, col in enumerate(columns[:-1]) if isPivotCol(col)]
    return list(zip(indices, columns[-1]))

def objectiveValue(tableau):
    return -(tableau[-1][-1])

def canImprove(tableau):
    lastRow = tableau[-1]
    return any(x > 0 for x in lastRow[:-1])

def pivotAbout(tableau, pivot):
    i,j = pivot

    pivotDenom = tableau[i][j]
    tableau[i] = [x / pivotDenom for x in tableau[i]]

    for k,row in enumerate(tableau):
        if k != i:
            pivotRowMultiple = [y * tableau[k][j] for y in tableau[i]]
            tableau[k] = [x - y for x,y in zip(tableau[k], pivotRowMultiple)]
