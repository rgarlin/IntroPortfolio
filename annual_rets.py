#!/usr/local/bin/python3.8

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import edhec_risk as erk
import scipy.stats
import scipy
from scipy.optimize import minimize
import  argparse


def compound(r):
    """
    returns the result of compounding the set of returns in r
    """
    return np.expm1(np.log1p(r).sum())

parser = argparse.ArgumentParser(description='Ticker Symbol')
parser.add_argument('ticker')

args = parser.parse_args()



ticker_sym = yf.Ticker(args.ticker)
pd.set_option('display.max_rows', None)



xday = ticker_sym.history(interval='1d', period="max")
xdaycloseprice = xday.dropna()["Close"]
xdayclose = xdaycloseprice/100
xdayreturns = xdayclose.pct_change()

## print(xdayreturns.head(10))
## bkka_d is daily retunrs and reample converts that to monthy returns
x_month = xdayreturns.resample('Y').apply(compound).to_period('Y')
print(round(x_month*100,2))