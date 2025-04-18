import numpy as np
import time
from TSP_tabu import tabu_search
from TSP_gurobi import gurobi_opt
import matplotlib.pyplot as plt

# parameter
node_cnt = 50
max_dist = 100
max_stagnation = 50
tabu_tenure = 20  # the size of the tabu


# randomly generate the "coordinate" and then generate the distance matrix
coords = np.random.rand(node_cnt, 2) * max_dist
distance_matrix = np.zeros((node_cnt, node_cnt))

for i in range(node_cnt):
    for j in range(i + 1, node_cnt):
        dist = np.linalg.norm(coords[i] - coords[j])
        distance_matrix[i][j] = dist
        distance_matrix[j][i] = dist  # symmetry


# gurobi
start_gurobi = time.time()
gurobi_score = gurobi_opt(distance_matrix)
end_gurobi = time.time()

# Tabu Search
start_tabu = time.time()
tabu_score, history = tabu_search(node_cnt, distance_matrix, max_stagnation, tabu_tenure)
end_tabu = time.time()

# print the optimal solution
print("\n------------------------------------")
print(f"Gurobi Best score: {gurobi_score}")
print(f"Gurobi execution time (sec) = {end_gurobi - start_gurobi}")
print(f"\nTabu Best score: {tabu_score}")
print(f"Tabu execution time (sec) = {end_tabu - start_tabu}")
print(f"\nOptimality Gap: {(tabu_score - gurobi_score) / gurobi_score:.2%}")


# plot the tabu search progress
plt.plot([i for i in range(len(history))], history, label = f"max_stagnation = {max_stagnation}, tenure = {tabu_tenure}")
plt.plot([i for i in range(len(history))], [gurobi_score] * len(history), label = "optimal sol")
plt.xlabel('Iteration')
plt.ylabel('Best Score')
plt.title('Tabu Search Progress')
plt.legend()
plt.show()
