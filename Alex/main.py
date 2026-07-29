from scripts.plotting import PlottingConfig
from scripts.readdata import read_data, read_data_with_threshold
from scripts.Promethee import run_promethee_ii, run_promethee_ii_with_in_out
from scripts.BestWorstMethod import run_best_worst_method
from scripts.Electre import run_electre_i, run_electre_ii
from scripts.MAUT import run_maut_method
from scripts.WeightedSum import run_weighted_sum
from scripts.logging import Tee
import sys
import numpy as np
from datetime import datetime

CRITERIA = ['pv', 'daylight', 'compactness', 'fsi']

BEST_WORST_PROFILE = {
    'Client': {
        'mic': np.array([2, 9, 6, 1]), # best: fsi compared to all others
        'lic': np.array([7, 1, 2, 9])  # worst: all others compared to daylight
    },
    'Municipality': { 
        'mic': np.array([2, 1, 9, 4]), # best: daylight compared to all others
        'lic': np.array([7, 9, 1, 4])  # worst: all others compared to compactness
    },
    'Engineering' : {
        'mic': np.array([9, 2, 1, 7]), # best: compactness compared to all others
        'lic': np.array([1, 6, 9, 2])  # worst: all others compared to pv
    },
    'COMMON' : {
        'mic': np.array([1, 2, 2, 3]), # best: pv compared to all others
        'lic': np.array([3, 2, 2, 1])  # worst: all others compared to fsi
    } 
}
PROFILE = 'COMMON' # Change this to 'Municipality' or 'Engineering' to use different profiles

MIN_PV = 0.7
MIN_DAYLIGHT = 0.7
MIN_COMPACTNESS = 0.75
MIN_FSI = 0.8

plottingConfig = PlottingConfig(
    criteria=CRITERIA, 
    weights=BEST_WORST_PROFILE[PROFILE]['mic'], 
    title="")

# Save the original stdout
original_stdout = sys.stdout

# Open log file
# logfile = open(f"Alex/Results/{PROFILE}_PV-{MIN_PV}_daylight-{MIN_DAYLIGHT}_compactness-{MIN_COMPACTNESS}_fsi-{MIN_FSI}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log", "w")

# Redirect stdout to both terminal and file
# sys.stdout = Tee(original_stdout, logfile)



print(f"""
YOU ARE ASSUMING THE ROLE OF: {PROFILE}
    Best: {BEST_WORST_PROFILE[PROFILE]['mic']} -> {[CRITERIA[i] for i in np.argwhere(BEST_WORST_PROFILE[PROFILE]['mic'] == np.min(BEST_WORST_PROFILE[PROFILE]['mic'])).flatten()]} to all others
    Worst: {BEST_WORST_PROFILE[PROFILE]['lic']} -> all others to {[CRITERIA[i] for i in np.argwhere(BEST_WORST_PROFILE[PROFILE]['lic'] == np.min(BEST_WORST_PROFILE[PROFILE]['lic'])).flatten()]}
""")
print(f"""
THRESHOLD IS:
    MIN_PV:          {MIN_PV}
    MIN_DAYLIGHT:    {MIN_DAYLIGHT}
    MIN_COMPACTNESS: {MIN_COMPACTNESS}
    MIN_FSI:         {MIN_FSI}
      """)
##################### All data read ##########################
print("All Data:")
dataSet = read_data("data/configurations.csv")
for i, house in enumerate(dataSet):
    print(f"{i}: {house}")

##################### filtered data read ##########################
print("\nFiltered Data:")    
dataSetFiltered = read_data_with_threshold("data/configurations.csv", pv=MIN_PV, daylight=MIN_DAYLIGHT, compactness=MIN_COMPACTNESS, fsi=MIN_FSI)
for i, house in enumerate(dataSetFiltered):
    print(f"{i}: {house}")

plottingConfig.alternatives = np.array([house.id for house in dataSetFiltered], dtype=str)

##################### best worst method ##########################
print("\nBest-Worst Method Weights:")
# Taking the role of a Client
mic = BEST_WORST_PROFILE[PROFILE]['mic']
lic = BEST_WORST_PROFILE[PROFILE]['lic']
plottingConfig.title = f"Best-Worst Method Weights ({PROFILE})"
WEIGHTS = run_best_worst_method(CRITERIA, mic, lic, plottingConfig=plottingConfig, eps_penalty = 1, verbose_impl = True, verbose = True)

##################### Weighted Sum ##########################
weighted_sum_results = run_weighted_sum(dataSetFiltered, WEIGHTS, verbose=True)

##################### MAUT ##########################
criteria_direction = ['max', 'max', 'max', 'max'] # All criteria are to be maximized
utility_function = ['linear', 'linear', 'linear', 'linear'] # All criteria use linear utility functions
maut_results = run_maut_method(dataSetFiltered, WEIGHTS, criteria_direction, utility_function, verbose=True)

##################### Promethee II ##########################
Q = [ 0.03,  0.03,  0.03,  0.03] # indifference thresholds for each criterion
S = [ 0,  0,  0,  0] # Gaussian thresholds for each criterion (only used for 't6' preference function)
P = [ 0.2,  0.2,  0.2,  0.2] # preference thresholds for each criterion to deem one alternative as preferred over another
W = WEIGHTS # weights for each criterion
F = ['t5', 't5', 't5', 't5'] # 't1' = Usual; 't2' = U-Shape; 't3' = V-Shape; 't4' = Level; 't5' = V-Shape with Indifference; 't6' = Gaussian; 't7' = C-Form    
# promethee_results = run_promethee_ii(dataSetFiltered, W, Q, S, P, F, verbose=True)

plottingConfig.title = f"Promethee II - Flows ({PROFILE})"
promethee_results_with_in_out = run_promethee_ii_with_in_out(dataSetFiltered, W, Q, S, P, F, plottingConfig=plottingConfig, sort=True, topn=0, graph=False, verbose_impl=False, verbose=True)
    
##################### Electre I ##########################
c_hat = 0.65 # concordance threshold
d_hat = 0.35 # discordance threshold
electre_i_results = run_electre_i(dataSetFiltered, WEIGHTS, c_hat, d_hat, remove_cycles=True, graph=False, verbose=True)


##################### Electre II ##########################
c_minus = 0.65
c_zero  = 0.75
c_plus  = 0.85

d_minus = 0.25
d_plus  = 0.50
electre_ii_results = run_electre_ii(dataSetFiltered, WEIGHTS, c_minus, c_zero, c_plus, d_minus, d_plus, verbose=True)
