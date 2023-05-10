from setup import *
import random

class Optimizer(setup):
    def __init__(self):
        setup.__init__(self)
        self._pType = None
        self._numExp = None

    def setNumExp(self, numExp):
        self._numExp = numExp
        
    def getNumExp(self):
        return(self._numExp)
    
    def setPType(self, pType):
        self._pType = pType
        
    def displayNumExp(self):
        print("Number of experiments: ", self._numExp)

class MetaHeuristics(Optimizer):
    def __init__(self):
        Optimizer.__init__(self)
        self._limitEval = 0
        self._whenBestFound = None

    def setLimitEval(self, limitEval):
        self._limitEval = limitEval
        
    def setWhenBestFound(self, whenBestFound):
        self._whenBestFound = whenBestFound
        
    def getWhenBestFound(self):
        return(self._whenBestFound)
    
    def run(self):
        pass
    
    def displaySetting(self):
        if self._pType == 1:
            print()
            print("Mutation step size:", self._delta)
            
            if self._aType == 2 or 3:
                print("Limit evaluations : ", self._limitEval)

class SimulatedAnnealing(MetaHeuristics):
    def run(self, a):
        newfile = open('SA.txt', 'w')
        
        current = a.randomInit()
        valueC = a.evaluate(current)
        
        t = 1
        T = a.initTemp()
        
        while t <= self._limitEval:
            newfile.write(str(valueC) + "\n")
            if T == 0:
                return current
            
            successor = a.randomMutant(current)
            valueS = a.evaluate(successor)

            E = valueS-valueC
            if E < 0:
                current = successor
                valueC = valueS
                self.setWhenBestFound(t)
            else:
                P = a.getExp(E,T)
                if random.uniform(0, 1) < (P):
                    currnet = successor
                    valueC = valueS
                    self.setWhenBestFound(t)
                    
            t = t+1
            T = a.tSchedule(T)

        a.setSolution(current)
        a.setMinimum(valueC)
        newfile.close()
#        return(current,valueC)

    def displaySetting(self):
        print()
        print("Search algorithm: SimulatedAnnealing")
        MetaHeuristics.displaySetting(self)
    
class HillClimbing(Optimizer):
    def __init__(self):
        Optimizer.__init__(self)
        self._limitStuck = 100
        self._numRestart = None

    def setNumRestart(self, numRestart):
        self._numRestart = numRestart
        
    def setLimitStuck(self, limitStuck):
        self._limitStuck = limitStuck
        
    def randomRestart(self, a):
        Solution,Minimum = self.run(a)
        a.setMinimum(Minimum)
        a.setSolution(Solution)
        
        for i in range(0, self._numRestart-1):
            Solution,Minimum = self.run(a)
            if a.getValue() >= Minimum:
                a.setMinimum(Minimum)
                a.setSolution(Solution)
       
    def run(self):
        pass

    def displaySetting(self):
        if self._pType == 1:
            print()
            print("Mutation step size:", self._delta)
            
            if self._aType == 2 or 3:
                print("Max evaluations with no improvement: ",self._limitStuck,"iterations")

class FirstChoice(HillClimbing):
    def run(self,a):
        newfile = open('firstChoice.txt', 'w')
        current = a.randomInit()   # 'current' is a list of values
        valueC = a.evaluate(current)
        i = 0
        while i < self._limitStuck:
            successor = a.randomMutant(current)
            valueS = a.evaluate(successor)
            
            if valueS < valueC:
                current = successor
                valueC = valueS
                i = 0              # Reset stuck counter
                newfile.write(str(valueC)+"\n")
            else:
                i += 1
#        a.setSolution(current)
#        a.setMinimum(valueC)
        newfile.close()
        return(current,valueC)
    
    def displaySetting(self):
        print()
        print("Search algorithm: First-Choice Hill Climbing")
        HillClimbing.displaySetting(self)


class SteepestAscent(HillClimbing):
    def run(self, a):
        current = a.randomInit()   # 'current' is a list of city ids
        valueC = a.evaluate(current)
        
        while True:
            neighbors = a.mutants(current)
            (successor, valueS) = a.bestOf(neighbors)
            if valueS >= valueC:
                break
            else:
                current = successor
                valueC = valueS
#        a.setSolution(current)
#        a.setMinimum(valueC)
        return(current, valueC)
    
    def displaySetting(self):
        print()
        print("Search algorithm: Steepest-Ascent Hill Climbing")
        HillClimbing.displaySetting(self)

class GradientDescent(HillClimbing):
    def run(self,a):
        currentA = a.randomInit() # 'current' is a list of values
        valueC = a.evaluate(currentA)
        while True:
            nextA = a.takeStep(currentA,valueC)
            valueN = a.evaluate(nextA)
            if valueN >= valueC:
                break
            else:
                currentA = nextA
                valueC = valueN
#        a.setSolution(currentA)
#        a.setMinimum(valueC)
        return(current,valueC)
    
    def displaySetting(self):
        print()
        print("Search algorithm: Gradient Desent")
        print()
        print("Mutation step size:", self._delta)
        print("Increment for calculating derivatives:",self._dx)
        
class Stochastic(HillClimbing):
    def run(self,a):
        current = a.randomInit()   # 'current' is a list of city ids
        valueC = a.evaluate(current)
        while True:
            neighbors = a.mutants(current)
            (successor, valueS) = a.stochasticBest(neighbors)
            if valueS >= valueC:
                break
            else:
                current = successor
                valueC = valueS
#        a.setSolution(current)
#        a.setMinimum(valueC)
        return(current,valueC)
    
    def displaySetting(self):
        print()
        print("Search algorithm: Stochastic")
        HillClimbing.displaySetting(self)


