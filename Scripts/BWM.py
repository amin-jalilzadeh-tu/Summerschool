import numpy as np
from numpy.typing import NDArray
import gurobipy as gp
from gurobipy import GRB, Model

def _infer_identity_index(values: NDArray[np.float64], label: str) -> int:
    matches = np.flatnonzero(np.isclose(values, 1.0))
    if matches.size != 1:
        raise ValueError(f"{label} must contain exactly one entry equal to 1.0.")
    return int(matches[0])


def BWM(Ab: NDArray[np.float64], Aw: NDArray[np.float64]) -> NDArray[np.float64]:
    """
    Computes the Best Worst Method (BWM) weights.

    Parameters
    ----------
    Ab : np.ndarray
        The best-to-others comparison vector.
    Aw : np.ndarray
        The others-to-worst comparison vector.

    Returns
    -------
    np.ndarray
        The computed weights for each criterion.
    """
    Ab = np.asarray(Ab, dtype=np.float64)
    Aw = np.asarray(Aw, dtype=np.float64)

    if Ab.shape != Aw.shape:
        raise ValueError("Ab and Aw must have the same shape.")

    n = len(Ab)

    best = _infer_identity_index(Ab, "Ab")
    worst = _infer_identity_index(Aw, "Aw")

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
    