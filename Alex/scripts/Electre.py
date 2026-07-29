from pyDecision.algorithm import electre_i, electre_ii
from scripts.HouseConfig import HouseConfig
from scripts.readdata import convert_to_numpy_array
import numpy as np

def run_electre_i(dataset:list[HouseConfig], weights:list[float], c_hat:float, d_hat:float, remove_cycles:bool=True, graph:bool=True, verbose:bool=True):
    dataset_array = convert_to_numpy_array(dataset)
    electre_results = electre_i(dataset_array, W = weights, remove_cycles = remove_cycles, c_hat = c_hat, d_hat = d_hat, graph = graph)
    
    if verbose:
        print("#"*40)
        print("Electre I Results:")
        print(f"Concordance Matrix:\n{np.ndarray.round(electre_results[0], 2)}")
        print(f"Discordance Matrix:\n{np.ndarray.round(electre_results[1], 2)}")
        print(f"Dominance Matrix:\n{np.ndarray.round(electre_results[2], 2)}")
        print(f"Kernel (Best Alternatives):")
        for i, alt in enumerate(electre_results[3]):
            idx = int(alt[1:])-1
            print(f"\t{i+1}: {dataset[idx].id}")
        print(f"Dominated Alternatives:")
        for i, alt in enumerate(electre_results[4]):
            idx = int(alt[1:])-1
            print(f"\t{i+1}: {dataset[idx].id}")
        print("#"*40)
    return electre_results

def run_electre_ii(dataset:list[HouseConfig], weights:list[float], c_minus:float, c_zero:float, c_plus:float, d_minus:float, d_plus:float, verbose:bool=True, graph:bool=False):
    dataset_array = convert_to_numpy_array(dataset)
    electre_results = electre_ii(dataset_array, W = weights, c_minus = c_minus, c_zero = c_zero, c_plus = c_plus, d_minus = d_minus, d_plus = d_plus, graph = graph)
    
    concordance, discordance, dominance_s, dominance_w, rank_D, rank_A, rank_N, rank_P = electre_results
    
    if verbose:
        print("#"*40)
        print("Electre II Results:")
        print(f"Concordance Matrix:\n{np.ndarray.round(concordance, 2)}")
        print(f"Discordance Matrix:\n{np.ndarray.round(discordance, 2)}")
        print(f"Dominance Strong Matrix:\n{np.ndarray.round(dominance_s, 2)}")
        print(f"Dominance Weak Matrix:\n{np.ndarray.round(dominance_w, 2)}")
        print(f"Rank - Decending:")
        for i in range(len(rank_D)):
            idxs = [int(a[1:])-1 for a in rank_D[i]]
            ranked_labels = [dataset[idx].id for idx in idxs]
            print(f"\tRank {i+1}: {ranked_labels}")
        
        print(f"Rank - Ascending:")
        for i in range(len(rank_A)):
            idxs = [int(a[1:])-1 for a in rank_A[i]]
            ranked_labels = [dataset[idx].id for idx in idxs]
            print(f"\tRank {i+1}: {ranked_labels}")
            
        print(f"Rank - Neutral:")
        for i, rank in enumerate(rank_N):
            idx = int(rank[1:])-1
            print(f"\tRank {i+1}: {dataset[idx].id}")
                    
        print(f"Rank - Final:\n{rank_P}")
        
        print("#"*40)
    return electre_results