"""Q3 figure: parametric epsilon-constraint analysis of the four stakeholder minimums.

Two things this script is careful about.

**Exact arithmetic.** Appendix C is published to two decimals and two configurations sit at
exact equality (C8 daylight 0.70, C14 PV 0.70). In binary floating point
0.80 + 0.14 = 0.9400000000000001, so C8 fails its own FSI limit by 1e-16 and the reported
slack comes out one step short. All threshold comparisons are therefore in integer
hundredths.

**Supportedness is relative to a set.** An earlier version of this figure claimed C15 was
"unsupported, so no weighted sum can ever select it" while the same panel showed a weighted
sum selecting it. Both cannot be true: supportedness is a property of an alternative
*within a given set*, and removing C8 uncovers C15 on the hull. The panel now says what
actually happens, which is the more interesting finding — moving a threshold changes the
geometry of the feasible set, not just the winner.
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import linprog

sys.path.insert(0, str(Path(__file__).resolve().parent))
from style import (BODY, ELIMINATED, INK, KEPT, MUTED, REACHABLE, RULE, SMALL,
                   UNREACHABLE, apply_defaults, mark_zero, tidy)

apply_defaults()
GIVEN = Path("/Users/amin/Documents/4_Learning/Summer school/Digital Twin/data/given/appendix_c.csv")
OUT = Path(__file__).resolve().parent

K = ["pv_potential", "daylighting_potential", "relative_compactness", "fsi_performance"]
NICE = {"pv_potential": "PV", "daylighting_potential": "Daylight",
        "relative_compactness": "Compactness", "fsi_performance": "FSI"}
OWNER = {"pv_potential": "municipality", "daylighting_potential": "municipality",
         "relative_compactness": "engineering", "fsi_performance": "client"}

d = pd.read_csv(GIVEN)
A = d[K].to_numpy()
Ai = np.rint(A * 100).astype(int)
ids = d.configuration.to_numpy()
B = np.array([70, 70, 75, 80])
CLIENT = np.array([.10, .10, .10, .70])


def supported(Z, i):
    """Can alternative i attain the maximum of some strictly positive weighted sum?

    The LP allows ties, so this asks whether i can reach the top, not whether it can reach
    it alone. Answered within the set Z: remove a competitor and the answer can change.
    """
    rows = [Z[j] - Z[i] for j in range(len(Z)) if j != i]
    r = linprog(np.zeros(4), A_ub=np.array(rows), b_ub=np.zeros(len(rows)),
                A_eq=np.ones((1, 4)), b_eq=[1.0], bounds=[(1e-6, None)] * 4, method="highs")
    return r.status == 0


fig = plt.figure(figsize=(16.5, 6.6))
gs = fig.add_gridspec(1, 3, width_ratios=[1.06, 1.0, 1.12], wspace=0.30,
                      left=0.055, right=0.985, top=0.78, bottom=0.15)

# --- 1: simultaneous shift -------------------------------------------------------
ax = fig.add_subplot(gs[0, 0])
deltas = np.arange(-5, 7)
counts = [int((Ai >= B + dd).all(1).sum()) for dd in deltas]
cols = [MUTED if dd < 0 else REACHABLE for dd in deltas]
ax.bar(deltas, counts, color=cols, width=0.72)
for dd, c in zip(deltas, counts):
    if c:
        ax.text(dd, c + 0.45, str(c), ha="center", fontsize=SMALL, color="#3f3f46")
mark_zero(ax, 6, 0, label="EMPTY", colour=ELIMINATED, fontsize=BODY)
ax.axvline(0, color=INK, lw=1.2)
ax.text(0.2, 16.0, "as agreed\nin Meeting 4", fontsize=SMALL, color=INK)
ax.text(3.0, 10.4, "+0.05 → C1, C6, C21", fontsize=SMALL, color="#3f3f46", ha="center")
ax.set_xlabel("all four minimums shifted together (hundredths)")
ax.set_ylabel("feasible configurations")
ax.set_title("1 · Six hundredths from infeasibility\nKöksalan II p.11 — vary εᵢ systematically",
             loc="left")
ax.set_xticks(deltas)
ax.set_xticklabels([f"{dd:+d}" for dd in deltas])
ax.set_ylim(0, 19)
tidy(ax)

# --- 2: which requirements do work -----------------------------------------------
ax = fig.add_subplot(gs[0, 1])
rows = []
for j, k in enumerate(K):
    others = np.all([Ai[:, i] >= B[i] for i in range(4) if i != j], 0)
    uniq = ids[others & (Ai[:, j] < B[j])]
    rows.append((k, len(uniq), list(uniq)))
y = np.arange(4)
for i, (k, v, names) in enumerate(rows):
    if v:
        ax.barh(i, v, color=KEPT, height=0.5)
        ax.text(v + 0.06, i, f"saves {names[0]}", va="center", fontsize=BODY, color="#3f3f46")
    else:
        mark_zero(ax, 0, i, label="eliminates nothing", colour=ELIMINATED,
                  fontsize=BODY, orientation="horizontal")
ax.set_yticks(y)
ax.set_yticklabels([f"{NICE[k]} ≥ {B[j]/100:.2f}\n({OWNER[k]})" for j, k in enumerate(K)],
                   fontsize=SMALL)
ax.invert_yaxis()
ax.set_xlim(0, 1.45)
ax.set_xticks([0, 1])
ax.set_xlabel("configurations it uniquely eliminates")
ax.set_title("2 · One requirement does no work\nwhat each removes that the others do not",
             loc="left")
ax.text(0.30, 2.38, "stays non-binding at every tightening\nlevel from +0.00 to +0.05",
        fontsize=SMALL, color=ELIMINATED, va="top")
tidy(ax)

# --- 3: the knife edge, and what it does to the geometry --------------------------
ax = fig.add_subplot(gs[0, 2])
ax.axis("off")
scen = [("as agreed", B), ("daylight 0.70 → 0.71", B + np.array([0, 1, 0, 0]))]
cells = []
for label, t in scen:
    m = (Ai >= t).all(1)
    Z, sub = A[m], ids[m]
    sup = [supported(Z, i) for i in range(len(Z))]
    unsup = [s for s, k in zip(sub, sup) if not k]
    winner = sub[int(np.argmax(Z @ CLIENT))]
    cells.append([label, str(int(m.sum())), winner, ", ".join(unsup)])

tbl = ax.table(cellText=cells,
               colLabels=["scenario", "feasible", "client\npicks", "unsupported\nin that set"],
               cellLoc="center", loc="upper center", colWidths=[0.30, 0.15, 0.16, 0.32])
tbl.auto_set_font_size(False)
tbl.set_fontsize(SMALL)
tbl.scale(1, 2.9)
for (r, c), cell in tbl.get_celld().items():
    cell.set_edgecolor(RULE)
    if r == 0:
        cell.set_facecolor("#f4f4f5")
        cell.set_text_props(weight="bold", color="#3f3f46")
    elif r == 2 and c == 2:
        # C15 became SUPPORTED here — amber would say the opposite of the finding
        cell.set_facecolor("#dbeafe")
        cell.set_text_props(weight="bold", color=REACHABLE)
    elif r == 2 and c == 3:
        cell.set_facecolor("#fef3c7")
        cell.set_text_props(weight="bold", color=UNREACHABLE)
ax.set_title("3 · A hundredth changes the shape of the problem\nC8 sits at daylight = 0.70 exactly; C14 at PV = 0.70",
             loc="left", y=1.02)
ax.text(0.0, 0.55,
        "Raising the municipality's daylight floor by one hundredth removes\n"
        "C8 — the client's preferred design. But it does more than change the\n"
        "winner: it changes the geometry of the feasible set.\n\n"
        "C15 is unsupported among the baseline ten — no positive\n"
        "weighted sum selects it there. With C8 gone it becomes supported,\n"
        "and the client's own weighted sum then selects it.\n\n"
        "Supportedness is a property of an alternative WITHIN A SET, not a\n"
        "fixed label. Moving a threshold rewrites which designs a\n"
        "weighted-sum method can reach at all.",
        transform=ax.transAxes, fontsize=SMALL, va="top", color="#3f3f46", linespacing=1.45)

fig.suptitle("Q3 · Tightening and relaxing the stakeholder requirements",
             fontsize=14, fontweight="bold", x=0.055, ha="left", y=0.955)
fig.text(0.055, 0.885,
         "Parametric ε-constraint analysis · all threshold comparisons in exact hundredths, "
         "because two designs sit at equality",
         fontsize=SMALL, color=MUTED)
fig.savefig(OUT / "Q3_thresholds.png", dpi=200, facecolor="white")

print("simultaneous:", dict(zip([f"{x:+d}" for x in deltas], counts)))
print("uniquely eliminates:", {NICE[k]: v for k, v, _ in rows})
for row in cells:
    print("  ", row)
print("saved:", OUT / "Q3_thresholds.png")
