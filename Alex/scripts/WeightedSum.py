from scripts.HouseConfig import HouseConfig
from scripts.readdata import convert_to_numpy_array
import numpy as np

def run_weighted_sum(dataset:list[HouseConfig], weights:list[float], verbose:bool=True):
    dataset_array = convert_to_numpy_array(dataset)
    scores = [np.dot(dataset_array[i], weights) for i in range(len(dataset_array))]
    
    if verbose:
        ranked_results = sorted(zip(dataset, scores), key=lambda item: item[1], reverse=True)
        print("#"*40)
        print("Weighted Sum Results - best to worst:")
        for house, res in ranked_results:
            print(f"\t{house} - Weighted Sum: {np.round(res, 2)}")
        print("#"*40)
    return scores
