from Setup import *
from optimizer import *
from Problem import *

def main():
    pt=input("Select the problem type:\n\t1.Numerical Optimization\n\t2.Tsp\nEnter the number:")
    fn=input("Enter the file name of a function:")
    if pt == "1":                   ##Numeric Optimizer
        sa=input("Select the search algorithm:\n\t1. Steepest-Ascent\n\t2. First-Choice\n\t3. Gradient Descent\nEnter the number:")
        if sa == "1":               ##Steepest-Ascent algrorithm
            b = Numeric()
            b.setAll(pt,fn,sa)
            b.createProblem()
            
            c = SteepestAscent()
            c.setAll(pt,fn,sa)
            c.steepestAscent(b)
            
            b.describeProblem()
            c.displaySetting()
            b.displayResult()
            
        elif sa == "2":             ##First-choice algorithm
            b = Numeric()
            b.setAll(pt,fn,sa)
            b.createProblem()
            
            c = FirstChoice()
            c.setAll(pt,fn,sa)
            c.firstChoice(b)
            
            b.describeProblem()
            c.displaySetting()
            b.displayResult()
            
        elif sa == "3":             ##Gradient-descent algorithm
            b = Numeric()
            b.setAll(pt,fn,sa)
            b.createProblem()
            
            c = GradientDescent()
            c.setAll(pt,fn,sa)
            c.gradientDescent(b)
            
            b.describeProblem()
            c.displaySetting()
            b.displayResult()
            
    elif pt == "2":                 ##Tsp function
        sa=input("Select the search algorithm:\n\t1. Steepest-Ascent\n\t2. First-Choice\nEnter the number:")
        if sa == "1":               ##Steepest-Ascent algorithm
            b = Tsp()
            b.setAll(pt,fn,sa)
            b.createProblem()
            
            c = SteepestAscent()
            c.setAll(pt,fn,sa)
            c.steepestAscent(b)
            
            b.describeProblem()
            c.displaySetting()
            b.displayResult()
            
        elif sa == "2":             ##First-choice algorithm
            b = Tsp()
            b.setAll(pt,fn,sa)
            b.createProblem()
            
            c = FirstChoice()
            c.setAll(pt,fn,sa)
            c.firstChoice(b)
            
            b.describeProblem()
            c.displaySetting()
            b.displayResult()
            
        
            
main()
