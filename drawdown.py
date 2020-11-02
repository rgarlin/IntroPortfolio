#!/usr/local/bin/python3.8

import pandas as pd
import numpy as np
pd.plotting.register_matplotlib_converters()
import matplotlib.pyplot as plt


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
print(rets)
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
##drawdown.plot.line()
##plt.show()
print(draw_down.min())
results = drawdown(rets["LargeCap"])
print(results.head())
## slices individual columns
wealth_peaks = drawdown(rets[:"1950"]["LargeCap"])[["Wealth", "Peaks"]]
wealth_peaks.head()

wealth_peaks.plot.line()
plt.show()


print(draw_down["2009"].idxmin())
print(draw_down["2009"].min())
