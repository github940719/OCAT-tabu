# generate the initial solution (greedily choose the nearest node)
def initial_solution(node_cnt, dist_matrix):
    unvisited = set(range(1, node_cnt))  # set of unvisited nodes
    route = [0]     # the initial solution (e.g. [A, B, C, D, E, A])
    temp = 0        # from the starting point
    total_dist = 0  # the cumuulative total distance
    
    while unvisited:    # find the nearest unvisited node
        nearest = min(unvisited, key = lambda x: dist_matrix[temp][x])
        route.append(nearest)
        unvisited.remove(nearest)
        total_dist += dist_matrix[temp][nearest]
        temp = nearest

    total_dist += dist_matrix[route[-1]][0]  # back to starting point
    route.append(0)
    return route, total_dist


def find_best_neigh(node_cnt, dist, route, former_score, best_score, tabu):
    # record the information of the best neighbor
    best_neigh_score = float("inf")
    best_neigh = None
    add_edge1 = tuple()
    add_edge2 = tuple()

    # evaluate all neighbor solutions
    for i in range(node_cnt):
        for j in range(i + 2, node_cnt):

            # (A, B) and (C, D) are the deleted edge; (A, C) and (B, D) are the added edge
            A, B, C, D = route[i], route[i+1], route[j], route[j+1]
            neigh = route[:i+1] + route[i+1:j+1][::-1] + route[j+1:]  # sub-tour reversal
            score = former_score - dist[A][B] - dist[C][D] + dist[B][D] + dist[A][C] 
            
            # eliminate the neighbors with both deleted edges on the tabu
            # unless it is better than best_score
            # then choose the best neighbor
            if score < best_score or (score < best_neigh_score and not((A, B) in tabu and (C, D) in tabu)):
                add_edge1 = (B, D)  # record the added edge
                add_edge2 = (A, C)
                best_neigh = neigh
                best_neigh_score = score

    return best_neigh, best_neigh_score, add_edge1, add_edge2


# the main function of tabu search
def tabu_search(node_cnt, dist, max_stagnation, tabu_tenure):

    # initialize the solution
    route, best_score = initial_solution(node_cnt, dist)
    former_score = best_score
    
    tabu = list()   # the tabu : record the edges added in some iteration
    history = []    # best score of each iteration, for plot
    stagnation = 0  # the number of no-improvement iterations
    
    while stagnation < max_stagnation:

        best_neigh, best_neigh_score, add_edge1, add_edge2 = \
        find_best_neigh(node_cnt, dist, route, former_score, best_score, tabu)

        # add to the tabu
        tabu.append(add_edge1)
        tabu.append(add_edge2)

        if len(tabu) >= 2 * tabu_tenure:  # remove the two oldest edges
            tabu.pop(0)
            tabu.pop(0)

        # renew the best score
        if best_neigh_score < best_score:
            best_score = best_neigh_score
            stagnation = 0
        else:
            stagnation += 1
        
        history.append(best_score)
        route = best_neigh
        former_score = best_neigh_score
    
    return best_score, history
