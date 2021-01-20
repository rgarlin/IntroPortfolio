#!/usr/local/bin/python3.8

import yfinance as yf
import pandas as pd
from yahoo_fin import stock_info as si
import datetime
import  argparse
import numpy as np
pd.plotting.register_matplotlib_converters()
import matplotlib.pyplot as plt
import edhec_risk as erk


parser = argparse.ArgumentParser(description='Ticker Symbol')
parser.add_argument('ticker')

args = parser.parse_args()



ticker_sym = yf.Ticker(args.ticker)
pd.set_option('display.max_rows', None)



xday = ticker_sym.history(interval='1d', period="max")
## x = ticker_sym.history(interval='1mo', start="2010-01-20", end="2020-12-01")
## xday = ticker_sym.history(interval='1d', start="2010-01-20", end="2020-12-01")



## gets the closing price

xdaycloseprice = xday.dropna()["Close"]
## divides by 100 to get percent in decimal 

xdayclose = xdaycloseprice/100
## changes date format 
xdayclose.index = pd.to_datetime(xdayclose.index, format="%m")
xdayclose.index = xdayclose.index.to_period('D')

## converts prices to percent change 

xdayreturns = xdayclose.pct_change()
##print(xreturns)


## Rollong averages, but need to get daily data 
x_rolling10 = xdaycloseprice.rolling(window=10).mean()
x_rolling15 = xdaycloseprice.rolling(window=15).mean()
x_rolling30 = xdaycloseprice.rolling(window=30).mean()
x_rolling50 = xdaycloseprice.rolling(window=50).mean()
x_rolling200 = xdaycloseprice.rolling(window=200).mean()


print(f" price {xdaycloseprice.tail(1)[0]}")
print(f" 10-day {x_rolling10.tail(1)[0]}")
print(f" 15-day {x_rolling15.tail(1)[0]}")
print(f" 30-day {x_rolling30.tail(1)[0]}")
print(f" 50-day {x_rolling50.tail(1)[0]}")
print(f" 200-day {x_rolling200.tail(1)[0]}")
