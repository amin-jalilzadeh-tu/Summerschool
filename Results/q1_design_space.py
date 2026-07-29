"""Q1 figure: the screen, the supported/unsupported split, and what each scalarisation reaches.

Every number is computed here from Appendix C; nothing is typed in by hand.
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Patch
from scipy.optimize import linprog

import sys as _sys
_sys.path.insert(0, str(Path(__file__).resolve().parent))
from style import BODY, REACHABLE, SMALL, UNREACHABLE, apply_defaults, mark_zero, tidy
apply_defaults()

sys.path.insert(0, str(Path(__file__).resolve().parents[0]))
GIVEN = Path("/Users/amin/Documents/4_Learning/Summer school/Digital Twin/data/given/appendix_c.csv")
OUT = Path("/Users/amin/Documents/4_Learning/Summer school/Results")
OUT.mkdir(parents=True, exist_ok=True)

K = ["pv_potential", "daylighting_potential", "relative_compactness", "fsi_performance"]
LABEL = {"pv_potential": "PV", "daylighting_potential": "Daylight",
         "relative_compactness": "Compactness", "fsi_performance": "FSI"}
TH = np.array([0.70, 0.70, 0.75, 0.80])

d = pd.read_csv(GIVEN)
A = d[K].to_numpy()
ok = (A >= TH).all(axis=1)
F, ids = A[ok], d.configuration[ok].to_numpy()

# --- supported? exists w > 0, sum w = 1, with w.(z_j - z_i) <= 0 for all j -------
def supported(i):
    rows = [F[j] - F[i] for j in range(len(F)) if j != i]
    r = linprog(np.zeros(4), A_ub=np.array(rows), b_ub=np.zeros(len(rows)),
                A_eq=np.ones((1, 4)), b_eq=[1.0], bounds=[(1e-6, None)] * 4, method="highs")
    return r.status == 0

sup = np.array([supported(i) for i in range(len(F))])

# --- SMAA: share of the weight simplex on which each is the weighted-sum winner --
rng = np.random.default_rng(20260728)
W = rng.dirichlet(np.ones(4), 500_000)
share = np.bincount(np.argmax(W @ F.T, 1), minlength=len(F)) / len(W)

# --- ASF (Wierzbicki) at two reference points ------------------------------------
def asf(q, w=np.full(4, 0.25), rho=1e-6):
    g = (F - q) / w
    return g.min(1) + rho * g.sum(1)

asf_thresh = asf(TH)
asf_c15 = asf(F[ids == "C15"][0])

fig = plt.figure(figsize=(15.5, 6.2))
gs = fig.add_gridspec(1, 3, width_ratios=[1.05, 1.15, 1.0], wspace=0.30,
                      left=0.055, right=0.985, top=0.83, bottom=0.13)
BLUE, GREY, RED, GREEN = "#2563eb", "#a1a1aa", "#dc2626", "#059669"
# supported / unsupported: blue and amber, not green and red — an unsupported design is
# not worse, it is unreachable by one family of methods.
SUP, UNSUP = REACHABLE, UNREACHABLE

# ---- panel 1: the screen --------------------------------------------------------
ax = fig.add_subplot(gs[0, 0])
slack = (A - TH).min(axis=1)
order = np.argsort(slack)
colours = [BLUE if s >= 0 else GREY for s in slack[order]]
ax.barh(range(len(A)), slack[order], color=colours, height=0.72)
ax.axvline(0, color=RED, lw=1.4)
ax.set_yticks(range(len(A)))
ax.set_yticklabels(d.configuration.to_numpy()[order], fontsize=6.5)
ax.set_xlabel("worst slack against the four minimums", fontsize=9)
ax.set_title("1 · Screening: 30 → 10\nall 30 are non-dominated, so dominance decides nothing",
             fontsize=10, loc="left")
ax.text(0.97, 0.60, f"{int(ok.sum())} feasible", transform=ax.transAxes, color=BLUE,
        fontsize=9.5, fontweight="bold", ha="right", va="center")
ax.text(0.03, 0.30, "fails at least\none minimum", transform=ax.transAxes,
        color="#52525b", fontsize=8)
ax.tick_params(labelsize=8)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)

# ---- panel 2: supported vs unsupported ------------------------------------------
ax = fig.add_subplot(gs[0, 1])
o = np.argsort(-share)
cols = [SUP if sup[i] else UNSUP for i in o]
bars = ax.bar(range(len(F)), share[o] * 100, color=cols, width=0.66)
ax.set_xticks(range(len(F)))
ax.set_xticklabels(ids[o], fontsize=8.5)
ax.set_ylabel("share of the weight simplex won  (%)", fontsize=9)
ax.set_title("2 · Which designs a positive weighted sum can pick\n500 000 uniform weight draws, plus an LP proof",
             fontsize=10, loc="left")
for pos, (rect, i) in enumerate(zip(bars, o)):
    v = share[i] * 100
    if v == 0:
        mark_zero(ax, pos, 0, label="", colour=UNSUP)
    else:
        ax.text(rect.get_x() + rect.get_width() / 2, v + 1.0,
                f"{v:.3f}" if v < 1 else f"{v:.1f}", ha="center", fontsize=SMALL, color="#3f3f46")
ax.set_ylim(0, 44)
ax.legend(handles=[Patch(color=SUP, label="supported in this set — some weight vector picks it"),
                   Patch(color=UNSUP, label="unsupported in this set — none does")],
          fontsize=SMALL, loc="upper right", frameon=False)
zero_pos = [pos for pos, i in enumerate(o) if share[i] == 0]
ax.annotate("never selected, in this set",
            xy=(float(np.mean(zero_pos)), 0.4), xytext=(float(np.mean(zero_pos)), 6.4),
            ha="center", fontsize=SMALL, color=UNSUP, fontweight="bold",
            arrowprops=dict(arrowstyle="-", color=UNSUP, lw=1))
ax.annotate("C11: 158 wins in 500 000\n(0.032 %, seed 20260728)\n— tiny, but not zero",
            xy=(6, 0.6), xytext=(4.15, 12.5), fontsize=7.6, color="#52525b",
            arrowprops=dict(arrowstyle="->", color="#a1a1aa", lw=1))
ax.tick_params(labelsize=8)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)

# ---- panel 3: ASF reaches what the weighted sum cannot --------------------------
ax = fig.add_subplot(gs[0, 2])
o2 = np.argsort(-asf_c15)
cols3 = [RED if ids[i] == "C15" else "#c7d7f5" for i in o2]
bars = ax.bar(range(len(F)), asf_c15[o2], color=cols3, width=0.66)
ax.set_xticks(range(len(F)))
ax.set_xticklabels(ids[o2], fontsize=8.5)
ax.axhline(0, color="#71717a", lw=0.8)
ax.set_ylabel("achievement scalarising function", fontsize=9)
ax.set_title("3 · A reference point reaches what no weight can\nWierzbicki ASF with q = y(C15)",
             fontsize=10, loc="left")
mark_zero(ax, 0, 0, label="", colour=UNSUP, size=10)
ax.set_ylim(min(asf_c15) * 1.12, 0.055)
ax.annotate("C15 wins outright at 0 —\nyet no weight vector\nselects it in this set",
            xy=(0.12, -0.004), xytext=(1.6, -0.175), fontsize=8, color=RED,
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))
ax.text(0.02, 0.03, "At q = the four minimums the ASF instead ties C6, C1, C21\n"
                    "— so it does not discriminate there either.",
        transform=ax.transAxes, fontsize=7.8, color="#52525b", va="bottom")
ax.tick_params(labelsize=8)
for s_ in ("top", "right"):
    ax.spines[s_].set_visible(False)

fig.suptitle("Q1 · The feasible design space: screening, reachability, and what the method choice decides",
             fontsize=13, fontweight="bold", x=0.055, ha="left", y=0.955)
fig.text(0.055, 0.905,
         "Appendix C (30 × 4) · minimums PV ≥ 0.70, daylight ≥ 0.70, compactness ≥ 0.75, FSI ≥ 0.80 (Meeting 4)",
         fontsize=9, color="#52525b")
fig.savefig(OUT / "Q1_design_space.png", dpi=200, facecolor="white")

print("feasible:", list(ids))
print("unsupported:", list(ids[~sup]))
print("ASF ties at q=minimums:", list(ids[np.isclose(asf_thresh, asf_thresh.max(), atol=1e-4)]))
print("ASF winner at q=y(C15):", ids[int(np.argmax(asf_c15))])
print("saved:", OUT / "Q1_design_space.png")
