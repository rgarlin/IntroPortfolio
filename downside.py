#!/usr/local/bin/python3.8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import edhec_risk as erk
import scipy.stats
import scipy


def var_his(r, level=5):
    """
    """
    if isinstance(r, pd.DataFrame):
        return r.aggregate(var_his, level=level)
    elif isinstance(r, pd.Series):
        return -np.percentile(r, level)
    else:
        raise TypeError("Excpeted r to be series or dataframe")



hfi = erk.get_hfi_returns()

## Semideviation 
## Computes the standard deviation for oly returns that are negative
## hfi[hfi<0].std(ddof=0)

## using the function 
erk.semideviation(hfi)

## 3 variation of VaR
## Historic VAR look at what happens in history, pass returns 
## Parametric VaR - Gaussian looks as the past as only a sample and models that 
## Cornish-Fisher VaR - not Gaussian, have large positive and negative swings. 

np.percentile(hfi, 5, axis=0)
var_his(hfi)
## Computes the standard deviation for oly returns that are negative uses function from import 
erk.var_his(hfi)


## z score tells from far it is from the mean 
z = scipy.stats.norm.ppf(0.1)

## Formula at risk at the 5% level
-hfi.mean() + z*hfi.std(ddof=0)
## use function in erk doesn't work  
erk.var_gaussian(hfi)

## Cornish-Fisher 
var_list = erk.var_gaussian(hfi), erk.var_gaussian(hfi, modified=True), erk.var_his(hfi)
comparison=pd.concat(var_list, axis=1)
comparison.columns = ["Gau", "Corn", "His"]
print(comparison)

print(erk.cvar_his(hfi))