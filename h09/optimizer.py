from Setup import *

class HillCliming(Setup):
    def __init__(self):
        Setup.__init__(self)
        self._stuck = 100
        
class FirstChoice(HillCliming):
    def firstChoice(self, a):
        current = a.randomInit()   # 'current' is a list of values
        valueC = a.evaluate(current)
        
        i = 0
        while i < self._stuck:
            successor = a.randomMutant(current)
            valueS = a.evaluate(successor)
            
            if valueS < valueC:
                current = successor
                valueC = valueS
                i = 0              # Reset stuck counter
            else:
                i += 1
        a.setSolution(current)
        a.setMinimum(valueC)
        
    def displaySetting(self):
        print()
        print("Search algorithm: First-Choice Hill Climbing")
        print()
        if self._ProblemType == "1":
            print("Mutation step size:", self._delta)


class SteepestAscent(HillCliming):
    def steepestAscent(self, a):
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
                
        a.setSolution(current)
        a.setMinimum(valueC)

    def displaySetting(self):
        print()
        print("Search algorithm: Steepest-Ascent Hill Climbing")
        print()
        if self._ProblemType == "1":
            print("Mutation step size:", self._delta)

class GradientDescent(HillCliming):
    def gradientDescent(self, a):
        currentA = a.randomInit() # 'current' is a list of values
        valueC = a.evaluate(currentA)
        
        while True:
            nextA = a.takeStep(currentA, valueC)
            valueN = a.evaluate(nextA)
            if valueN >= valueC:
                break
            else:
                currentA = nextA
                valueC = valueN
                
        a.setSolution(currentA)
        a.setMinimum(valueC)
        
    def displaySetting(self):
        print()
        print("Search algorithm: Gradient Desent")
        print()
        print("Mutation step size:", self._delta)
        print("Increment for calculating derivatives:",self._dx)
