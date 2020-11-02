#!/usr/local/bin/python3.8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import edhec_risk as erk
import scipy.stats
import scipy
from scipy.optimize import minimize

##ind = pd.read_csv("ind30_m_vw_rets.csv", header=0, index_col=0)/100
##ind.index = pd.to_datetime(ind.index, format="%Y%m").to_period('M')
##ind.columns = ind.columns.str.strip()

ind = erk.get_ind_returns()
erk.var_gaussian(ind[["Food", "Smoke", "Coal", "Beer", "Fin"]], modified=True)
erk.var_gaussian(ind, modified=True).sort_values().plot.bar()
##plt.show()

ind_sh = erk.share_ratio(ind, 0.03, 12).sort_values()
##ind_sh.plot.bar()
#plt.show()

er = erk.annualize_rets(ind["1996":"2000"], 12)
##er.sort_values().plot.bar()
##plt.show()

## Efficient frontier Part II

cov = ind["1995":"2000"].cov()


def portfolio_return(weights, returns):
    """
    Weights to return 
    """
    return weights.T @ returns
def portfolio_vol(weights, covmat):
    """
    Weighhts to Vol
    """
    return (weights.T @ covmat @ weights)**0.5


def minimize_vol(target_return, er, cov):
    """
    target retunr to weight vector
    """
    n = er.shape[0]
    init_guess =  np.repeat(1/n, n)
    bounds = ((0.0, 1.0),)*n
    return_is_target = {
        'type': 'eq',
        'args': (er,),
        'fun': lambda weights, er:target_return - erk.portfolio_return(weights, er) 
    }
    weights_sum_to_1 = {
        'type': 'eq',
        'fun': lambda weights: np.sum(weights)-1
    }
    results = minimize(erk.portfolio_vol, init_guess, 
                args=(cov,), method="SLSQP", 
                constraints=(return_is_target, weights_sum_to_1),
                bounds=bounds
                )
    return(results.x)

def optimal_weights(n_points, er, cov):
    """
    list of weights to run the optimizer on to minimize the vol 
    """
    target_rs = np.linspace(er.min(), er.max(), n_points)
    weighs = [minimize_vol(target_return, we, cov) for target_returns in target_rs]
    return weights

def plot_ef(n_points, er, cov):
    weights = optimal_weights(n_points, er, cov)
    rets = [portfolio_return(w, er) for w in weights]
    vols = [portfolio_vol(w, cov) for w in weights]
    ef = pd.DataFrame({"Returns": rets, "Volality": vols})
    return ef.plot.line(x="Vol", y="returns")

l = ['Food', "Beer", "Smoke", 'Coal']

##weights = np.repeat(1/4, 4)
##print(erk.portfolio_return(weights, er[l]))

## print(erk.portfolio_vol(weights, cov.loc[l, l]))

## 2 Asset fromtier

l =["Games", "Fin"]
n_points = 20 
## below weights is onky for 2 assets 
## weights = [np.array([w, 1-w]) for w in np.linspace(0, 1, n_points)]
##rets = [erk.portfolio_return(w, er[l]) for w in weights]
##vols = [erk.portfolio_vol(w, cov.loc[l, l]) for w in weights]
##ef = pd.DataFrame({"R": rets, "Vol": vols})
##ef.plot.scatter(x="Vol", y="R")
##plt.show()

## erk.plot_ef2(25, er[l], cov.loc[l, l])

## N-Asset Efficient Frontier 



w15 = erk.minimize_vol(0.15, er[l], cov.loc[l, l])
vol15 = erk.portfolio_vol(w15, cov.loc[l, l])
## print(vol15) 

b = ["Smoke", "Fin","Games","Coal"]

x = plot_ef(23, er[b], cov.loc[b, b])
print(x)
