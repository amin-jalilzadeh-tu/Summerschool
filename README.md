# Summer School Case Study 2 - Solar-Efficient Building Design

MCDA analysis for the 2026 EURO PhD Summer School case study. We pick among 30 candidate
building designs scored on 4 criteria (PV, daylight, compactness, FSI).

## Layout
- `data/` - input CSVs 
- `notebooks/` - one notebook per question


## Run

Python 3.9+ (tested on 3.13). Then:
```
pip install -r requirements.txt
pip install jupyterlab
jupyter lab notebooks/Q1.ipynb
```

If Q1's coloured table cell errors with `ImportError: ... jinja2`, run
`pip install jinja2` (it is in requirements.txt). Still stuck? Pin the exact
tested versions listed at the bottom of requirements.txt.

### Gurobi (only needed for scripts that use it)

Some scripts use the Gurobi optimiser:
```
pip install gurobipy
```
The free restricted licence that ships with `gurobipy` already solves small
models, which is all this project needs - no activation required.

For unlimited use, get a free academic licence at
https://www.gurobi.com/academia/ and activate it once with
`grbgetkey <your-key>` (this needs the full Gurobi tools installed, not just
`pip install gurobipy`). Do not commit your licence key.
