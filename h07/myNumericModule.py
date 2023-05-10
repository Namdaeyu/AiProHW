import random
import math

def CreateProblem():
    fileName = input("Enter the file name of a function: ")
    infile = open(fileName,'r')
    
    ListVal = []
    domain = []
    
    for line in infile:
        ListVal.append(line.rstrip())
    for i in range(1,len(ListVal)):
        ListVal[i] = ListVal[i].split(',')
        
    expression = ListVal[0]
    varName =[]
    low = []
    up = []
    for a in ListVal[1:]:
        varName.append(a[0])
        low.append(int(a[1]))
        up.append(int(a[2]))
    domain.append(varName)
    domain.append(low)
    domain.append(up)
    
    ##print(domain)
    infile.close()
    ## Then, return a problem 'p'.
    ## 'p' is a tuple of 'expression' and 'domain'.
    ## 'expression' is a string.
    ## 'domain' is a list of 'varNames', 'low', and 'up'.
    ## 'varNames' is a list of variable names.
    ## 'low' is a list of lower bounds of the varaibles.
    ## 'up' is a list of upper bounds of the varaibles.
    
    return expression, domain

def randomInit(p): ###
    init = []
    domain = p[1]
    print(domain)
    for a in range(0,5):
        l = domain[1][a]
        u = domain[2][a]
        init.append(round(random.uniform(l,u),3))
    return init

def mutate(current, i, d, p): ## Mutate i-th of 'current' if legal
    curCopy = current[:]
    domain = p[1]        # [VarNames, low, up]
    l = domain[1][i]     # Lower bound of i-th
    u = domain[2][i]     # Upper bound of i-th
    if l <= (curCopy[i] + d) <= u:
        curCopy[i] += d
    return curCopy
