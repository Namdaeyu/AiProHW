from Problem import *

def main():
    # Create an instance of numerical optimization problem
    a=Numeric()   # 'p': (expr, domain)
    # Call the search algorithm
    a.createProblem()
    steepestAscent(a)
    # Show the problem and algorithm settings
    a.describeProblem()
    displaySetting()
    # Report results
    a.displayResult()


def steepestAscent(a):
    current = a.randomInit() # 'current' is a list of values
    valueC = a.evaluate(current)
    while True:
        neighbors = a.mutants(current)
        successor, valueS = a.bestOf(neighbors)
        if valueS >= valueC:
            break
        else:
            current = successor
            valueC = valueS
    a.setSolution(current)
    a.setMinimum(valueC)


def displaySetting():
    print()
    print("Search algorithm: Steepest-Ascent Hill Climbing")
    print()
    print("Mutation step size:", DELTA)


main()
