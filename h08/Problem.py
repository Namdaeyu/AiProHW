import random
import math
DELTA=0.001
ALPHA=0.0001

class Problem:
    def __init__(self):
        self._solution = None
        self._minimum= None
        self._NumEval= 0


    def setSolution(self,solution):
        self._solution=solution
        
    def setMinimum(self,minimum):
        self._minimum=minimum
        
class Numeric(Problem):
    def __init__(self):
        Problem.__init__(self)
        self._expression=None
        self._domain=None

    def createProblem(self): ###
        fileName=input()
        infile = open(fileName,'r')
        self._expression=infile.readline()
        varNames=[]
        low=[]
        up=[]
        line = infile.readline()
        while line !='':
            data = line.split(',')
            varNames.append(data[0])
            low.append(float(data[1]))
            up.append(float(data[2]))
            line=infile.readline()
        infile.close()
        self._domain =[varNames,low,up]

    def mutants(self,current): ###
        neighbors=[]
        for i in range(len(current)):
            mutant=self.mutate(current,i,DELTA)
            neighbors.append(mutant)
            mutant=self.mutate(current,i,-DELTA)
            neighbors.append(mutant)
        return neighbors     # Return a set of successors

    def Gmutants(self,current): ###
        neighbors=[]

        for i in range(0,len(current)):
            mutantg=self.mutate(current,i,ALPHA)
            mutant=self.mutate(current,i,DELTA)
            neighbors.append([mutantg,mutant])
            mutantg=self.mutate(current,i,-ALPHA)
            mutant=self.mutate(current,i,-DELTA)
            neighbors.append([mutantg,mutant])
        return neighbors     # Return a set of successors
    
    def Gevaluate(self,a,valueC):
        self._NumEval += 1
        expr = self._expression         # p[0] is function expression
        varNames = self._domain[0]  # p[1] is domain
        for i in range(len(varNames)):
            assignment = varNames[i] + '=' + str(a[i])
            exec(assignment)
        value=eval(expr)
        res=(value-valueC)/ALPHA
        return (res)


    def GbestOf(self,neighbors,valueA): ###
        best = neighbors[0]
        bestValue=self.Gevaluate(best[0],valueA)
        for i in range(1,len(neighbors)):
            newValue=self.Gevaluate(neighbors[i][0],valueA)
            if newValue < bestValue:
                best = neighbors[i]
                bestValue=newValue
        return best[1], bestValue





    def bestOf(self,neighbors): ###
        best = neighbors[0]
        bestValue=self.evaluate(best)
        for i in range(1,len(neighbors)):
            newValue=self.evaluate(neighbors[i][0])
            if newValue < bestValue:
                best = neighbors[i]
                bestValue=newValue
        return best, bestValue


    def randomInit(self): ###
        domain =self._domain
        low,up=domain[1],domain[2]
        init =[]
        for i in range(len(low)):
            r=random.uniform(low[i],up[i])
            init.append(r) # Return a random initial point
        return init
    
    def bestOf(self,neighbors): ###
        best = neighbors[0]
        bestValue=self.evaluate(best)
        for i in range(1,len(neighbors)):
            newValue=self.evaluate(neighbors[i])
            if newValue < bestValue:
                best = neighbors[i]
                bestValue=newValue
        return best, bestValue

    def evaluate(self,a):
        self._NumEval += 1
        expr = self._expression         # p[0] is function expression
        varNames = self._domain[0]  # p[1] is domain
        for i in range(len(varNames)):
            assignment = varNames[i] + '=' + str(a[i])
            exec(assignment)
        return eval(expr)

    def mutate(self,current,i, d): ## Mutate i-th of 'current' if legal
        curCopy = current[:]
        l = self._domain[1][i]     # Lower bound of i-th
        u = self._domain[2][i]     # Upper bound of i-th
        if l <= (curCopy[i] + d) <= u:
            curCopy[i] += d
        return curCopy

    def randomMutant(self,current): ###
        i=random.randint(0,len(current)-1)
        if random.uniform(0,1)>0.5:
            d = DELTA
        else:
            d = -DELTA
        return self.mutate(current,i, d) # Return a random successor

    def displayResult(self):
        print()
        print("Solution found:")
        print(self.coordinate())  # Convert list to tuple
        print("Minimum value: {0:,.3f}".format(self._minimum))
        print()
        print("Total number of evaluations: {0:,}".format(self._NumEval))
        
    def describeProblem(self):
        print()
        print("Objective function:")
        print(self._expression)   # Expression
        print("Search space:")
        varNames = self._domain[0] # p[1] is domain: [VarNames, low, up]
        low = self._domain[1]
        up = self._domain[2]
        for i in range(len(low)):
            print(" " + varNames[i] + ":", (low[i], up[i]))
            
    def coordinate(self):
        c = [round(value, 3) for value in self._solution]
        return tuple(c)  # Convert the list to a tuple


class Tsp(Problem):
    def __init__(self):
        Problem.__init__(self)
        self._numCities=0
        self._locations=None
        self._table=None
        
    def createProblem(self):
        ## Read in a TSP (# of cities, locatioins) from a file.
        ## Then, create a problem instance and return it.
        fileName = input("Enter the file name of a TSP: ")
        infile = open(fileName, 'r')
        # First line is number of cities
        numCities = int(infile.readline())
        locations = []
        line = infile.readline()  # The rest of the lines are locations
        while line != '':
            locations.append(eval(line)) # Make a tuple and append
            line = infile.readline()
        infile.close()
        self.calcDistanceTable(numCities, locations)
        self._numCities,self._locations= numCities, locations

    def calcDistanceTable(self, numCities, locations): ###
        table=[]
        for i in range(numCities):
            row=[]
            for j in range(numCities):
                dx=locations[i][0] - locations[j][0]
                dy=locations[i][1] - locations[j][1]
                d=round(math.sqrt(dx**2+dy**2),1)
                row.append(d)
            table.append(row)
        self._table=table # A symmetric matrix of pairwise distances
    def randomInit(self):   # Return a random initial tour
        n = self._numCities
        init = list(range(n))
        random.shuffle(init)
        return init

    def evaluate(self,current): ###
        ## Calculate the tour cost of 'current'
        ## 'p' is a Problem instance
        ## 'current' is a list of city ids

        self._NumEval +=1
        n=self._numCities
        cost=0
        for i in range(n-1):
            locFrom = current[i]
            locTo = current[i+1]
            cost += self._table[locFrom][locTo]
        return cost

    def mutants(self,current): # Apply inversion
        n = self._numCities
        neighbors = []
        count = 0
        triedPairs = []
        while count <= n:  # Pick two random loci for inversion
            i, j = sorted([random.randrange(n) for _ in range(2)])
            if i < j and [i, j] not in triedPairs:
                triedPairs.append([i, j])
                curCopy = self.inversion(current, i, j)
                count += 1
                neighbors.append(curCopy)
        return neighbors

    def inversion(self,current, i, j):  ## Perform inversion
        curCopy = current[:]
        while i < j:
            curCopy[i], curCopy[j] = curCopy[j], curCopy[i]
            i += 1
            j -= 1
        return curCopy

    def bestOf(self,neighbors): ###
        best=neighbors[0]
        bestValue=self.evaluate(best)
        for i in range(1,len(neighbors)):
            newValue=self.evaluate(neighbors[i])
            if newValue < bestValue:
                best=neighbors[i]
                bestValue = newValue
        return best, bestValue

    def randomMutant(self,current): # Apply inversion
        while True:
            i, j = sorted([random.randrange(self._numCities)
                           for _ in range(2)])
            if i < j:
                curCopy = self.inversion(current, i, j)
                break
        return curCopy

    def describeProblem(self):
        print()
        n = self._numCities
        print("Number of cities:", n)
        print("City locations:")
        locations = self._locations
        for i in range(n):
            print("{0:>12}".format(str(locations[i])), end = '')
            if i % 5 == 4:
                print()
                
    def displayResult(self):
        print()
        print("Best order of visits:")
        self.tenPerRow()       # Print 10 cities per row
        print("Minimum tour cost: {0:,}".format(round(self._minimum)))
        print()
        print("Total number of evaluations: {0:,}".format(self._NumEval))

    
    def tenPerRow(self):
        for i in range(len(self._solution)):
            print("{0:>5}".format(self._solution[i]), end='')
            if i % 10 == 9:
                print()        
