from gurobipy import *

def gurobi_opt(facilityCnt, customerCnt, fixedCost, demand, distanceMatrix):
    model = Model("CapacitatedFacilityLocation")

    # Decision variables
    x = model.addVars(customerCnt, facilityCnt, vtype = GRB.BINARY)
    y = model.addVars(facilityCnt, vtype = GRB.BINARY)

    # Objective: minimize fixed cost + transportation cost
    model.setObjective(
        quicksum(fixedCost[j] * y[j] for j in range(facilityCnt)) +
        quicksum(distanceMatrix[i][j] * x[i,j] for i in range(customerCnt) for j in range(facilityCnt)),
        GRB.MINIMIZE)

    # Constraint 1: e customer is assigned to exactly one facility
    for i in range(customerCnt):
        model.addConstr(quicksum(x[i,j] for j in range(facilityCnt)) == 1)

    # Constraint 2: if yi = 0, then demand[i] * x[i, j] = 0
    for j in range(facilityCnt):
        for i in range(customerCnt):
            model.addConstr(demand[i] * x[i,j] <= demand[i] * y[j])

    # solve
    model.optimize()
    return model.ObjVal