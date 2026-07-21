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
