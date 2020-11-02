#!/usr/local/bin/python3.8
import yfinance as yf
import pandas as pd
import openpyxl
import os
from yahoo_fin import stock_info as si
import datetime




msft = yf.Ticker("ANET")
pd.set_option('display.max_rows', None) 


x = msft.history(interval='1mo', period="max")
print(x.head(100))
