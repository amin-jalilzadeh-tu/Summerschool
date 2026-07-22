import numpy as np
from numpy.typing import NDArray
import gurobipy as gp
from gurobipy import GRB, Model

def BWM(Ab: NDArray[np.float64], Aw: NDArray[np.float64], b: NDArray[np.float64], w: NDArray[np.float64]) -> NDArray[np.float64]:
    """
    Computes the Best Worst Method (BWM) weights.

    Parameters
    ----------
    Ab : np.ndarray
        The best-to-others comparison vector.
    Aw : np.ndarray
        The others-to-worst comparison vector.
    b : np.ndarray
        The best criterion index.
    w : np.ndarray
        The worst criterion index.

    Returns
    -------
    np.ndarray
        The computed weights for each criterion.
    """
    n = len(Ab)
    

    best = int(np.asarray(b).item())
    worst = int(np.asarray(w).item())

    model = Model("BWM")
    model.Params.OutputFlag = 0

    weights = model.addVars(n, lb=0.0, ub=1.0, name="weight")
    xi = model.addVar(lb=0.0, name="xi")

    model.addConstr(sum(weights[i] for i in range(n)) == 1.0, name="sum_weights")

    for j in range(n):
        model.addConstr(weights[best] - Ab[j] * weights[j] <= xi, name=f"best_pos_{j}")
        model.addConstr(Ab[j] * weights[j] - weights[best] <= xi, name=f"best_neg_{j}")
        model.addConstr(weights[j] - Aw[j] * weights[worst] <= xi, name=f"worst_pos_{j}")
        model.addConstr(Aw[j] * weights[worst] - weights[j] <= xi, name=f"worst_neg_{j}")

    model.setObjective(xi, GRB.MINIMIZE)
    model.optimize()

    if model.status != GRB.OPTIMAL:
        raise RuntimeError("BWM LP did not solve to optimality.")

    return np.array([weights[i].X for i in range(n)], dtype=np.float64)
    