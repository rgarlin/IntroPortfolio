#!/usr/local/bin/python3.8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

## print((prices_np[1:]/prices_np[:-1] -1) * 100)

## pct_change() pandas function that convers prices to per change
prices = pd.read_csv("sample_prices.csv")
returns = prices.pct_change()
returns = returns.dropna()
print(returns)                   


## This will compute standard deviation 

print(returns.std())


## Compute standard deviation manually 
deviations = returns - returns.mean()
squared_deviations = deviations**2
number_of_obs = returns.shape[0]
variance = squared_deviations.sum()/(number_of_obs -1)
volatility = np.sqrt(variance)
print(volatility)

## Below will annualize the volality 
print(returns.std()*np.sqrt(12))


me_m = pd.read_csv("Portfolios_Formed_on_ME_monthly_EW.csv", 
                   header=0, index_col=0, parse_dates=True, na_values=-99.99)

## This cuts out the 2 columns you need 
columns = ["Lo 10", "Hi 10"]
## Makes me_m with only those 2 columns 
me_m = me_m[columns]
## divides by 100 so .03 instead of 3% 
me_m = me_m/100
## Changes column names
me_m.columns = ["Small Cap", "Large Cap"]
print(me_m)
## Basic plots 
##plt.plot(me_m)
##plt.show()

print(me_m.std())
## takes monthly data and annualizes volality 
annualize_vol = me_m.std()*np.sqrt(12)
print(annualize_vol)

## This will gie you the average return per month 
return_per_month = (me_m+1).prod()**(1/me_m.shape[0]) -1
print(return_per_month)

## This uses retrun per month to anualize the return 
annualize_return = (return_per_month+1)**12 -1
print(annualize_return)

## Smplier way to do annualized return 
## (me_m+1).prod - returns we saw compounded 
##  raised to the 12th power 
## divided by number of months 
annualize_returnsp = (me_m+1).prod()**(12/me_m.shape[0]) -1
print(annualize_returnsp)

## Simple method for return with volality 
print(annualize_return/annualize_vol)


## Sharpe ration excess return over risk free rate
riskfree_rate = 0.03
excess_return = annualize_return - riskfree_rate
sharpe_ratio = excess_return/annualize_vol
print(sharpe_ratio)












