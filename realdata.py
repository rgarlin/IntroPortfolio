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



## rets = me_m[['Lo 10', 'Hi 10']]
## rets.columns = ['SmallCap','LargeCap']
## rets = rets/100
## rets.index = pd.to_datetime(rets.index, format="%Y%m")
## rets.index = rets.index.to_period('M')
## pd.set_option('display.max_rows', None)

##print(rets.head())
##rets.plot.line()
##plt.show()

## Compute drawdown 
## Compute Wealth index
## Compute previouspeaks 
## compute drawdown wealth values as a percenage from previous peaks
## wealth_index = 1000*(1+rets["LargeCap"]).cumprod()
## pd.set_option('display.max_rows', None)

##wealth_index.plot.line()
##plt.show()

## computes previous peaks 
## previous_peak = wealth_index.cummax()
##previous_peak.plot.line()
##plt.show()

## draw_down = (wealth_index - previous_peak)/previous_peak
##draw_down.plot.line()
##plt.show()
##print(draw_down.min())
## results = drawdown(rets["LargeCap"])
##print(results.head())
## slices individual columns
## wealth_peaks = drawdown(rets[:"1950"]["LargeCap"])[["Wealth", "Peaks"]]
## wealth_peaks.head()
## 
##wealth_peaks.plot.line()
##plt.show()


##print(draw_down["2009"].idxmin())
##print(draw_down["2009"].min())

## Everything above from class 

parser = argparse.ArgumentParser(description='Ticker Symbol')
parser.add_argument('ticker')

args = parser.parse_args()



ticker_sym = yf.Ticker(args.ticker)
pd.set_option('display.max_rows', None)


x = ticker_sym.history(interval='1mo', period="max")
xday = ticker_sym.history(interval='1d', period="max")
##x = msft.history(period="1d")
y = ticker_sym.splits
z = ticker_sym.dividends

## gets the closing price
xcloseprice = x.dropna()["Close"]
xdaycloseprice = xday.dropna()["Close"]
## divides by 100 to get percent in decimal 
xclose = xcloseprice/100
xdayclose = xdaycloseprice/100
## changes date format 
xclose.index = pd.to_datetime(xclose.index, format="%Y%m")
xclose.index = xclose.index.to_period('M')
xdayclose.index = pd.to_datetime(xdayclose.index, format="%Y%m")
xdayclose.index = xdayclose.index.to_period('M')


## converts prices to percent change 
xreturns = xclose.pct_change()
xdayreturns = xdayclose.pct_change()
##print(xreturns)

## Creates a wealth index with 1,000 start value 
wealth_xclose = round(1000*(1+xreturns).cumprod(),2)
##print(wealth_xclose.head)
##wealth_xclose.plot.line()
##plt.show()

## computes previous peaks 
previous_xpeak = wealth_xclose.cummax()
##previous_xpeak.plot.line()
##plt.show()

## Computes drawdown from previous peaks.
xdraw_down = (wealth_xclose - previous_xpeak)/previous_xpeak
print(xdraw_down.idxmin())
print(round(xdraw_down.min(),2)*100)
xdraw_down.plot.line()
plt.show()

##wealth_peaks = drawdown(rets[:"1950"]["LargeCap"])[["Wealth", "Peaks"]]
##wealth_peaks.head()

## xwealth_peaks = drawdown(xreturns["1997":])
xwealth_peaks = drawdown(xreturns)
##print(xwealth_peaks.head(20))

xwealth_peaks.plot.line()
plt.show()
##print("Gaussian")
##print(erk.var_gaussian(xreturns, modified=True))

annualize_returnsp = (xreturns+1).prod()**(12/xreturns.shape[0]) -1
print('annual returns')
##print(annualize_returnsp)
print(erk.annualize_rets(xreturns, 12))
print('annualized vol lower the better')
print(erk.annualize_vol(xreturns, 12))
## when looking at sharpe ratios the higher the better 
print('sharpe ratio')
print('   * under 1 sub-optimal')
print('   * Greater than 1 acceptable')
print('   * Greater than 2 very good')
print(erk.share_ratio(xreturns, 0.015, 12))
wealth_index = 1000*(1+xreturns).cumprod()
print("Wealth Index")
print(round(wealth_index.dropna(), 2).head(1))
print(round(wealth_index, 2).tail(1))

## rsi
delta = xdayclose.diff()
up, down = delta.copy(), delta.copy()
up[up < 0] = 0
down[down > 0] = 0
period = 14
roll_up = up.ewm(com=period - 1, adjust=False).mean()
roll_down = down.ewm(com=period - 1, adjust=False).mean().abs()
rs = roll_up / roll_down   # relative strength =  average gain/average loss
rsi = 100-(100/(1+rs))

## Rollong averages, but need to get daily data 
x_rolling = xdaycloseprice["2017":].rolling(window=30).mean()
x_rolling50 = xdaycloseprice["2017":].rolling(window=50).mean()
x_rolling200 = xdaycloseprice["2017":].rolling(window=200).mean()
xdaycloseprice["2017":].plot.line(label='stock price', legend=True)
x_rolling.plot.line(label='30 DMA', legend=True)
x_rolling50["2017":].plot.line(label='50 DMA', legend=True)
x_rolling200["2017":].plot.line(label='200 DMA', legend=True)
plt.show()

## test RSI
rsi.tail(25000).plot.line(label="RSI", legend=True)
plt.axhline(0, linestyle='--', alpha=0.1)
plt.axhline(20, linestyle='--', alpha=0.5)
plt.axhline(30, linestyle='--')

plt.axhline(70, linestyle='--')
plt.axhline(80, linestyle='--', alpha=0.5)
plt.axhline(100, linestyle='--', alpha=0.1)
plt.show()
print(rsi.tail(25000))
