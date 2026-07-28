"""Shared visual language for the four case-study figures.

Two rules, both learned from review:

1. **One colour per configuration, everywhere.** C6, C8, C11, C14 and C15 recur across all
   four figures. If C15 is the same colour every time, the audience follows the story
   without re-reading a legend each slide.

2. **A zero must be visible.** The punchline of five panels is a zero — a design that wins
   0 % of the weight space, a requirement that eliminates nothing, a design at exactly zero
   slack. Drawn as a bar, a zero is blank space, and the eye goes to the tallest bar
   instead, which is never the point. `mark_zero` draws an explicit "none" marker so
   absence reads as deliberate rather than as missing data.

Supported / unsupported is drawn in blue and amber, not green and red: an unsupported
design is not worse, it is unreachable by one family of methods, and three of them are
perfectly good buildings.
"""

import matplotlib.pyplot as plt

# --- semantic colours -------------------------------------------------------------
INK = "#18181b"
MUTED = "#52525b"
FAINT = "#a1a1aa"
RULE = "#e4e4e7"

REACHABLE = "#2563eb"      # supported: some positive weight vector selects it
UNREACHABLE = "#d97706"    # unsupported: none does — not "bad", just out of reach
ELIMINATED = "#dc2626"     # fails a requirement, or an empty set
KEPT = "#059669"           # survives / does work

#: One colour per configuration, fixed across every figure in the deck.
CONFIG = {
    "C1": "#eb6834",
    "C6": "#2563eb",
    "C8": "#dc2626",
    "C11": "#0891b2",
    "C14": "#059669",
    "C15": "#d97706",
    "C18": "#65a30d",
    "C21": "#7c3aed",
    "C25": "#db2777",
    "C28": "#0d9488",
}


def colour_for(config_id, default=FAINT):
    """The fixed colour of a configuration, so the story survives across slides."""
    return CONFIG.get(config_id, default)


def mark_zero(ax, x, y=0.0, *, label="none", colour=ELIMINATED, size=9, fontsize=8.5,
              orientation="vertical"):
    """Draw an explicit marker where a value is exactly zero.

    A zero-height bar is indistinguishable from missing data. An open circle with the word
    "none" beside it reads as a measured zero, which is what these zeros are.
    """
    ax.plot([x], [y], marker="o", ms=size, mfc="white", mec=colour, mew=1.8,
            zorder=6, clip_on=False)
    if label:
        if orientation == "vertical":
            ax.annotate(label, (x, y), textcoords="offset points", xytext=(0, 11),
                        ha="center", fontsize=fontsize, color=colour, fontweight="bold")
        else:
            ax.annotate(label, (x, y), textcoords="offset points", xytext=(11, 0),
                        va="center", fontsize=fontsize, color=colour, fontweight="bold")


def tidy(ax, *, spines=("top", "right"), labelsize=9):
    for s in spines:
        ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=labelsize)


#: Projected in a lecture hall, 8 pt becomes unreadable. These are floors, not suggestions.
TITLE = 12
LABEL = 10.5
BODY = 10
SMALL = 9.5


def apply_defaults():
    plt.rcParams.update({
        "font.size": BODY,
        "axes.titlesize": TITLE,
        "axes.labelsize": LABEL,
        "xtick.labelsize": SMALL,
        "ytick.labelsize": SMALL,
        "legend.fontsize": SMALL,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
    })
