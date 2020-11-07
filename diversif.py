#!/usr/local/bin/python3.8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import edhec_risk as erk
import scipy.stats
import scipy
from scipy.optimize import minimize

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

ind_return = erk.get_ind_returns()
ind_nfirms = erk.get_ind_nfirms()
ind_size = erk.get_ind_size()

ind_mktcap = ind_nfirms * ind_size
total_mktcap = ind_mktcap.sum(axis="columns")

## total_mktcap.plot.line()
## plt.show()

ind_capweight = ind_mktcap.divide(total_mktcap, axis="rows")
ind_capweight["1926"].sum(axis="columns")

## ind_capweight[["Fin", "Steel"]].plot.line()
## plt.show()

total_market_return = (ind_capweight*ind_return).sum(axis="columns")
## total_market_return.plot.line()
## plt.show()

total_market_index = 1000*(1+total_market_return).cumprod()
## total_market_index.plot.line()
## plt.show()

## total_market_index["1980":].plot.line()
## total_market_index["1980":].rolling(window=36).mean().plot.line()
## plt.show()

## This will give the traling 36 months compounded return return
tml_tr36rets = total_market_return.rolling(window=36).aggregate(erk.annualize_rets, periods_per_year = 12)
## tml_tr36rets.plot.line()
## total_market_return.plot.line() 
## plt.show()

## Rolling Correlations - along with Multiindexes and .groupby
ts_corr = ind_return.rolling(window=36).corr()
ts_corr.index.names = ['date', 'Industry']

ind_tr36corr = ts_corr.groupby(level='date').apply(lambda cormat: cormat.values.mean())
## ind_tr36corr.plot.line()

## tml_tr36rets["2007":].plot.line(label='Tr36 months rets')
## ind_tr36corr["2007":].plot.line(label='Tr36 months corr', secondary_y=True)
## plt.show()

print(tml_tr36rets.corr(ind_tr36corr))










