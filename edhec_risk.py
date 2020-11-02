#!/usr/local/bin/python3.8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy
import scipy.stats
from scipy.optimize import minimize

## Builging modules: 


## Drawdown 
def draw_down(return_series: pd.Series):
    """ Takes a time series of returns
    computes and returns a dataframe tha contains
    wealth index, previous peaks and & drawdowns 
    """
    wealth_index = 1000*(1*return_series).cumprod()
    previous_peak = wealth_index.cummax()
    drawdowns = (wealth_index - previous_peak)/previous_peak
    return pd.DataFrame({
        "Wealth" : wealth_index,
        "Peaks" : previous_peak,
        "Drawdown" : drawdowns
    })


def get_ffme_returns():
    me_m = pd.read_csv("Portfolios_Formed_on_ME_monthly_EW.csv", 
                   header=0, index_col=0, parse_dates=True, na_values=-99.99)
    rets = me_m[['Lo 10', 'Hi 10']]
    rets.columns = ['SmallCap','LargeCap']
    rets = rets/100
    rets.index = pd.to_datetime(rets.index, format="%Y%m")
    rets.index = rets.index.to_period('M')
    return rets

def get_hfi_returns():
    hfi = pd.read_csv("edhec-hedgefundindices.csv", 
                   header=0, index_col=0, parse_dates=True)
    hfi = hfi/100
    hfi.index = pd.to_datetime(hfi.index, format="%Y%m")
    hfi.index = hfi.index.to_period('M')
    return hfi


def skewness(r):
    demeaned_r = r - r.mean()
    sigma_r = r.std(ddof=0)
    exp = (demeaned_r**3).mean()
    return(exp/sigma_r**3)

def kurtosis(r):
    demeaned_r = r - r.mean()
    sigma_r = r.std(ddof=0)
    exp = (demeaned_r**4).mean()
    return(exp/sigma_r**4)

def is_normal(r, level=0.01):
    statistic, p_value = scipy.stats.jarque_bera(r)
    return p_value > level

def semideviation(r):
    """ This provides the standard deviation of returns that are 
    less thna 0 
    """
    is_negative = r < 0
    return r[is_negative].std(ddof=0)

def var_his(r, level=5):
    """
    """
    if isinstance(r, pd.DataFrame):
        return r.aggregate(var_his, level=level)
    elif isinstance(r, pd.Series):
        return -np.percentile(r, level)
    else:
        raise TypeError("Excpeted r to be series or dataframe")

def var_gaussian(r, level=5, modified=False):
    """
    Returns the Parametric Gaussian VaR of a Series or DataFra,e
    """
    # computes z score
    z = scipy.stats.norm.ppf(level/100)
    if modified:
        s = skewness(r)
        k = kurtosis(r)
        z = (z +
                 (z**2 - 1)*s/6 +
                 (z**3 - 3*z)*(k-3)/24 -
                 (2*z**3 - 5*z)*(s**2)/36
                 )
    
    return -(r.mean() + z*r.std(ddof=0))

def cvar_his(r, level=5):
    """
    Computes cnditional var of a seriers or dataframe
    """
    if isinstance(r, pd.Series):
        is_beyond = r <= -var_his(r, level=level)
        return -r[is_beyond].mean()
    elif isinstance(r, pd.DataFrame):
        return r.aggregate(cvar_his, level=level)
    else:
        raise TypeError("R should be a series or dataframe")

def get_ind_returns():
    ind = pd.read_csv("ind30_m_vw_rets.csv", header=0, index_col=0)/100
    ind.index = pd.to_datetime(ind.index, format="%Y%m").to_period('M')
    ind.columns = ind.columns.str.strip()
    return ind

def annualize_rets(r, periods_per_year):
    compounded_growth= (1+r).prod()
    n_periods = r.shape[0]
    return compounded_growth**(periods_per_year/n_periods)-1

def annualize_vol(r, periods_per_year):
    return r.std()*(periods_per_year**.05)

def share_ratio(r, riskfree_rate, periods_per_year):
    rf_per_period = (1+riskfree_rate)**(1/periods_per_year)-1
    excess_ret = r - rf_per_period
    ann_ex_ret = annualize_rets(excess_ret, periods_per_year)
    ann_vol = annualize_vol(r, periods_per_year)
    return ann_ex_ret/ann_vol

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

def plot_ef2(n_points, er, cov):
    if er.shape[0] !=2 or er.shape[0] != 2:
        raise ValieError("Can only lot 2 assets ")
    weights = [np.array([w, 1-w]) for w in np.linspace(0, 1, n_points)]
    rets = [portfolio_return(w, er) for w in weights]
    vols = [portfolio_vol(w, cov) for w in weights]
    ef = pd.DataFrame({"Returns": rets, "Volality": vols})
    return ef.plot.line(x="Vol", y="returns")

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
        'fun': lambda weights, er:target_return - portfolio_return(weights, er) 
    }
    weights_sum_to_1 = {
        'type': 'eq',
        'fun': lambda weights: np.sum(weights)-1
    }
    results = minimize(portfolio_vol, init_guess, 
                args=(cov,), method="SLSQP", 
                constraints=(return_is_target, weights_sum_to_1),
                bounds=bounds
                )
    return(results.x)
    

