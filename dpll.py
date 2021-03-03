import copy
class CNF:
    def __init__(self,clauses = [], literals = []):
        self.clauses = clauses
        self.literals = literals
    # checks if CNF is empty
    def is_empty(self):
        return len(self.clauses) == 0 and len(self.literals) == 0

    # checks if there is a unit clause or literals
    def has_unit(self):
        if len(self.literals) != 0:
            return True
        for c in self.clauses:
            if c.len == 1:
                return True
        return False

    # get the first instance of a unit clause or literal
    # returns a literal or none
    def get_unit(self):
        for l in self.literals:
            if len(self.literals) > 0:
                return self.literals[0]

        for c in self.clauses:
            if c.len == 1:
                return c.first()
        return None

    # pick literal from shortest clause in C
    def lfsc(self):
        c1 = copy.deepcopy(self.clauses)
        sorted(c1, key = lambda c: c.len)
        return c1[0].first()

class Clause:
    def __init__(self, vars = []):
        # this should be a list of literals
        self.vars = vars
        self.len = len(vars)

    # checks if the clause is empty
    def is_empty(self):
        return len(self.vars) == 0

    # checks if the clause is length 1
    def is_unit(self):
        return len(self.vars) == 1

    # returns the first literal in the clause
    def first(self):
        return self.vars[0]

class Literal:
    def __init__(self, name, neg=False):
        self.name = name
        self.neg = neg

    # override literal equivalence
    def __eq__(self, other):
        return self.name == other.name and self.neg == other.neg

    # check if literal is its negative
    def is_neg(self,other):
        return self.name == other.name and self.neg != other.neg

    # negate yourself
    def negate(sef):
        self.neg = not self.neg

# check if p and not p are in CNF as a unit clause or literal
def neg_unit(CNF,p):
    for c in CNF.clauses:
        if (c.is_unit()):
            if(c.first()==p or c.first().is_neg(p)):
                return True
    for l in CNF.literals:
        if (l.is_neg(p)):
            return True
    return False

# simplify the cnf
def simplify(CNF, p):
    for c in CNF.clauses:
        for l in c.vars:
            if(l.is_neg(p)):
                c.vars.remove(l)
            if(l==p):
                CNF.clauses.remove(c)
                break
    for l in CNF.literals:
        if(l==p):
            CNF.literals.remove(l)
    return CNF

# dpll algorithm as described by the pseudocode
def dpll(CNF):
    if (CNF.is_empty()):
        return True
    while(CNF.has_unit()):
        p = CNF.get_unit()
        if(neg_unit(CNF, p)):
            return False
        else:
            CNF = simplify(CNF, p)
    if (CNF.is_empty()):
        return True

    p = CNF.lfsc()
    if(dpll(simplify(CNF,p))):
        return True
    else:
        return dpll(Simplify(CNF, p.negate()))

# create literals
x = Literal("x")
y = Literal("y")
z = Literal("z")
nx = Literal("x", True)
ny = Literal("y", True)
nz = Literal("z", True)

# make clauses
c1 = Clause([x,y,nz])
c2 = Clause([nx,ny,z])
c3 = Clause([nx,y,nz])
c4 = Clause([nx])
c5 = Clause([x])

# create cnfs
cnf1 = CNF([c1,c2,c3],[])
cnf2 = CNF([c4,c5],[])
cnf3 = CNF([c4],[x])
cnf4 = CNF([],[x,y,z])

# Test cnfs against the dpll algorithm
print(dpll(cnf1))
print(dpll(cnf2))
print(dpll(cnf3))
print(dpll(cnf4))
