import numpy as np

COLORS = {
    'pv': 'gold',
    'daylight': 'orange',
    'compactness': 'forestgreen',
    'fsi': 'royalblue'
}

class PlottingConfig:
    def __init__(self, criteria: np.ndarray, weights:list[float], title:str):
        # ensure criteria is a numpy array of strings
        self.show = True
        self.criteria = np.array(criteria, dtype=str)
        self.alternatives = np.array([], dtype=str)
        self.labels = {'x':'Criteria', 'y':'Weight'}
        self.weights = weights
        self.colors = [COLORS[c] for c in self.criteria]
        self.title = title
        