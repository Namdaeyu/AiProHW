from Problem import *

def main():
    # Create an instance of numerical optimization problem
    a=Numeric()   # 'p': (expr, domain)
    # Call the search algorithm
    a.createProblem()
    gradientDesent(a)
    # Show the problem and algorithm settings
    a.describeProblem()
    displaySetting()
    # Report results
    a.displayResult()


def gradientDesent(a):
    current = a.randomInit() # 'current' is a list of values
    valueC=0
    valueB=0
    while True:
        valueA = a.evaluate(current)
        neighbors = a.Gmutants(current)
        successor, valueS = a.GbestOf(neighbors,valueA)
        print(valueS)
        if valueS>=-0.01:
            valueR=a.evaluate(successor)
            break
        else:
            current = successor
            valueC=valueB
            valueB=valueS
    a.setSolution(current)
    a.setMinimum(valueR)


def displaySetting():
    print()
    print("Search algorithm: Gradient Desent")
    print()
    print("Mutation step size:", DELTA)


main()
