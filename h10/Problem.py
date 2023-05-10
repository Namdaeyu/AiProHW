from setup import *
import random
import math

class Problem(setup):
    def __init__(self):
        setup.__init__(self)
        self._solution = None
        self._minimum = None
        self._NumEval = 0
        self._avgMinimum = 0
        self._avgNumEval = 0
        self._avgWhen = 0
        self._numSample = 100

    def setSolution(self, solution):
        self._solution = solution
        
    def setMinimum(self, minimum):
        self._minimum = minimum
        
    def getSolution(self):
        return(self._solution)
    
    def getValue(self):
        return(self._minimum)
    
    def getNumEval(self):
        return(self._NumEval)
    
    def storeExpResult(self, results):
        self._solution = results[0]
        self._minimum = results[1]
        self._avgMinimum = results[2]
        self._avgNumEval = results[3]
        self._NumEval = results[4]
        self._avgWhen = results[5]
         
class Numeric(Problem):
    def __init__(self):
        Problem.__init__(self)
        self._expression = None
        self._domain = None
        
    def createProblem(self, fileName): ###
        infile = open(fileName, 'r')
        self._expression = infile.readline()
        
        varNames=[]
        low=[]
        up=[]
        line = infile.readline()
        
        while line !='':
            data = line.split(',')
            varNames.append(data[0])
            low.append(float(data[1]))
            up.append(float(data[2]))
            line = infile.readline()
            
        infile.close()
        self._domain = [varNames, low, up]

    def mutants(self, current): ###
        neighbors = []
        
        for i in range(len(current)):
            mutant = self.mutate(current, i, self._delta)
            neighbors.append(mutant)
            mutant = self.mutate(current, i, -self._delta)
            neighbors.append(mutant)
            
        return neighbors     # Return a set of successors

    def takeStep(self, x, v):
        grad = self.gradient(x,v)
        xCopy = x[:]
        for i in range(len(xCopy)):
            xCopy[i] = xCopy[i] - self._alpha * grad[i]
            
        if self.isLegal(xCopy):
            return xCopy
        else:
            return x

    def gradient(self, x, v):
        grad = []
        for i in range(len(x)):
            xCopyH = x[:]
            xCopyH[i] += self._dx
            g = (self.evaluate(xCopyH)-v)/self._dx
            grad.append(g)
        return grad
    
    def isLegal(self, x):
        domain = self._domain
        low = domain[1]
        up = domain[2]
        flag = True
        
        for i in range(len(low)):
            if x[i] < low[i] or up[i] < x[i]:
                flag = False
                break
            
        return flag

    def bestOf(self, neighbors): ###
        best = neighbors[0]
        bestValue = self.evaluate(best)
        for i in range(1, len(neighbors)):
            newValue = self.evaluate(neighbors[i])
            if newValue < bestValue:
                best = neighbors[i]
                bestValue = newValue
        return best, bestValue
    
    def stochasticBest(self, neighbors):
        # Smaller valuse are better in the following list
        valuesForMin = [self.evaluate(indiv) for indiv in neighbors]
        largeValue = max(valuesForMin) + 1
        valuesForMax = [largeValue - val for val in valuesForMin]
        # Now, larger values are better
        total = sum(valuesForMax)
        randValue = random.uniform(0, total)
        s = valuesForMax[0]
        for i in range(len(valuesForMax)):
            if randValue <= s: # The one with index i is chosen
                break
            else:
                s += valuesForMax[i+1]
        return neighbors[i], valuesForMin[i]

    def initTemp(self): # To set initial acceptance probability to 0.5
        diffs = []
        for i in range(self._numSample):
            c0 = self.randomInit()     # A random point
            v0 = self.evaluate(c0)     # Its value
            c1 = self.randomMutant(c0) # A mutant
            v1 = self.evaluate(c1)     # Its value
            diffs.append(abs(v1 - v0))
        dE = sum(diffs) / 5 # Average value difference
        t = dE / math.log(2)        # exp(–dE/t) = 0.5
        return t

    def tSchedule(self, t):
        return t * (1 - (1 / 10**4))

    def getExp(self, E,T):
        return (math.exp(-E/T))

    def randomInit(self): ###
        domain = self._domain
        low,up = domain[1],domain[2]
        init = []
        for i in range(len(low)):
            r = random.uniform(low[i], up[i])
            init.append(r) # Return a random initial point
        return init
    
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
            d = self._delta
        else:
            d = -self._delta
        return self.mutate(current,i, d) # Return a random successor

    def report(self):
        print("Average objective value: {0:,.3f}".format(self._avgMinimum))
        print("Average number of evaluations: {0:,}".format(self._avgNumEval))
        print()
        print("Best Solution found:")
        print(self.coordinate())  # Convert list to tuple
        print("Best value: {0:,.3f}".format(self._minimum))
        print()
        if 5 <= self._aType <= 6:
             print("When best found average: {0:,}".format(self._avgWhen))
        print()
        print("Total number of evaluations: {0:,}".format(self._NumEval))
        
    def describe(self):
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
        
    def createProblem(self,fileName):
        ## Read in a TSP (# of cities, locatioins) from a file.
        ## Then, create a problem instance and return it.
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
    
    def stochasticBest(self, neighbors):
        # Smaller valuse are better in the following list
        valuesForMin = [self.evaluate(indiv) for indiv in neighbors]
        largeValue = max(valuesForMin) + 1
        valuesForMax = [largeValue - val for val in valuesForMin]
        # Now, larger values are better
        total = sum(valuesForMax)
        randValue = random.uniform(0, total)
        s = valuesForMax[0]
        for i in range(len(valuesForMax)):
            if randValue <= s: # The one with index i is chosen
                break
            else:
                s += valuesForMax[i+1]
        return neighbors[i], valuesForMin[i]

    def initTemp(self): # To set initial acceptance probability to 0.5
        diffs = []
        for i in range(self._numSample):
            c0 = self.randomInit()     # A random point
            v0 = self.evaluate(c0)     # Its value
            c1 = self.randomMutant(c0) # A mutant
            v1 = self.evaluate(c1)     # Its value
            diffs.append(abs(v1 - v0))
        dE = sum(diffs) / 5 # Average value difference
        t = dE / math.log(2)        # exp(–dE/t) = 0.5
        return t

    def tSchedule(self, t):
        return t * (1 - (1 / 10**4))

    def getExp(self,E,T):
        return math.exp(-E/T)
    
    def describe(self):
        print()
        n = self._numCities
        print("Number of cities:", n)
        print("City locations:")
        locations = self._locations
        for i in range(n):
            print("{0:>12}".format(str(locations[i])), end = '')
            if i % 5 == 4:
                print()
                
    def report(self):
        print()
        print("Average objective value: {0:,.3f}".format(self._avgMinimum))
        print("Average number of evaluations: {0:,}".format(self._avgNumEval))
        print()
        print("Best order of visits:")
        self.tenPerRow()       # Print 10 cities per row
        print("Best tour cost: {0:,}".format(round(self._minimum)))
        if 5 <= self._aType <= 6:
             print("When best found average: {0:,}".format(self._avgWhen))
        print("Total number of evaluations: {0:,}".format(self._NumEval))

    
    def tenPerRow(self):
        for i in range(len(self._solution)):
            print("{0:>5}".format(self._solution[i]), end='')
            if i % 10 == 9:
                print()        
