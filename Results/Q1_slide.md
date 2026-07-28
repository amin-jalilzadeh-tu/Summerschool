# Q1 · Analysing the feasible design space

**Figure:** `Q1_design_space.png` · **Reproduce with:** `q1_design_space.py`

---

## The slide

### Title
**Which designs are even recommendable — before anyone argues about weights**

### Figure
`Q1_design_space.png` (three panels, left to right)

### The three findings, one per panel

**1 · Dominance decides nothing. The minimums decide a lot.**
All 30 configurations are mutually non-dominated — 0 dominated pairs out of 870 ordered
comparisons. The four stakeholder minimums cut 30 → **10**:
`C1 C6 C8 C11 C14 C15 C18 C21 C25 C28`. Those 10 are *also* mutually non-dominated.

**2 · Three of the ten are unreachable by any weighted sum.**
**C15, C25 and C28 are unsupported *within this ten-design set***: no positive weight
vector makes any of them a weighted-sum winner **there**. Supportedness is a property of an
alternative *relative to a set* — see Q3, where removing C8 makes C15 supported. Proved by linear programming, one LP per configuration.
500 000 random weight vectors confirm it — those three win **zero** times, while the
knife-edge C11 wins **158** times (0.032 %).

> A positive linear weighted sum cannot select 3 of the 10 admissible designs.
> (The ASF below is itself a scalarising method, and it can.)

**3 · A reference point reaches what no weight can.**
With the reference point set at C15's own performance, the Wierzbicki achievement
scalarising function selects **C15 outright**. Same data, same 10 alternatives — the
answer changed because the *family of scalarisation* changed, not because a weight did.

### The sentence to say out loud
> *Which designs are recommendable at all depends on the scalarisation family, before any
> weight is discussed.*

### Recommendation — a set, not a winner
Score gaps among the ten are **0.001–0.012**, on a table published to two decimals. That is
inside the rounding, so a single "winner" is not defensible.

| | design | role |
|---|---|---|
| compromise | **C6, C11** | best under equal weights (0.8175, 0.8125); C6 also wins L₁ and L₂ to the ideal, and ties C11 at L∞ |
| client extreme | **C8** | wins the largest share of the weight simplex (38.3 %) |
| engineering extreme | **C14** | second largest (30.2 %) |

---

## Methods used, and why

| # | Method | Source | Why this method | What it needs |
|---|---|---|---|---|
| 1 | **Pareto dominance** | Köksalan, *MCDM_Delft_Part_I.pdf* p.5–6; Słowiński, *MCDA_School_2026_DRSA_Rules* p.3 | The only preference-free comparison. Establishes that the space is fully conflicting, which is *why* preference information is needed at all | nothing |
| 2 | **Conjunctive screen** — thresholds as ε-constraints and as vetoes | Köksalan Part I p.15–16 (ε-constraint); Figueira, *Electre_Part_I* p.17 and *Part_II* p.8 (veto) | Meeting 4 states *minimum performances*, and Laura's rule is that failing one is disqualifying. That is non-compensatory — a weighted sum structurally cannot express it | the four stated minimums (given) |
| 3 | **Supported / unsupported classification** (LP) | Köksalan Part I p.7 (solution types), p.12–13 (weighted sums on discrete alternatives) | Answers a question no scoring method can: *is this design reachable at all?* Needs no elicited preferences | nothing |
| 4 | **Uniform weight-space sampling** (first-rank acceptability) | Köksalan Part I p.14 (weight set); Kadziński, *mcdamss-delft* p.14 (stochastic acceptabilities) | Turns "which weights favour which design" into a distribution. **Not full SMAA** — no uncertain performances, no complete rank acceptabilities | nothing — it sweeps all weights |
| 5 | **Achievement scalarising function** (Wierzbicki 1980) | Köksalan, *MCDM-Delft_Part_II.pdf* p.28–31 | The only method here that can reach unsupported points. Demonstrates the reachability gap rather than asserting it | a reference point |

### Why *not* the alternatives we rejected

- **Weighted sum alone** — fully compensatory; a strong PV score would buy its way past a
  failed compactness minimum, which Meeting 4 forbids. It also cannot reach C15/C25/C28.
- **ELECTRE Tri-nB** — the more correct *problematique* (absolute evaluation against
  reference profiles, Figueira *Electre_Part_I* p.34), but it needs weights, indifference,
  preference and veto thresholds and λ — eleven-plus parameters nobody in the case supplied.
- **DRSA** — degenerates here: the class labels would come from the thresholds themselves,
  so the approximation is exact by construction and the rules restate the screen.

---

## Assumptions to state on the slide

1. **Appendix C's normalisation is not published.** The 0.70 cutoffs are numbers on an
   undisclosed scale. Everything here is conditional on the table as given.
2. **Equal weights** wherever weights appear, used only as a reference point — never as a
   claim about anyone's preferences.
3. The ASF uses ρ = 1e-6 as the augmentation term; it only breaks exact ties.

## The honest caveats

- At the reference point q = (0.70, 0.70, 0.75, 0.80) the ASF **ties C6, C1 and C21** at
  0.20 — it does not discriminate there either. Reporting that is stronger than hiding it.
- **Sampling cannot prove unsupportedness.** A zero share means "not found in 500 000
  draws", not "impossible" — C11's 158 wins (seed 20260728) show how a tiny region behaves.
  The LP is the proof; the sampling corroborates.
- **Setting q = y(C15) is constructed to demonstrate reachability.** It shows the ASF *can*
  reach C15; it is not evidence that C15 is the right building.
- The compactness minimum (≥ 0.75) is **inert**: relaxing it to 0.65 leaves the feasible
  set unchanged at 10. The engineering team's requirement did no work.
