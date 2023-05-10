from Problem import *

LIMIT_STUCK = 100 # Max number of evaluations enduring no improvement
   # Total number of evaluations


def main():
    # Create an instance of numerical optimization problem
    a=Tsp()   # 
    # Call the search algorithm
    a.createProblem()
    firstChoice(a)
    # Show the problem and algorithm settings
    a.describeProblem()
    displaySetting()
    # Report results
    a.displayResult()
    

def firstChoice(a):
    current = a.randomInit()   # 'current' is a list of city ids
    valueC = a.evaluate(current)
    i = 0
    while i < LIMIT_STUCK:
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

def displaySetting():
    print()
    print("Search algorithm: First-Choice Hill Climbing")



main()
