from gurobipy import *

def gurobi_opt(distance_matrix):
    nodeCnt = len(distance_matrix)
    try:
        # create a new model
        m = Model("TSP")

        # create decision variables
        x = m.addVars(nodeCnt, nodeCnt, vtype = GRB.BINARY, name = "x")
        for i in range(nodeCnt):
            m.addConstr(x[i, i] == 0)

        u = m.addVars(nodeCnt, vtype = GRB.INTEGER, name = "u") # ui = j means that the node i is visited jth in the route

        # set objective function
        m.setObjective(quicksum(distance_matrix[i][j] * x[i, j] for i in range(nodeCnt) for j in range(nodeCnt)), GRB.MINIMIZE)

        # add constraints
        for i in range(nodeCnt) :
            m.addConstr(sum(x[i, j] for j in range(nodeCnt)) == 1)  # outflow
            m.addConstr(sum(x[j, i] for j in range(nodeCnt)) == 1)  # inflow

        # for u
        for i in range(1, nodeCnt):
            m.addConstr(u[i] >= 1)
            m.addConstr(u[i] <= nodeCnt - 1)
        m.addConstr(u[0] == 0)

        # eliminate subtours
        for i in range(1, nodeCnt):
            for j in range(1, nodeCnt):
                if i != j:
                    m.addConstr(u[i] - u[j] + nodeCnt * x[i, j] <= nodeCnt - 1)

        # optimize the mode
        m.optimize()
        return m.ObjVal

    except GurobiError:
        print("Encountered a Gurobi error")
