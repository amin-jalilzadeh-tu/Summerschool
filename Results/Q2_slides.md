# Q2 · Three stakeholders, different priorities

**Figure:** `Q2_stakeholders.png` · **Reproduce with:** `q2_stakeholders.py`
Three slides. Slide 2 carries the finding.

---

## Slide 1 · Who are the actors, and what did they actually give us?

**Source:** Cinelli, *Problem structuring* p.8–20 — internal/external stakeholders,
*"the lonely DM is a myth"*, Power–Interest matrix p.16–17 (Ferretti & Grosso 2019)

**Why:** the case names three parties with different standing. Before any arithmetic,
say who they are and what standing each has.

| actor | stated in Meeting 4 | standing |
|---|---|---|
| Client | FSI ≥ 0.80 | pays; high power, high interest |
| Municipality | PV ≥ 0.70 **and** daylight ≥ 0.70 | permits; high power, low day-to-day interest |
| Engineering team | compactness ≥ 0.75 | advises; low power, high interest |

**The line that governs the rest of the analysis:**

> The case supplies **four minimum levels and no weights.** That is the entire preference
> information in the document.

So every weight vector in Q2 is **ours** — an elicitation assumption, not data. Name it on
every slide or nothing is reproducible.

---

## Slide 2 · What survives the weighting assumption — and what does not

**Figure:** `Q2_stakeholders.png`, panels 1 and 2

**Sources:**
- Köksalan, *MCDM_Delft_Part_I.pdf* p.12–13 (the optimum moves as w changes), p.14 (the weight set)
- Rezaei, *BWM_EURO.pdf* p.10–18 — 2n−3 = **5 comparisons** for 4 criteria, with a consistency ratio

**BWM is proposed, not performed.** We have no Best-to-Others or Others-to-Worst judgements
from anyone — the weights below are our own assumption. BWM is what we would use to elicit
them properly: 2n−3 = **5** comparisons for four criteria (against AHP's 6 pairwise
judgements), with a consistency ratio to report. Both methods have consistency measures.

### The result

| actor | preferred design | stable? |
|---|---|---|
| **Client** | **C8** | ✅ invariant for FSI weight **0.40 → 0.85**, gap widening 0.004 → 0.016 |
| **Engineering** | **C14** | ⚠️ only once compactness weight clears **5/11 = 0.4545**, and only for the equal-remainder sweep; below that it is C6 |
| **Municipality** | **C21 / C1 / C6** | ❌ three winners across five plausible weightings |

```
municipality          winner   margin
  45/45/05/05           C21     0.0030
  40/40/10/10           C21     0.0010
  35/35/15/15           C1      0.0010
  30/30/20/20           C6      0.0030
  25/25/25/25           C6      0.0050
```

**Every margin is ≤ 0.005.** Each score carries up to ±0.005 from two-decimal rounding, so
a *difference* carries up to ±0.010 — every margin here is at the precision of the data.

### The sentence to say

> The client's and engineer's preferred designs are robust to how we elicit weights.
> The municipality's flips between C21, C1 and C6 on five-point weight shifts, over gaps
> smaller than the source table's own rounding.
>
> **That instability is in our elicitation model, not in the actor.** The municipality
> constrains two criteria and leaves two free, so it is exactly where the case gave us
> least to work with — while the client's single sharp constraint pins C8 regardless.

---

## Slide 3 · Aggregating across actors without a common scale

**Figure:** `Q2_stakeholders.png`, panel 3

**Sources:**
- Vetschera, *Delft_CDM.pdf* p.24–26 (welfare maximisation), **p.33 "But: What if one utility scale changes?"**
- p.31 max-min · p.32 contract imbalance · p.34 Gini · p.65–71 Nash bargaining

### The trap, and why we avoid it

**Do not average the three weight vectors.** Averaging *is* welfare maximisation, and
Vetschera p.33 shows the winner flipping under an admissible rescaling of one actor's
utility. The slide title is literally that question.

### What we do instead

| rule | result | property |
|---|---|---|
| **Nash product** (primary) | **C6** (0.29713) | invariant to positive affine rescaling per actor |
| max-min (secondary) | C11 (0.470) | **not** scale-invariant |

**Why Nash is primary:** it maximises Π(uᵢ − dᵢ), and min–max normalisation is itself a
positive affine transform per actor with dᵢ = 0 — so the argmax is unchanged by it.
Max-min's argmax is not. Verified: C6 wins under d = column-min, d = 0, and
d = the threshold configuration's value.

**Caveat to state:** Nash is invariant to *rescaling* when the disagreement point rescales
with it. It is **not** invariant to the *choice* of d — that is a separate modelling
decision (Vetschera p.67, individual rationality). Here it happens not to bite, which is a
robustness result we report rather than an assumption we skip.

### The honest footnote on max-min

`max-min = 0 for C8, C14, C18` — but that is an **artefact of min–max normalisation**:
whoever is last on a column scores 0 by construction. These are not vetoes and not
"unacceptable to someone". This is precisely Vetschera p.33's warning landing on our own
slide, so we report it rather than present the zeros as meaning.

---

## Recommendation

> Three actors, no consensus, and gaps inside the noise. We therefore report **a set with
> the weight vectors named**, not a winner:
>
> - **C6** — Nash bargaining solution; equal-weight optimum; municipality's pick under two of five weightings
> - **C11** — max-min solution; the compromise no actor ranks worst
> - **C8** — client extreme (robust)
> - **C14** — engineering extreme (robust once compactness weight > 5/11)

---

## Also considered, and why not

| method | source | why not |
|---|---|---|
| Weight-space / SMAA simulation | Köksalan p.14; Kadziński p.14 | It is Q1's simplex sweep reused — a footnote here, not a slide |
| Robust ordinal regression | Greco, *Ordinal regression revisited* | Necessary/possible relations per actor with no weights at all — the most defensible option, and the most work. Only if time allows |
| AHP per stakeholder (AIP) | Brunelli p.45 | Valid, but six pairwise comparisons per actor against BWM's five, and no better justified when the DM is invented |

## Assumptions to declare

1. All weight vectors are **ours**; the case states only minimums.
2. Actor values are min–max normalised over the ten feasible designs; d = 0.
3. Profiles used: client 10/10/10/70 · municipality 35/35/15/15 · engineering 15/15/55/15.
   **Different profiles give different numbers** — that is the finding, not a defect.
