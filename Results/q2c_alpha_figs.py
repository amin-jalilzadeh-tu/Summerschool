"""Four pictures for Q2, each one a slide from Koksalan Part I redrawn on our ten designs."""
import itertools
from pathlib import Path
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np, pandas as pd
import style as S

HERE = Path(__file__).resolve().parent
CSV  = "/Users/amin/Documents/4_Learning/Summer school/Digital Twin/data/given/appendix_c.csv"
K    = ["pv_potential","daylighting_potential","relative_compactness","fsi_performance"]
TH   = [0.70,0.70,0.75,0.80]
S.apply_defaults()

d     = pd.read_csv(CSV).set_index("configuration")
Z     = d.loc[((d[K]*100).round() >= np.array(TH)*100).all(axis=1), K]
ideal = Z.max()
GAP   = (ideal - Z)
col   = lambda c: S.colour_for(c)

def L(w, a):
    g = w * GAP
    return g.max(axis=1) if a == np.inf else (g**a).sum(axis=1)**(1/a)

ENG   = np.array([.15,.15,.55,.15])
PROF  = {"Client 10/10/10/70":[.10,.10,.10,.70], "Municipality 35/35/15/15":[.35,.35,.15,.15],
         "Engineering 15/15/55/15":list(ENG),    "Equal 25/25/25/25":[.25,.25,.25,.25]}
AGRID = [1,1.25,1.5,2,2.5,3,4,6,10,np.inf]

fig = plt.figure(figsize=(16.5,8.6))
gs  = fig.add_gridspec(2,2, hspace=0.42, wspace=0.24, left=.055, right=.985, top=.855, bottom=.075)

# --- 1 : slide 31 redrawn, illustrative 2-criterion slice -------------------------
ax = fig.add_subplot(gs[0,0])
gx, gy = GAP["pv_potential"].values, GAP["relative_compactness"].values
w2 = 0.5
t  = np.linspace(0, np.pi/2, 400)
for a, ls in [(1,"-"),(2,"-"),(4,"-"),(np.inf,"-")]:
    r = 0.075
    if a == np.inf:
        ax.plot([0,r/w2,r/w2],[r/w2,r/w2,0], color=S.MUTED, lw=1.3)
        ax.annotate("α=∞", (r/w2, r/w2), xytext=(4,4), textcoords="offset points",
                    fontsize=9.5, color=S.MUTED)
    else:
        x = (np.cos(t)**(2/a))*r/w2; y = (np.sin(t)**(2/a))*r/w2
        ax.plot(x, y, color=S.MUTED, lw=1.3)
        ax.annotate(f"α={a}", (x[len(t)//2], y[len(t)//2]), xytext=(3,3),
                    textcoords="offset points", fontsize=9.5, color=S.MUTED)
for i, c in enumerate(Z.index):
    ax.scatter(gx[i], gy[i], s=95, color=col(c), zorder=5)
    ax.annotate(c, (gx[i], gy[i]), xytext=(6,-3), textcoords="offset points", fontsize=9.5)
ax.scatter(0,0, marker="*", s=300, color=S.INK, zorder=6)
ax.annotate("ideal", (0,0), xytext=(9,4), textcoords="offset points", fontsize=10, fontweight="bold")
ax.set_xlabel("gap on PV  (ideal − design)"); ax.set_ylabel("gap on compactness")
ax.set_title("1 · Slide 31 redrawn on our designs\nequal weights — the contour SHAPE is what α changes",
             loc="left")
ax.text(.97,.06,"SHAPE only — this is a 2-criterion slice.\nThe winner is decided in 4-D: see panel 2.",
        transform=ax.transAxes, ha="right", va="bottom", fontsize=8.8, color=S.FAINT)
S.tidy(ax)

# --- 2 : the honest 4-criterion version -------------------------------------------
ax = fig.add_subplot(gs[0,1])
g   = ENG * GAP
sx, sy = g.max(axis=1).values, g.sum(axis=1).values
for i, c in enumerate(Z.index):
    ax.scatter(sx[i], sy[i], s=95, color=col(c), zorder=5)
    ax.annotate(c, (sx[i], sy[i]), xytext=(6,-3), textcoords="offset points", fontsize=9.5)
o = np.argsort(sx); front=[]
best = np.inf
for i in o:
    if sy[i] < best: front.append(i); best = sy[i]
ax.plot(sx[front], sy[front], color=S.FAINT, lw=1.1, ls="--", zorder=1)
ax.axvline(sx[list(Z.index).index("C6")],  color=S.REACHABLE, lw=1, ls=":")
ax.axhline(sy[list(Z.index).index("C14")], color=S.KEPT,      lw=1, ls=":")
ax.set_xlabel("worst weighted gap   max$_j$ w$_j$·gap$_j$      ← this is α = ∞")
ax.set_ylabel("total weighted gap   Σ w$_j$·gap$_j$\n← this is α = 1")
ax.set_title("2 · Why the winner flips — no projection, all 4 criteria\nengineering weights; lower-left is better",
             loc="left")
ax.text(0.30, 0.30, "C14 wins on the SUM  (α = 1)\nC6 wins on the WORST (α = ∞)\n"
        "α slides the ranking between\nthe two axes",
        transform=ax.transAxes, fontsize=9.4, color=S.INK, va="top")
S.tidy(ax)

# --- 3 : winner as α sweeps --------------------------------------------------------
ax = fig.add_subplot(gs[1,0])
xs = np.arange(len(AGRID))
for r,(name,w) in enumerate(PROF.items()):
    for j,a in enumerate(AGRID):
        c = L(np.array(w), a).idxmin()
        ax.add_patch(plt.Rectangle((j-.5, r-.42), 1, .84, color=col(c)))
        ax.text(j, r, c, ha="center", va="center", fontsize=8.4, color="white", fontweight="bold")
ax.set_xlim(-.5, len(AGRID)-.5); ax.set_ylim(-.7, len(PROF)-.3)
ax.set_xticks(xs); ax.set_xticklabels([("∞" if a==np.inf else f"{a:g}") for a in AGRID])
ax.set_yticks(range(len(PROF))); ax.set_yticklabels(list(PROF), fontsize=9)
ax.set_xlabel("α    (1 = weighted sum, full compensation  →  ∞ = only the worst gap counts)")
ax.set_title("3 · Whose design wins depends on α, not only on the weights\nthe case states neither",
             loc="left")
S.tidy(ax)

# --- 4 : possible winners shrinking -------------------------------------------------
ax = fig.add_subplot(gs[1,1])
W = [np.array(c)/20 for c in itertools.product(range(1,21),repeat=4) if sum(c)==20]
M = pd.DataFrame([{"alpha":a, **L(np.array(w),a).to_dict()} for a in [1,2,3,4,np.inf] for w in W])
PREFS=[("C6","C8"),("C6","C14"),("C21","C18")]
alive=M; steps=[("no statements", sorted(M[Z.index].idxmin(axis=1).unique()), len(M))]
for b,wo in PREFS:
    alive=alive[alive[b]<=alive[wo]]
    steps.append((f"{b} ≻ {wo}", sorted(alive[Z.index].idxmin(axis=1).unique()), len(alive)))
for r,(lab,pw,n) in enumerate(steps):
    for j,c in enumerate(Z.index):
        on = c in pw
        ax.add_patch(plt.Rectangle((j-.42, -r-.4), .84, .8,
                     color=col(c) if on else "#f4f4f5", ec="none"))
        if not on: ax.plot(j, -r, marker="x", ms=6, color=S.FAINT, mew=1.6)
    ax.text(len(Z.index)-.1, -r, f"{lab}   ({n} models, {len(pw)} left)",
            va="center", fontsize=9.2, color=S.INK if r else S.MUTED)
ax.set_xlim(-.7, len(Z.index)+5.6); ax.set_ylim(-len(steps)+.4, .6)
ax.set_xticks(range(len(Z.index))); ax.set_xticklabels(Z.index, fontsize=9)
ax.set_yticks([]); ax.set_xlabel("possible winners after each holistic statement")
ax.set_title("4 · What the notebook does\neach statement deletes models, and with them some designs",
             loc="left")
S.tidy(ax, spines=("top","right","left"))

fig.suptitle("Q2 · The two unknowns the case never states: the weights w, and the compensation level α",
             fontsize=14, fontweight="bold", x=.055, ha="left", y=.965)
fig.text(.055,.905,"Köksalan, Interactive Multiobjective Optimization Part I, slides 30–35, "
                   "redrawn on the ten admissible configurations", fontsize=10, color=S.MUTED)
fig.savefig(HERE/"Q2c_alpha.png", dpi=190, facecolor="white")
print("saved Q2c_alpha.png")
for name,w in PROF.items():
    print(f"  {name:26s} " + " ".join(f"{('∞' if a==np.inf else f'{a:g}')}:{L(np.array(w),a).idxmin()}" for a in [1,2,4,np.inf]))
for lab,pw,n in steps: print(f"  {lab:16s} {n:5d} models  winners {pw}")
