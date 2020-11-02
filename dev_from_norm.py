#!/usr/local/bin/python3.8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import edhec_risk as erk
import scipy.stats


## hfi = erk.get_hfi_returns()
##print(pd.concat([hfi.mean(), hfi.median(), hfi.mean()>hfi.median()], axis="columns"))

hfi = pd.read_csv("edhec-hedgefundindices.csv", 
                   header=0, index_col=0, parse_dates=True)
me_m = pd.read_csv("Portfolios_Formed_on_ME_monthly_EW.csv", 
                   header=0, index_col=0, parse_dates=True)
## skewness
erk.skewness(hfi).sort_values()

## provide skewness with built in scipy module
## print(scipy.stats.skew(hfi))
##

normal_rets = np.random.normal(0, .15, size=(263000, 1))
## print(erk.skewness(normal_rets))


## Kurtosis first uses a function, second line uses built in scipy module
normal_rets = np.random.normal(0, .15, size=(263000, 1))
## print(erk.kurtosis(hfi))
## print(scipy.stats.kurtosis(normal_rets))

## comares to Jarque Bera 
scipy.stats.jarque_bera(normal_rets)

scipy.stats.jarque_bera(hfi)

hfi.aggregate(erk.is_normal)
erk.is_normal(hfi)

## skewness for Large and small caps 
ffme = erk.get_ffme_returns()
print(erk.skewness(ffme))
print(erk.kurtosis(ffme))

