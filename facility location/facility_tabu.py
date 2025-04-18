import random

def total_cost(facilities_open, customerCnt, facilityCnt, fixedCost, distanceMatrix):
    totalCost = 0

    # assign customer to the nearest facility
    for i in range(customerCnt):
        assigned_facility = min(
            [j for j in range(facilityCnt) if facilities_open[j]],
            key = lambda j: distanceMatrix[i][j],
            default = -1
        )
        if assigned_facility == -1:
            return float("inf")  # infeasible if no facility open
        totalCost += distanceMatrix[i][assigned_facility]

    # plus the fixed cost
    totalCost += sum(fixedCost[j] for j in range(facilityCnt) if facilities_open[j])
    return totalCost


def tabu_search(facilityCnt, customerCnt, fixedCost, demand, distanceMatrix, max_stag , tabu_tenure):

    # initialize: randomly open several facilities until feasible
    while True:
        current_facilities = [random.choice([0, 1]) for _ in range(facilityCnt)]
        cost = total_cost(current_facilities, customerCnt, facilityCnt, fixedCost, distanceMatrix)
        if cost < float('inf'):
            break

    best_facilities = current_facilities[:]  # not returned currently
    best_cost = cost
    history = []  # used in plot

    tabu_list = []
    stag = 0

    while stag < max_stag:
        best_neighbor = None
        best_neighbor_cost = float("inf")
        
        # find the best neighbor
        for j in range(facilityCnt):
            neighbor = current_facilities[:]
            neighbor[j] = 1 - neighbor[j]  # flip

            n_cost = total_cost(neighbor, customerCnt, facilityCnt, fixedCost, distanceMatrix)

            # condition: not in tabu, except better than best_cost
            if (neighbor not in tabu_list and n_cost < best_neighbor_cost) \
                or (n_cost < best_cost):
                best_neighbor = neighbor[:]
                best_neighbor_cost = n_cost

        if best_neighbor is None:
            break  # no feasible neighbor

        current_facilities = best_neighbor[:]
        cost = total_cost(current_facilities, customerCnt, facilityCnt, fixedCost, distanceMatrix)

        # add to tabu
        tabu_list.append(best_neighbor)
        if len(tabu_list) > tabu_tenure:
            tabu_list.pop(0)

        # renew best_cost
        if cost < best_cost:
            best_cost = cost
            best_facilities = current_facilities[:]
            stag = 0  # reset
        else:
            stag += 1
        
        history.append(best_cost)

    return best_cost, history
