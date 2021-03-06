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

## Drawdown 

def drawdown(return_series: pd.Series):
    """ Takes a time series of returns
    computes and returns a dataframe tha contains
    wealth index, previous peaks and & drawdowns 
    """
    wealth_index = 1000*(1+return_series).cumprod()
    previous_peak = wealth_index.cummax()
    drawdowns = (wealth_index - previous_peak)/previous_peak
    return pd.DataFrame({
        "Wealth" : wealth_index,
        "Peaks" : previous_peak,
        "Drawdowns" : drawdowns
    })


pd.set_option('display.max_rows', None)
parser = argparse.ArgumentParser(description='Ticker Symbol')
parser.add_argument('ticker')
parser.add_argument('ticker1')
parser.add_argument('amount')

args = parser.parse_args()

ticker_sym = yf.Ticker(args.ticker)
ticker_sym1 = yf.Ticker(args.ticker1)

pd.set_option('display.max_rows', None)

stock1 = ticker_sym.history(interval='1d', start="2020-07-22", end="2020-11-25")
stock2 = ticker_sym1.history(interval='1d', start="2020-07-22", end="2020-11-25")

##x = msft.history(period="1d")
## y = ticker_sym.splits
## z = ticker_sym.dividends

## gets the closing price
stock1closepr = stock1.dropna()["Close"]
stock2closepr = stock2.dropna()["Close"]
print(stock1closepr)
## divides by 100 to get percent in decimal 
stock1close = stock1closepr/100
stock2close = stock2closepr/100

## changes date format 

stock1close.index = pd.to_datetime(stock1close.index, format="%Y%m")
stock1close.index = stock1close.index.to_period('D')
stock2close.index = pd.to_datetime(stock2close.index, format="%Y%m")
stock2close.index = stock2close.index.to_period('D')


## converts prices to percent change 

stock1rets =  stock1close.pct_change()
stock2rets =  stock2close.pct_change()


## Creates a wealth index with 1,000 start value 

wealth_stock1close = round(int(args.amount)*(1+stock1rets).cumprod(),2)
wealth_stock2close = round(int(args.amount)*(1+stock2rets).cumprod(),2)
wealth_stock1close.plot.line(label=ticker_sym, legend=True)
wealth_stock2close.plot.line(label=ticker_sym1, legend=True)
plt.show()
wealth1last = (wealth_stock1close.tail(1))
wealth2last = (wealth_stock2close.tail(1))
print(wealth1last[0] - wealth2last[0])
print(str(ticker_sym) + " returns")
print(((wealth1last[0]/int(args.amount))-1)*100)
print(str(ticker_sym1) + " returns")
print(((wealth2last[0]/int(args.amount))-1)*100)
