# Q3 · Tightening and relaxing the stakeholder requirements

**Figure:** `Q3_thresholds.png` · **Reproduce with:** `q3_thresholds.py`
Three slides. Slide 3 closes the loop back to Q1.

---

## The citation to say out loud

**Köksalan, *MCDM-Delft_Part_II.pdf* p.11:**

> *"Changing εᵢ values systematically, we can find many (sometimes all) efficient
> solutions… we can explore different (desirable) parts of the efficient frontier."*

Q3 **is** parametric ε-constraint analysis. The four stakeholder minimums are the εᵢ
right-hand sides, so the lecture's own method matches the question exactly — not by
analogy.

---

## Slide 1 · How much room is there?

**Figure:** panel 1 · **Source:** Köksalan Part I p.15–16, Part II p.9–11

Shift all four minimums together:

| shift | feasible | | shift | feasible |
|---|---|---|---|---|
| −0.05 | 17 | | +0.01 | 8 |
| −0.03 | 15 | | +0.03 | 6 |
| −0.01 | 11 | | +0.05 | **3** — C1, C6, C21 |
| **0** | **10** | | **+0.06** | **0** |

### The headline

> **The requirements as agreed sit six hundredths from infeasibility.**
> On a table published to two decimals, that is six rounding units of headroom.

Relaxing is far less dramatic: −0.05 admits 17, so the constraint set is much tighter on
the upside than the downside. There is no room to negotiate up, and considerable room to
negotiate down.

### One-at-a-time slack, before the feasible set empties

| requirement | slack | binding alternative |
|---|---|---|
| PV ≥ 0.70 | **+0.13** (to 0.83) | C8 |
| **Daylight ≥ 0.70** | **+0.10** (to 0.80) | C14 |
| Compactness ≥ 0.75 | +0.15 (to 0.90) | C14 |
| FSI ≥ 0.80 | **+0.14** (to 0.94) | C8 |

**Daylight is the tightest lever.** Note that PV and FSI are both limited by the same
alternative, C8 = (0.83, 0.70, 0.76, 0.94).

---

## Slide 2 · Not all four requirements are real

**Figure:** panel 2

The count of designs failing each criterion *in isolation* is misleading, because the
failures overlap. The question is what each requirement removes **that the others do not**:

| requirement | set by | uniquely eliminates | feasible if dropped |
|---|---|---|---|
| PV ≥ 0.70 | municipality | 1 — C4 | 11 |
| Daylight ≥ 0.70 | municipality | 1 — C27 | 11 |
| **Compactness ≥ 0.75** | **engineering** | **0 — nothing** | **10, unchanged** |
| FSI ≥ 0.80 | client | 1 — C2 | 11 |

### The finding

> **The engineering team's requirement does no work.** Delete it from Meeting 4 entirely
> and the feasible set is the same ten designs. Every configuration that fails compactness
> already fails something else.

And it is not a coincidence of where the threshold sits — compactness stays non-binding at
**every** tightening level from +0.00 to +0.05:

```
        with RC   without RC          with RC   without RC
+0.00      10        10        +0.03      6         6
+0.01       8         8        +0.04      5         5
+0.02       7         7        +0.05      3         3
```

The other three are load-bearing — but **by exactly one configuration each**. Three
requirements, three single points of failure.

**Why this matters for Studio Delta:** a negotiated requirement that changes nothing is
worth knowing about. That effort could have gone somewhere that moves the outcome.

---

## Slide 3 · One hundredth decides the client's building

**Figure:** panel 3

Two designs survive only at **exact equality**: C8 at daylight = 0.70, C14 at PV = 0.70.
They are also the client's and the engineer's preferred designs from Q2.

| scenario | feasible | client picks | unsupported in that set |
|---|---|---|---|
| as agreed | 10 | **C8** | C15, C25, C28 |
| daylight 0.70 → **0.71** | 9 | **C15** | C28 only |

### The sentence

> Raising the municipality's daylight floor by one hundredth removes C8 — the client's
> preferred design. But it does more than change the winner: **it changes the geometry of
> the feasible set.**
>
> C15 is unsupported among the baseline ten, meaning no positive weighted sum selects it
> *there*. With C8 gone, C15 becomes **supported**, and the client's own weighted sum then
> selects it.

**Supportedness is a property of an alternative WITHIN A SET, not a fixed label.** Moving a
threshold rewrites which designs a weighted-sum method can reach at all — which is a
stronger Q3 → Q1 link than "the client cannot reach its own design", and unlike that
claim, it is true.

### The mirror image

The engineering team's own requirement changes nothing, while the municipality's daylight
floor silently decides whether the client gets C8 or C15. **Influence in this decision is
not where the stakeholders think it is.**

---

## The alternative model, for critical discussion

**Thresholds as vetoes rather than hard constraints** — Figueira, *Electre_Part_I* p.17–19.

Under a veto reading, a design at daylight 0.69 is not *deleted*; it is *blocked from
outranking* on that criterion. Softer, and it shows what the hard-constraint reading throws
away.

**The knife-edge table is the argument for it:** at daylight 0.71, C8 is not a bad design —
it misses by one hundredth on a measure whose normalisation the case never published.

**Cost, to state honestly:** ELECTRE needs weights, concordance and veto thresholds nobody
supplied. Use it as critical discussion, not as a second computed answer.

---

## A methodological note worth one line

All threshold comparisons here are done in **exact integer hundredths**, not floating point.

In binary floating point `0.80 + 0.14 = 0.9400000000000001`, so C8's FSI of exactly 0.94
fails its own limit by 1e-16 and the reported slack comes out one step short. With two
designs sitting at exact equality, that artefact directly attacks the knife-edge analysis —
so the arithmetic is kept exact.

*(This is a real bug we hit and fixed, not a hypothetical.)*

---

## Assumptions

1. Appendix C is taken as given, to two decimals: ±0.005 per score, so ±0.010 on a
   difference between two scores.
2. Stakeholder weight profiles for the "who prefers what" columns are the Q2 ones:
   client 10/10/10/70 · municipality 35/35/15/15 · engineering 15/15/55/15.
3. Requirements are read as hard constraints, per Meeting 4: *"Any configuration failing to
   satisfy one or more stakeholder requirements cannot be recommended."* The veto reading
   is offered as an alternative, not a substitute.
