import math
from pyDecision.algorithm import promethee_ii
from scripts.HouseConfig import HouseConfig
from scripts.plotting import PlottingConfig
from scripts.readdata import convert_to_numpy_array
import numpy as np
import plotly.graph_objects as go

def run_promethee_ii(dataset:list[HouseConfig], W, Q, S, P, F, sort=True, topn=10, graph=True, verbose_impl=False, verbose=True):
    dataset_array = convert_to_numpy_array(dataset)
    p2 = promethee_ii(dataset_array, W = W, Q = Q, S = S, P = P, F = F, sort = sort, topn = topn, graph = graph, verbose = verbose_impl)
    result = []
    for res in p2:
        result.append((dataset[int(res[0])-1], res[1]))
        
    if verbose:
        print("#"*40)
        print("Promethee II Results - best to worst:")
        for res in result:
            print(f"\t{res[0]} - Net Flow: {np.round(res[1], 2)}")
        print("#"*40)
    return result

def run_promethee_ii_with_in_out(dataset, W, Q, S, P, F, plottingConfig:PlottingConfig, sort = True, topn = 0, graph = False, verbose_impl = False, verbose = True):
    dataset_array = convert_to_numpy_array(dataset)
    pd_matrix  = preference_degree(dataset_array, W, Q, S, P, F)
    flow_plus  = np.sum(pd_matrix, axis = 1)/(pd_matrix.shape[0] - 1)
    flow_minus = np.sum(pd_matrix, axis = 0)/(pd_matrix.shape[0] - 1)
    flow       = flow_plus - flow_minus
    flow       = np.reshape(flow, (pd_matrix.shape[0], 1))
    flow       = np.insert(flow, 0, list(range(1, pd_matrix.shape[0]+1)), axis = 1)
    if (sort == True or graph == True):
        flow = flow[np.argsort(flow[:, 1])]
        flow = flow[::-1]
    if (topn > 0):
        if (topn > pd_matrix.shape[0]):
            topn = pd_matrix.shape[0]
        if (verbose_impl == True):
            for i in range(0, topn):
                print('a' + str(int(flow[i,0])) + ': ' + str(round(flow[i,1], 3)))
                
    result = []
    for res in flow:
        result.append((dataset[int(res[0])-1], res[1]))
        
    if verbose:
        print("#"*40)
        print("Promethee II Results - best to worst:")
        for res in result:
            print(f"\t{res[0]} - Net Flow: {np.round(res[1], 2)}")
        print("#"*40)
    
    if plottingConfig.show:
        plot_promethee_ii_in_out(flow[:,1], flow_plus, flow_minus, plottingConfig)
    
    return flow[:,1], flow_plus, flow_minus, pd_matrix

def distance_matrix(dataset, criteria = 0):
    distance_array = np.zeros(shape = (dataset.shape[0],dataset.shape[0]))
    for i in range(0, distance_array.shape[0]):
        for j in range(0, distance_array.shape[1]):
            distance_array[i,j] = dataset[i, criteria] - dataset[j, criteria] 
    return distance_array


def preference_degree(dataset, W, Q, S, P, F):
    pd_array = np.zeros(shape = (dataset.shape[0],dataset.shape[0]))
    for k in range(0, dataset.shape[1]):
        distance_array = distance_matrix(dataset, criteria = k)
        for i in range(0, distance_array.shape[0]):
            for j in range(0, distance_array.shape[1]):
                if (i != j):
                    if (F[k] == 't1'):
                        if (distance_array[i,j] <= 0):
                            distance_array[i,j]  = 0
                        else:
                            distance_array[i,j] = 1
                    if (F[k] == 't2'):
                        if (distance_array[i,j] <= Q[k]):
                            distance_array[i,j]  = 0
                        else:
                            distance_array[i,j] = 1
                    if (F[k] == 't3'):
                        if (distance_array[i,j] <= 0):
                            distance_array[i,j]  = 0
                        elif (distance_array[i,j] > 0 and distance_array[i,j] <= P[k]):
                            distance_array[i,j]  = distance_array[i,j]/P[k]
                        else:
                            distance_array[i,j] = 1
                    if (F[k] == 't4'):
                        if (distance_array[i,j] <= Q[k]):
                            distance_array[i,j]  = 0
                        elif (distance_array[i,j] > Q[k] and distance_array[i,j] <= P[k]):
                            distance_array[i,j]  = 0.5
                        else:
                            distance_array[i,j] = 1
                    if (F[k] == 't5'):
                        if (distance_array[i,j] <= Q[k]):
                            distance_array[i,j]  = 0
                        elif (distance_array[i,j] > Q[k] and distance_array[i,j] <= P[k]):
                            distance_array[i,j]  =  (distance_array[i,j] - Q[k])/(P[k] -  Q[k])
                        else:
                            distance_array[i,j] = 1
                    if (F[k] == 't6'):
                        if (distance_array[i,j] <= 0):
                            distance_array[i,j]  = 0
                        else:
                            distance_array[i,j] = 1 - math.exp(-(distance_array[i,j]**2)/(2*S[k]**2))
                    if (F[k] == 't7'):
                        if (distance_array[i,j] == 0):
                            distance_array[i,j]  = 0
                        elif (distance_array[i,j] > 0 and distance_array[i,j] <= S[k]):
                            distance_array[i,j]  =  (distance_array[i,j]/S[k])**0.5
                        elif (distance_array[i,j] > S[k] ):
                            distance_array[i,j] = 1
        pd_array = pd_array + W[k]*distance_array
    pd_array = pd_array/sum(W)
    return pd_array

def plot_promethee_ii_in_out(flow_tot, flow_plus, flow_minus, plottingConfig:PlottingConfig):
    flow_tot_ind = np.argsort(flow_tot) #get sorted indicies for plot


    fig  = go.Figure(
        go.Bar(
            x=flow_tot[flow_tot_ind], 
            y=plottingConfig.alternatives[flow_tot_ind],
            orientation ="h"))

    fig.update_layout(
        barmode="relative",
        title=dict(
            text=plottingConfig.title,
        ),
        xaxis=dict(
            title=dict(
                text=r"$\phi_{tot}$"
            )
        ),
        yaxis=dict(
            title=dict(
                text="Alternative"
            )
        ),
        legend=dict(
            title=dict(
                text=""
            )
        ),
        font=dict(
            size=18,
            color="Black"
        )
    )
    # fig.show()

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=flow_plus[flow_tot_ind],
        y=plottingConfig.alternatives[flow_tot_ind],
        name =r"$\phi^+$",
        orientation="h",
        marker = dict(
            color='#00CC96')
    ))
    fig2.add_trace(go.Bar(
        x=-flow_minus[flow_tot_ind],
        y=plottingConfig.alternatives[flow_tot_ind],
        name= r"$\phi^-$",
        orientation="h",
        marker = dict(color= '#EF553B')
    ))

    fig2.update_layout(
        barmode="relative",
        title=dict(
            text=plottingConfig.title,
        ),
        xaxis=dict(
            title=dict(
                text="Positive and negatives flows"
            )
        ),
        yaxis=dict(
            title=dict(
                text="Alternative"
            )
        ),
        font=dict(
            size=18,
            color="Black"
        )
    )
    # fig2.show()
    
    fig.write_image(f"Alex/Results/{plottingConfig.title}_total.png")
    fig2.write_image(f"Alex/Results/{plottingConfig.title}_in_out.png")