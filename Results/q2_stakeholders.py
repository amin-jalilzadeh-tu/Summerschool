"""Q2 figure: three stakeholders, and where the disagreement actually lives.

The case states four MINIMUMS and no weights, so every weight vector here is the analyst's
assumption. The figure is built to show exactly that: which conclusions survive the choice
of weights and which are artefacts of it.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Patch

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from style import BODY, MUTED, SMALL, apply_defaults, colour_for, mark_zero, tidy
apply_defaults()

GIVEN = Path("/Users/amin/Documents/4_Learning/Summer school/Digital Twin/data/given/appendix_c.csv")
OUT = Path("/Users/amin/Documents/4_Learning/Summer school/Results")
OUT.mkdir(parents=True, exist_ok=True)

K = ["pv_potential", "daylighting_potential", "relative_compactness", "fsi_performance"]
TH = np.array([0.70, 0.70, 0.75, 0.80])
d = pd.read_csv(GIVEN)
ok = (d[K].to_numpy() >= TH).all(axis=1)
Z, ids = d[K].to_numpy()[ok], d.configuration[ok].to_numpy()

BLUE, ORANGE, GREEN, GREY, RED = "#2563eb", "#eb6834", "#059669", "#a1a1aa", "#dc2626"
COL = {c: colour_for(c) for c in ["C21", "C1", "C6", "C14", "C8", "C11", "C15", "C18", "C25", "C28"]}
win = lambda w: ids[int(np.argmax(Z @ np.asarray(w)))]

fig = plt.figure(figsize=(16, 6.4))
gs = fig.add_gridspec(1, 3, width_ratios=[1.25, 1, 1], wspace=0.28,
                      left=0.115, right=0.975, top=0.79, bottom=0.24)

# --- 1: sweep each stakeholder's own criterion weight -----------------------------
ax = fig.add_subplot(gs[0, 0])
sweeps = {
    "Client\n(FSI weight)":        (3, np.linspace(0.25, 0.85, 61)),
    "Engineering\n(compactness)":  (2, np.linspace(0.25, 0.85, 61)),
}
for row, (name, (idx, grid)) in enumerate(sweeps.items()):
    for g in grid:
        w = np.full(4, (1 - g) / 3)
        w[idx] = g
        c = win(w)
        ax.scatter(g, row, s=64, marker="s", color=COL.get(c, GREY), edgecolors="none")
# Municipality: its preference covers TWO criteria, so the x-axis is the TOTAL weight on
# them. Plotting the per-criterion g here would put 0.45 on the same tick as the client's
# 0.45 while actually meaning 0.90 — the same position meaning two different things.
grid = np.linspace(0.50, 0.90, 41)
for g in grid:
    r = (1 - g) / 2
    c = win([g / 2, g / 2, r, r])
    ax.scatter(g, 2, s=64, marker="s", color=COL.get(c, GREY), edgecolors="none")
ax.axvline(5 / 11, color="#71717a", ls="--", lw=1)
ax.text(0.475, 1.32, "engineering flips at\n5/11 = 0.4545\n(equal-remainder sweep)", fontsize=SMALL, color="#52525b")
ax.text(0.25, 2.34, "x is the TOTAL weight on that stakeholder's criteria —\nthe municipality has two, so its row runs 0.50–0.90",
        fontsize=SMALL, color="#71717a")
ax.set_yticks([0, 1, 2])
ax.set_yticklabels(["Client\nFSI weight", "Engineering\ncompactness weight",
                    "Municipality\nPV + daylight"], fontsize=8.5)
ax.set_xlabel("TOTAL weight on that stakeholder's own criteria")
ax.set_title("1 · Whose preferred design survives the weight assumption?\n"
             "each square = the winner at that weight", fontsize=10, loc="left")
ax.set_ylim(-1.05, 2.6)
ax.legend(handles=[Patch(color=COL[c], label=c) for c in ["C8", "C14", "C6", "C1", "C21"]],
          fontsize=8.5, ncol=5, loc="lower center", bbox_to_anchor=(0.5, 0.005),
          frameon=True, framealpha=0.95, edgecolor="none")
ax.tick_params(labelsize=8)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)

# --- 2: the municipality's flip, with the gaps ------------------------------------
ax = fig.add_subplot(gs[0, 1])
profs = [(0.45, "45/45/05/05"), (0.40, "40/40/10/10"), (0.35, "35/35/15/15"),
         (0.30, "30/30/20/20"), (0.25, "25/25/25/25")]
gaps, labels, cols, wins = [], [], [], []
for g, lab in profs:
    r = (1 - 2 * g) / 2
    s = Z @ np.array([g, g, r, r])
    o = np.argsort(-s)
    gaps.append(s[o[0]] - s[o[1]]); labels.append(lab)
    wins.append(ids[o[0]]); cols.append(COL.get(ids[o[0]], GREY))
y = np.arange(len(profs))
ax.barh(y, gaps, color=cols, height=0.6)
for i, (g, w_) in enumerate(zip(gaps, wins)):
    ax.text(g + 0.00012, i, f"{w_}   ({g:.4f})", va="center", fontsize=8.5)
ax.axvline(0.005, color=RED, ls="--", lw=1.2)
ax.text(0.0, -0.155, "±0.005 per score, so a difference carries up to ±0.010.\nEvery margin here is at the precision of the data.",
        transform=ax.transAxes, fontsize=SMALL, color=RED, va="top")
ax.set_yticks(y); ax.set_yticklabels(labels, fontsize=8.5)
ax.invert_yaxis()
ax.set_xlim(0, 0.0092)
ax.set_xlabel("winning margin over the runner-up", fontsize=9)
ax.set_title("2 · The municipality: three winners, all inside the noise\n"
             "five plausible weightings of the same stated preference", fontsize=10, loc="left")
ax.tick_params(labelsize=8)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)

# --- 3: fairness rules across the three actors ------------------------------------
ax = fig.add_subplot(gs[0, 2])
P = {"client": [.10, .10, .10, .70], "muni": [.35, .35, .15, .15], "eng": [.15, .15, .55, .15]}
V = np.column_stack([Z @ np.array(w) for w in P.values()])
N = (V - V.min(0)) / (V.max(0) - V.min(0))
mm, nash = N.min(1), np.prod(N, 1)

# Rank position, not raw value: a product of three numbers and a min of three numbers are
# not the same quantity, so their magnitudes cannot share an axis. Their ORDERINGS can.
rank_nash = np.argsort(np.argsort(-nash)) + 1
rank_mm = np.argsort(np.argsort(-mm)) + 1
order = np.argsort(rank_nash)
for pos, i in enumerate(order):
    ax.plot([0, 1], [rank_nash[i], rank_mm[i]], color=colour_for(ids[i]), lw=2.2, alpha=0.85,
            marker="o", ms=6)
    ax.annotate(ids[i], (0, rank_nash[i]), textcoords="offset points", xytext=(-11, 0),
                ha="right", va="center", fontsize=SMALL, color=colour_for(ids[i]))
    ax.annotate(ids[i], (1, rank_mm[i]), textcoords="offset points", xytext=(11, 0),
                ha="left", va="center", fontsize=SMALL, color=colour_for(ids[i]))
zeros = ids[np.isclose(mm, 0)]
ax.set_xlim(-0.35, 1.35)
ax.set_xticks([0, 1])
ax.set_xticklabels(["Nash product\n(scale-invariant)", "max-min\n(scale-dependent)"], fontsize=SMALL)
ax.set_ylabel("rank among the ten feasible designs")
ax.invert_yaxis()
ax.set_title("3 · Aggregating without a common scale\nVetschera p.33: do not average the vectors",
             loc="left")
ax.text(0.0, -0.155, f"max-min = 0 for {', '.join(sorted(zeros))} — each is somebody's worst,\n"
                     "an artefact of min–max normalisation, not a veto.\n"
                     "Nash is primary: invariant to rescaling per actor.",
        transform=ax.transAxes, fontsize=SMALL, color="#52525b", ha="left", va="top")
tidy(ax)

fig.suptitle("Q2 · Three stakeholders: what survives the weighting assumption, and what does not",
             fontsize=13, fontweight="bold", x=0.03, ha="left", y=0.955)
fig.text(0.03, 0.895,
         "The case states four MINIMUMS and no weights — every weight vector here is ours, and is named on the axis",
         fontsize=9, color="#52525b")
fig.savefig(OUT / "Q2_stakeholders.png", dpi=200, facecolor="white")

print("client  :", [win(np.array([(1-f)/3]*3 + [f])[[0,1,2,3]]) for f in (.40,.55,.70,.85)])
print("nash    :", ids[int(np.argmax(nash))], round(nash.max(), 5))
print("max-min :", ids[int(np.argmax(mm))], round(mm.max(), 3))
print("zeros   :", sorted(zeros.tolist()))
print("saved   :", OUT / "Q2_stakeholders.png")
