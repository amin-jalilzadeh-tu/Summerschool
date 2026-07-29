from pyDecision.algorithm import maut_method
from scripts.HouseConfig import HouseConfig
from scripts.readdata import convert_to_numpy_array
import numpy as np

def run_maut_method(dataset:list[HouseConfig], weights:list[float], criteria:list[str], utility_function:list[str], verbose_impl=False, verbose=True):
    assert len(criteria) == len(weights) == len(utility_function), "Inconsistent dimensions between criteria, weights, and utility functions"
    dataset_array = convert_to_numpy_array(dataset)
    maut_results = maut_method(dataset_array, weights, criteria, utility_function, verbose=verbose_impl)
    
    result = []
    for res in maut_results:
        result.append((dataset[int(res[0])-1], res[1]))
        
    if verbose:
        print("#"*40)
        print("MAUT Results - best to worst:")
        for res in result:
            print(f"\t{res[0]} - Score: {np.round(res[1], 2)}")
        print("#"*40)
    
    return result