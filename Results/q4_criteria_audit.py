"""Q4 figure: the criteria family, audited.

Two Cinelli axioms fail (non-redundancy, exhaustiveness) and one Meeting-4 requirement is
non-binding. These are findings about two DIFFERENT objects — the criteria family and the
requirement set — and are kept apart deliberately.

Panel 2 is the evidence that the redundancy is partly manufactured: the same four formulas
from Appendix B, recomputed on real Rotterdam geometry and real TMY weather.
"""
import glob
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path("/Users/amin/Documents/4_Learning/Summer school/Digital Twin")
OUT = Path("/Users/amin/Documents/4_Learning/Summer school/Results")
OUT.mkdir(parents=True, exist_ok=True)

K = ["pv_potential", "daylighting_potential", "relative_compactness", "fsi_performance"]
SHORT = ["PV", "Daylight", "Compact", "FSI"]
BLUE, RED, GREY, GREEN, AMBER = "#2563eb", "#dc2626", "#a1a1aa", "#059669", "#d97706"


def pc1(M):
    Z = (M - M.mean(0)) / M.std(0)
    ev = np.linalg.eigvalsh(np.corrcoef(Z.T))[::-1]
    return ev[0] / ev.sum()


given = pd.read_csv(ROOT / "data/given/appendix_c.csv")
A = given[K].to_numpy()
TH = np.array([0.70, 0.70, 0.75, 0.80])
ok = (A >= TH).all(1)

fig = plt.figure(figsize=(16, 6.3))
gs = fig.add_gridspec(1, 3, width_ratios=[0.95, 1.15, 1.05], wspace=0.32,
                      left=0.055, right=0.985, top=0.78, bottom=0.20)

# --- 1: the correlation matrix of Appendix C -------------------------------------
ax = fig.add_subplot(gs[0, 0])
C = np.corrcoef(A.T)
im = ax.imshow(C, cmap="RdBu_r", vmin=-1, vmax=1)
for i in range(4):
    for j in range(4):
        ax.text(j, i, f"{C[i, j]:+.2f}", ha="center", va="center", fontsize=10,
                color="white" if abs(C[i, j]) > 0.6 else "#18181b",
                fontweight="bold" if i != j else "normal")
ax.set_xticks(range(4)); ax.set_xticklabels(SHORT, fontsize=9)
ax.set_yticks(range(4)); ax.set_yticklabels(SHORT, fontsize=9)
ax.set_title("1 · The four criteria are near-collinear\nCinelli p.42–43 · every pair |r| ≥ 0.807",
             fontsize=10, loc="left")
ax.text(-0.55, 3.95, "PC1 = 92.4 % of variance\n(90.5 % on the feasible 10)",
        fontsize=9, color=RED, fontweight="bold", va="top")
fig.colorbar(im, ax=ax, shrink=0.62, ticks=[-1, 0, 1])

# --- 2: real geometry destroys the antagonism ------------------------------------
ax = fig.add_subplot(gs[0, 1])
rows = [("Appendix C\n(the case)", len(A), pc1(A), np.corrcoef(A.T)[0, 1], np.corrcoef(A.T)[0, 3])]
for p in sorted(glob.glob(str(ROOT / "data/runs/*/space/performance_normalised.csv"))):
    M = pd.read_csv(p)[K].to_numpy()
    Cx = np.corrcoef(M.T)
    rows.append((p.split("/")[-3].replace("_", "\n"), len(M), pc1(M), Cx[0, 1], Cx[0, 3]))

x = np.arange(len(rows)); w = 0.27
bars = ax.bar(x - w, [r[2] for r in rows], width=w, color=BLUE, label="PC1 (share of variance)")
gbars = ax.bar(x, [abs(r[3]) for r in rows], width=w, color=GREEN, label="|r| PV ~ daylight")
obars = ax.bar(x + w, [abs(r[4]) for r in rows], width=w, color=AMBER, label="|r| PV ~ FSI")
# The case is one column of THREE bars, so mark all three, not just the first.
for b in (bars[0], gbars[0], obars[0]):
    b.set_hatch("///"); b.set_edgecolor("white")
ax.axhline(0, color="#71717a", lw=0.8)
ax.set_xticks(x); ax.set_xticklabels([r[0] for r in rows], fontsize=8)
ax.set_ylim(0, 1.10)
ax.set_ylabel("share of variance  /  |correlation|", fontsize=9)
ax.set_title("2 · Same four formulas, real geometry and weather\nAppendix B recomputed on real BAG + PVGIS data",
             fontsize=10, loc="left")
leg = ax.legend(fontsize=8.2, frameon=False, ncol=3, loc="upper center",
                bbox_to_anchor=(0.5, -0.16))
for h in leg.legend_handles:   # the legend keys the COLOUR; only the case is hatched
    h.set_hatch("")
ax.annotate("PV ↔ daylight antagonism\nnot reproduced:\n−0.98 → −0.04 … +0.37\n(site-dependent)", xy=(1.0, 0.06),
            xytext=(1.42, 0.70), fontsize=8.4, color=GREEN, ha="center",
            arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.3,
                            connectionstyle="arc3,rad=-0.30"))
ax.annotate("PV ↔ FSI persists, far weaker\n0.98 → 0.55–0.68",
            xy=(3.27, 0.70), xytext=(2.20, 0.97), fontsize=8.4, color=AMBER,
            arrowprops=dict(arrowstyle="->", color=AMBER, lw=1.3))
ax.text(0, 1.03, "hatched = the case", fontsize=7.6, color="#52525b", ha="center")
ax.tick_params(labelsize=8)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)

# --- 3: the audit ----------------------------------------------------------------
ax = fig.add_subplot(gs[0, 2])
ax.axis("off")
ax.set_title("3 · Three findings, two different objects", fontsize=10, loc="left", y=1.0)
cells = [
    ["Criteria family\nCinelli p.42–43", "near-collinear\n(a flag)",
     "all six |r| ≥ 0.807\nPC1 = 92.4 %"],
    ["Criteria family\nCinelli p.42–43", "exhaustiveness\nFAILS",
     "shadowing named on\npp. 2 and 4, measured\nby nothing"],
    ["Requirement set\nMeeting 4", "one of four is\nNON-BINDING",
     "drop compactness ≥ .75\n→ same 10 designs, at\nevery tightening level"],
]
tbl = ax.table(cellText=cells, colLabels=["object", "finding", "evidence"],
               cellLoc="left", loc="upper center", colWidths=[0.27, 0.25, 0.42])
tbl.auto_set_font_size(False); tbl.set_fontsize(8.2); tbl.scale(1, 3.1)
for (r, c), cell in tbl.get_celld().items():
    cell.set_edgecolor("#e4e4e7")
    if r == 0:
        cell.set_facecolor("#f4f4f5"); cell.set_text_props(weight="bold", color="#3f3f46")
    elif r <= 2:
        cell.set_facecolor("#fef2f2" if c == 1 else "white")
    else:
        cell.set_facecolor("#fffbeb" if c == 1 else "white")
ax.text(0.0, 0.30,
        "The four criteria are all things the voxel optimiser\n"
        "could compute. The one the brief names twice —\n"
        "effect on the neighbours — is the one it could not,\n"
        "and it is missing.\n\n"
        "Note the distinction: the compactness THRESHOLD\n"
        "never binds, but the compactness CRITERION\n"
        "discriminates strongly (0.63–0.96 across the 30).\n"
        "Different objects, different tests.",
        transform=ax.transAxes, fontsize=8.4, va="top", color="#3f3f46")

fig.suptitle("Q4 · Auditing the criteria family — what Studio Delta should change next time",
             fontsize=13, fontweight="bold", x=0.055, ha="left", y=0.95)
fig.text(0.055, 0.885,
         "Cinelli's criteria-system tests applied to Appendix C, with our own pipeline as the control",
         fontsize=9, color="#52525b")
fig.savefig(OUT / "Q4_criteria_audit.png", dpi=200, facecolor="white")

print(f"{'run':22s} {'n':>3s} {'PC1':>7s} {'r(PV,DL)':>9s} {'r(PV,FSI)':>10s}")
for r in rows:
    print(f"{r[0][:22]:22s} {r[1]:3d} {r[2]:7.3f} {r[3]:+9.3f} {r[4]:+10.3f}")
print("PC1 feasible-10:", round(pc1(A[ok]), 4))
print("compactness range:", A[:, 2].min(), "-", A[:, 2].max())
print("saved:", OUT / "Q4_criteria_audit.png")
