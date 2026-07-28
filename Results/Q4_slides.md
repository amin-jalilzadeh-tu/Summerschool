# Q4 · Recommendations for Studio Delta, and reuse in future projects

**Figure:** `Q4_criteria_audit.png` · **Reproduce with:** `q4_criteria_audit.py`
Three slides. The reusable deliverable is a **method-selection protocol**, not a spreadsheet.

---

## Slide 1 · Defending the method choice, and the problematique change

### (i) Say the sentence almost nobody writes

**Source:** Kadziński, *mcdamss-delft-kadzinski-milosz.pdf* p.5–15 — MCDA-MSS, 156
characteristics across four sections (problem typology / preference model / elicitation /
exploitation); p.18 rule-based recommendation.

Run the case through MCDA-MSS, screenshot it, and produce:

> **"We used X because our problem has features a, b, c."**

Most teams assume a method. Deriving it from problem features is the thing the lecture
exists for, and it is checkable.

### (ii) This project and the next one are different problematiques

**Source:** Kadziński p.6

| | problematique | why |
|---|---|---|
| **This project** | **choice (α)** | pick one or more of 30 given configurations |
| **Future projects** | **sorting (β)** | *is this massing acceptable, marginal, or unacceptable?* |

**The reason this matters:** sorting is **absolute evaluation** — each design is compared to
fixed profiles, not to the other candidates. So it is **rank-reversal immune**. Next year's
configurations cannot reshuffle this year's verdicts, which is exactly the property a firm
accumulating designs across projects needs.

| for the reusable version | source | why |
|---|---|---|
| **ELECTRE Tri-nB** | Figueira, *Electre_Tri_nB_Delft* p.13–17 (assignment procedures), p.23–25 (numerical example) | several distinct borderline archetypes; the assignment interval *is* honest uncertainty |
| **DRSA** | Słowiński, *MCDA_School_2026_DRSA_Rules* p.30, 49–50 | **no weights at all.** Studio Delta accumulates accepted/rejected designs → induce `if compactness ≥ 0.80 then acceptable`. Directly readable by architects |
| Interactive sorting | Köksalan Part I p.48–54 (Köksalan & Ulu, EJOR 2003) | the value-function analogue, if an additive model is preferred |

---

## Slide 2 · The criteria family does not pass its own audit

**Figure:** panels 1 and 2 · **Source:** Cinelli p.42–43 (completeness / non-redundancy /
preferential independence / conciseness), p.83–85 (correlations between criteria, Lindén
et al. 2021)

### Finding 1 — the criteria are empirically near-collinear

Every one of the six pairs is |r| ≥ 0.807:

```
r(PV, daylight)  −0.979      r(PV, compactness)   −0.850
r(PV, FSI)       +0.975      r(daylight, compact) +0.827
r(daylight, FSI) −0.947      r(compact, FSI)      −0.807
```

**PC1 = 92.4 % of the variance.** Four criteria, one dominant dimension — and it does **not**
go away on the designs we actually recommend from: **90.5 % on the feasible ten**, where
three of the six correlations *strengthen* (PV~compactness → −0.935, daylight~FSI → −0.964).

### Finding 2 — exhaustiveness fails, and the case convicts itself

> p.2 — *"it may cast **larger shadows on neighbouring buildings** and public spaces or
> reduce the amount of sunlight available to the surrounding community"*
>
> p.4, Laura — *"how our design influences access to sunlight and daylight, **both for the
> new building and for the surrounding properties**"*

Then Appendix B measures roof PV **of this building**, façade daylight **in this building**,
compactness **of this building**, FSI **of this building**.

**Not one criterion looks outside the plot.** Two designs can tie on all four and differ
completely in what they do to the neighbours.

> The four criteria are all things the voxel optimiser could compute. The one the brief
> names twice is the one it could not — and it is missing.

---

## Slide 3 · The correlation structure did not reproduce on real geometry

**Figure:** panel 2

We reimplemented Appendix B's four formulas and ran them on **real Rotterdam geometry
(3DBAG) and real weather (PVGIS TMY)**:

| space | n | PC1 | r(PV, daylight) | r(PV, FSI) |
|---|---|---|---|---|
| **Appendix C** | 30 | **0.924** | **−0.979** | **+0.975** |
| rotterdam_blaak | 30 | 0.513 | +0.368 | +0.680 |
| zoetermeer_edge | 30 | 0.511 | +0.025 | +0.556 |
| area_bec57e | 40 | 0.486 | −0.041 | +0.611 |
| area_5de245 | 30 | 0.503 | −0.027 | +0.553 |

Same formulas. PC1 roughly **halves**, and no pair exceeds 0.68.

### The precise claim — the two couplings are not equally artificial

| coupling | Appendix C | our four runs | reading |
|---|---|---|---|
| PV ~ FSI | +0.975 | +0.55 → +0.68 | **persists, far weaker** — denser massing does tend to raise both |
| PV ~ daylight | **−0.979** | **−0.04 → +0.37** | **not reproduced** — the near-perfect trade-off did not appear in any run |

> The near-perfect PV–daylight relationship in Appendix C was not reproduced in four
> exploratory generated spaces. It appears **specific to the supplied design sample** rather
> than a general property of the four measures.

**State the limit of this evidence.** The four generated spaces share one generator, one set
of massing families, one normalisation approach — they are replications under a single
modelling pipeline, not independent validation. And Appendix C's own normalisation is
undisclosed, so the comparison is suggestive, not conclusive.

---

## The three findings, and why they are not all the same kind

| object | defect | evidence |
|---|---|---|
| **Criteria family** (Cinelli p.42–43) | empirical near-collinearity — a *flag*, not a verdict | all six \|r\| ≥ 0.807; PC1 = 92.4 % |
| **Criteria family** | exhaustiveness fails | neighbour shadowing named on pp.2 and 4, measured by nothing |
| **Requirement set** (Meeting 4) | one requirement non-binding | drop compactness ≥ 0.75 → same 10 designs, at every tightening level |

**Keep these apart.** The compactness *threshold* (≥ 0.75) never binds — that is a property
of the negotiated requirement set. The compactness *criterion* discriminates strongly
(range 0.63–0.96 across the 30; it is what makes C14 the engineering winner and carries
~30 % of the weight simplex). Filing a non-binding threshold under Cinelli's
conciseness test would be a category error in front of Cinelli.

**Two Roy/Cinelli axioms, plus one negotiation finding.**

---

## What we recommend Studio Delta change

**Source for the fix:** Cinelli p.86–91 — and it is an architecture case
(Matassino 2024, Leiden Orangery): stakeholder interviews → fundamental & means objectives
→ features → design alternatives.

> Derive the criteria from **stakeholder objectives**, not from whatever the voxel optimiser
> happens to compute.

---

## Three traps we deliberately avoided

| trap | why |
|---|---|
| **Running five methods and comparing rankings** | precisely the error Cinelli and Kadziński spend their lectures diagnosing. One justified choice, plus robustness within it |
| **Transplanting BWM weights into ELECTRE** | Figueira, *Electre_Part_II* p.4: *"The compensatory effects are not pertinent. This is due to the fact that **the weights cannot be interpreted as substitution rates**."* BWM/AHP weights are trade-offs; ELECTRE weights are voting power. If outranking, elicit separately with SRF / deck-of-cards |
| **Declaring a winner to three decimals** | the municipality profile separates C1 from C21 by **0.001**, on a table published to two decimals |

---

## Closing paragraph for the final slide

> The four criteria were all things the voxel optimiser could compute. The criterion the
> brief names twice — effect on the neighbours — is the one it could not, and it is missing.
> Meanwhile the four it did compute collapse onto one axis (PC1 = 92.4 %) — and that
> collapse did not reproduce when we recomputed the same formulas on real Rotterdam
> geometry and weather: PC1 ≈ 0.51, and no trace of the PV/daylight antagonism. Evidence
> that the structure is specific to the supplied sample, not to the measures. And one of
> the four negotiated requirements never bound. For the next
> project we would derive criteria from stakeholder objectives rather than from what the
> optimiser emits, and treat the recurring question as **sorting** rather than **choice**.
