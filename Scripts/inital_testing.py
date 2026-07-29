# Required Libraries
import numpy as np
import pandas as pd
from pyDecision.algorithm import bw_method, promethee_i, promethee_ii



class Configuration:
    def __init__(self, row):
        self.id = None
        self.pv = None
        self.daylight = None
        self.compactness = None
        self.fsi = None
        for key, value in row.items():
            setattr(self, key, value)
            if key == 'id':
              self.id = value
            if key == 'pv':
              self.pv = value
            if key == 'daylight':
              self.daylight = value
            if key == 'compactness':
              self.compactness = value
            if key == 'fsi':
              self.fsi = value

criteria = ['pv', 'daylight', 'compactness', 'fsi']
# pv, daylight, compactness, fsi - Client
mic = np.array([2, 9, 6, 1]) # best: fsi compared to all others
lic = np.array([7, 1, 1, 9]) # worst: all others compared to daylight

# Call BWM Function
weights = bw_method(mic, lic, eps_penalty = 1, verbose = True)

# Weigths
for i in range(0, weights.shape[0]):
  print('w(' + criteria[i] + '): ' + str(round(weights[i], 8)))



# Read CSV file
configurations_df = pd.read_csv('data/configurations.csv')

# Filter rows where pv is greater than 0.7
configurations_df = configurations_df[(configurations_df['pv'] > 0.7) & (configurations_df['daylight'] > 0.7) & (configurations_df['compactness'] > 0.75) & (configurations_df['fsi'] > 0.8)]

print(configurations_df.head())

# Convert selected columns to a NumPy 2D array
configurations = configurations_df[['pv', 'daylight', 'compactness', 'fsi']].to_numpy()

print(configurations)

Q = [0.05, 0.05, 0.05, 0.05]          # Indifference thresholds for each criterion
S = [0.4, 0.4, 0.4, 0.4]  # S parameters used by the preference function for each criterion
P = [0.05, 0.05, 0.05, 0.05]  # Preference thresholds for each criterion
W = weights               # Criterion weights from the BWM method
F = ['t5', 't5', 't5', 't5']  # Preference function type per criterion ('t5' = V-Shape with Indifference)


p1 = promethee_i(configurations, W = W, Q = Q, S = S, P = P, F = F, graph = False)

print("Promethee I Results:")
print(p1)


def sort_options_from_preference_matrix(preference_matrix, option_labels=None):
  matrix = np.asarray(preference_matrix)
  n = matrix.shape[0]

  if option_labels is None:
    option_labels = list(configurations_df["id"]) if "id" in configurations_df.columns else [f"Option {i + 1}" for i in range(n)]

  ranking = []
  for i in range(n):
    wins = np.sum(matrix[i] == 'P+')
    losses = np.sum(matrix[i] == 'R')
    score = int(wins - losses)
    ranking.append((option_labels[i], score, wins, losses))

  ranking.sort(key=lambda x: (x[1], x[2]), reverse=True)
  return ranking


print("\nSorted options (best to worst):")
ranking = sort_options_from_preference_matrix(p1)
for rank, (label, score, wins, losses) in enumerate(ranking, start=1):
  print(f"{rank}. {label} | score={score} | P+={wins} | R={losses}")

