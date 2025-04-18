import numpy as np
import time
from facility_gurobi import gurobi_opt
from facility_tabu import tabu_search
import matplotlib.pyplot as plt

# parameter
facilityCnt = 13
customerCnt = 13
fixedCost = [3000000, 3000000, 700000, 900000, 850000, 800000, 750000, 750000, 750000, 800000, 400000, 500000, 500000]
demand = [1560, 2110, 320, 1000, 1060, 810, 560, 450, 370, 505, 100, 110, 230]
max_stag = 10
tabu_tenure = 7


# distance matrix
distanceMatrix = [
    [0.00, 4.97, 6.20, 5.15, 8.69, 10.07, 13.73, 16.35, 20.09, 10.65, 32.96, 15.97, 17.16],
    [4.97, 0.00, 5.75, 9.88, 10.75, 12.03, 8.89, 11.88, 17.69, 9.77, 37.28, 19.97, 20.82],
    [17.50, 12.00, 0.00, 10.00, 6.50, 21.50, 24.50, 28.00, 39.00, 8.50, 39.50, 26.50, 30.50],
    [5.15, 9.88, 8.36, 0.00, 7.09, 12.38, 18.76, 21.50, 24.70, 11.73, 30.42, 14.68, 16.39],
    [8.69, 10.75, 5.56, 7.09, 0.00, 18.44, 18.68, 22.21, 28.21, 5.97, 37.00, 21.76, 23.47],
    [10.07, 12.03, 16.07, 12.38, 18.44, 0.00, 17.06, 17.51, 14.99, 20.58, 27.22, 10.13, 10.04],
    [13.73, 8.89, 13.12, 18.76, 18.68, 17.06, 0.00, 3.92, 14.01, 15.33, 44.12, 26.73, 27.02],
    [16.35, 11.88, 16.70, 21.50, 22.21, 17.51, 3.92, 0.00, 10.96, 19.19, 44.71, 27.56, 27.54],
    [20.09, 17.69, 23.43, 24.70, 28.21, 14.99, 14.01, 10.96, 0.00, 27.15, 39.72, 24.32, 23.44],
    [10.65, 9.77, 4.51, 11.73, 5.97, 20.58, 15.33, 19.19, 27.15, 0.00, 42.15, 26.02, 27.46],
    [32.96, 37.28, 38.50, 30.42, 37.00, 27.22, 44.12, 44.71, 39.72, 42.15, 0.00, 17.44, 17.18],
    [15.97, 19.97, 21.92, 14.68, 21.76, 10.13, 26.73, 27.56, 24.32, 26.02, 17.44, 0.00, 2.21],
    [17.16, 20.82, 23.24, 16.39, 23.47, 10.04, 27.02, 27.54, 23.44, 27.46, 17.18, 2.21, 0.00]
]

# gurobi
# gurobi
start_gurobi = time.time()
gurobi_score = gurobi_opt(facilityCnt, customerCnt, fixedCost, demand, distanceMatrix)
end_gurobi = time.time()

# Tabu Search
start_tabu = time.time()
tabu_score, history = tabu_search(facilityCnt, customerCnt, fixedCost, demand, distanceMatrix, max_stag, tabu_tenure)
end_tabu = time.time()

# print the optimal solution
print("\n------------------------------------")
print(f"Gurobi Best score: {gurobi_score}")
print(f"Gurobi execution time (sec) = {end_gurobi - start_gurobi}")
print(f"\nTabu Best score: {tabu_score}")
print(f"Tabu execution time (sec) = {end_tabu - start_tabu}")
print(f"\nOptimality Gap: {(tabu_score - gurobi_score) / gurobi_score:.2%}")

# plot the tabu search progress
scaled_history = [score / 10000 for score in history]
scaled_gurobi_score = gurobi_score / 10000
plt.plot([i for i in range(len(history))], scaled_history, label = f"max_stagnation = {max_stag}, tenure = {tabu_tenure}")
plt.plot([i for i in range(len(history))], [scaled_gurobi_score] * len(history), label = "optimal sol")
plt.xlabel('Iteration')
plt.ylabel('Best Score (ten thousand)')
plt.title('Tabu Search Progress')
plt.legend()
plt.show()
