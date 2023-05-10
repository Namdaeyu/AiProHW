import numpy as np
import matplotlib.pyplot as plt

y1 = []
infile = open("firstChoice.txt", 'r')

for line in infile:
    y1.append(float(line))
    
infile.close()
x1 = np.arange(len(y1))

y2 = []
infile = open("SA.txt", 'r')

for line in infile:
    y2.append(float(line))
    
infile.close()
x2 = np.arange(len(y2))

plt.plot(x1, y1)
plt.plot(x2, y2)

plt.xlabel('Number of Evaluations')
plt.ylabel('Tour Cost')
plt.title('Search Performance (TSP-100)')

plt.legend(['First-Choice HC', 'Simulated Annealing'])
plt.show()

