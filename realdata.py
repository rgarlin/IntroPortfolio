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

me_m = pd.read_csv("Portfolios_Formed_on_ME_monthly_EW.csv", 
                   header=0, index_col=0, parse_dates=True, na_values=-99.99)


rets = me_m[['Lo 10', 'Hi 10']]
rets.columns = ['SmallCap','LargeCap']
rets = rets/100
rets.index = pd.to_datetime(rets.index, format="%Y%m")
rets.index = rets.index.to_period('M')
pd.set_option('display.max_rows', None)

##print(rets.head())
##rets.plot.line()
##plt.show()

## Compute drawdown 
## Compute Wealth index
## Compute previouspeaks 
## compute drawdown wealth values as a percenage from previous peaks
wealth_index = 1000*(1+rets["LargeCap"]).cumprod()
pd.set_option('display.max_rows', None)

##wealth_index.plot.line()
##plt.show()

## computes previous peaks 
previous_peak = wealth_index.cummax()
##previous_peak.plot.line()
##plt.show()

draw_down = (wealth_index - previous_peak)/previous_peak
##draw_down.plot.line()
##plt.show()
##print(draw_down.min())
results = drawdown(rets["LargeCap"])
##print(results.head())
## slices individual columns
wealth_peaks = drawdown(rets[:"1950"]["LargeCap"])[["Wealth", "Peaks"]]
wealth_peaks.head()

##wealth_peaks.plot.line()
##plt.show()


##print(draw_down["2009"].idxmin())
##print(draw_down["2009"].min())



parser = argparse.ArgumentParser(description='Ticker Symbol')
parser.add_argument('ticker')

args = parser.parse_args()



msft = yf.Ticker(args.ticker)
pd.set_option('display.max_rows', None)


x = msft.history(interval='1mo', period="max")
##x = msft.history(period="1d")
y = msft.splits
z = msft.dividends

xclose = x.dropna()["Close"]
xclose = xclose/100
xclose.index = pd.to_datetime(xclose.index, format="%Y%m")
xclose.index = xclose.index.to_period('M')
xreturns = xclose.pct_change()
##print(xreturns)

##xreturns.plot.line()
##plt.show()
##wealth_index = 1000*(1+rets["LargeCap"]).cumprod()
wealth_xclose = round(1000*(1+xreturns).cumprod(),2)
##print(wealth_xclose.head)

##wealth_xclose.plot.line()
##plt.show()

## computes previous peaks 
previous_xpeak = wealth_xclose.cummax()
##previous_xpeak.plot.line()
##plt.show()

xdraw_down = (wealth_xclose - previous_xpeak)/previous_xpeak
print(xdraw_down.min())
xdraw_down.plot.line()
plt.show()

##wealth_peaks = drawdown(rets[:"1950"]["LargeCap"])[["Wealth", "Peaks"]]
##wealth_peaks.head()

xwealth_peaks = drawdown(xreturns)
##print(xwealth_peaks.head(20))

xwealth_peaks.plot.line()
plt.show()
erk.var_gaussian(xreturns, modified=True)

annualize_returnsp = (xreturns+1).prod()**(12/xreturns.shape[0]) -1
print('annual returns')
print(annualize_returnsp)
print(erk.annualize_rets(xreturns, 12))
print('annualized vol lower the better')
print(erk.annualize_vol(xreturns, 12))
## when looking at sharpe ratios the higher the better 
print('sharpe ratio higher the better ')
print(erk.share_ratio(xreturns, 0.03, 12))