from pyDecision.algorithm import bw_method
import plotly.express as px
from scripts.plotting import COLORS, PlottingConfig
import numpy as np

def run_best_worst_method(criteria:list[str], mic:list[int], lic:list[int], plottingConfig: PlottingConfig, eps_penalty=1, verbose_impl=True, verbose=True):
    assert len(criteria) == len(mic) == len(lic), "Inconsistent dimensions between criteria and prefrence vectors"
    weights = bw_method(mic, lic, eps_penalty=eps_penalty, verbose=verbose_impl)
    if verbose:   
        print("#"*40)         
        print(f"Best-Worst Method Weights: Results")
        label_width = max(len(c) for c in criteria)
        for i, weight in enumerate(weights):
            print(f"\t{criteria[i]:<{label_width}}: {np.round(weight, 2)}")
        print("#"*40)
        
    if plottingConfig.show:
        assert all(c in COLORS for c in criteria), "Some criteria do not have a defined color in the COLORS dictionary."
        
        fig = px.bar(
            x=criteria, 
            y=weights, 
            labels=plottingConfig.labels, 
            title=plottingConfig.title,
            color=criteria,
            color_discrete_map=COLORS
        )
        # fig.show()
        fig.write_image(f"Alex/Results/{plottingConfig.title}.png")
    return weights