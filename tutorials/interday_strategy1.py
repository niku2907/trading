#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 19:42:34 2020

@author: nishant.gupta
"""

# Strategy: This strategy used RSI + OBV slope for a stock which movers btn. Resistance and Support
# Since OBV is a leading indicator, sudden drop or rise does not mean the corresponding change
# in the price, we are hence bounding the OBV slope inorder to avoid buy/sell during that period
# Tuned values:
# OBV values: BUY (-10, -50) & SELL (30, 50)
# RSI values: BUY (<50: neutral or bullish) & SELL (>50: Bullish or neutral)
# ADX values: BUY (> 23) , Stop loss (> 30), SELL (>13)
# Stop value is 10% of the buy price
# KPIs ARE CALCULATED BY ASSUMING THAT WE SELL THE STOCKS BOUGHT BEFORE BUYING AGAIN
# Reason to buy even in neutral condition is based on the data for banking sector
# For banking sector OBV slope n = 5 (last 5 days OBV slope)

import numpy as np
import pandas as pd

from kpis import KPI
from interday_testing_helper import interday_testing_helper

tickers = ["HEROMOTOCO.BO", "TVSMOTOR.BO"]
interday_data = interday_testing_helper.get_interday_collated_data(tickers, n = 730, delta = 45)
collated_data = interday_data.collated_data

data = interday_data.ohlc_renko

# Now that we have all the data collated, we move to finding the signals and returns
profit = 0
loss = 0
for ticker in tickers:
  print("calculating daily returns for ",ticker)
  buy = 0
  buy_price = 0
  for i in range(len(interday_data.ohlc_renko[ticker])):
    if (i < 14):
      interday_data.tickers_ret[ticker].append(0)   
      interday_data.tickers_signal[ticker].append('NA')
      continue;
    if (buy == 0) :
      interday_data.tickers_ret[ticker].append(0)           
      if interday_data.ohlc_renko[ticker]["RSI"][i] < 50 and \
         interday_data.ohlc_renko[ticker]["obv_slope"][i] < -10 and interday_data.ohlc_renko[ticker]["obv_slope"][i] > -50 and \
         interday_data.ohlc_renko[ticker]["ADX"][i] > 23:
        print("Buying the: ", ticker, " at ", interday_data.ohlc_renko[ticker]["Adj Close"][i])
        print("Bar num: ", interday_data.ohlc_renko[ticker]["bar_num"][i], "Slope: ", interday_data.ohlc_renko[ticker]["obv_slope"][i], " RSI: ", interday_data.ohlc_renko[ticker]["RSI"][i])
        buy = 1
        buy_price = interday_data.ohlc_renko[ticker]["Adj Close"][i]
        interday_data.tickers_signal[ticker].append('B')
      else:
        interday_data.tickers_signal[ticker].append('NA')
    else :
      if interday_data.ohlc_renko[ticker]["RSI"][i] > 50 and \
         interday_data.ohlc_renko[ticker]["obv_slope"][i] > 30 and interday_data.ohlc_renko[ticker]["obv_slope"][i] < 50 and \
         interday_data.ohlc_renko[ticker]["ADX"][i] > 13 :
        buy = 0
        interday_data.tickers_ret[ticker].append((interday_data.ohlc_renko[ticker]["Adj Close"][i] / buy_price) - 1)
        print("Return booked : ", interday_data.ohlc_renko[ticker]["Adj Close"][i] / buy_price)
        if (buy_price >= interday_data.ohlc_renko[ticker]["Adj Close"][i]) :
          loss += 1
        else:
          profit += 1
        buy_price = 0
        interday_data.tickers_signal[ticker].append('S')
      elif interday_data.ohlc_renko[ticker]["Adj Close"][i] < 0.9 * buy_price and \
        (interday_data.ohlc_renko[ticker]["ADX"][i] > 30) :
        # We set the stop loss at -10% of the buy price. Also, making sure if there is a strong
        # falling trend or not
        interday_data.tickers_ret[ticker].append((interday_data.ohlc_renko[ticker]["Adj Close"][i] / buy_price) - 1)
        interday_data.tickers_signal[ticker].append('S')
        buy_price = 0
        buy = 0
        print("Return booked : ", interday_data.ohlc_renko[ticker]["Adj Close"][i] / buy_price)
      else :
        interday_data.tickers_ret[ticker].append(0)
        interday_data.tickers_signal[ticker].append('Hold')
  interday_data.ohlc_renko[ticker]["ret"] = np.array(interday_data.tickers_ret[ticker])
  interday_data.ohlc_renko[ticker]["State"] = np.array(interday_data.tickers_signal[ticker])

# calculating overall strategy's KPIs
strategy_df = pd.DataFrame()
for ticker in tickers:
    strategy_df[ticker] = interday_data.ohlc_renko[ticker]["ret"]
strategy_df["ret"] = strategy_df.mean(axis=1)
new_cagr = KPI.CAGR(strategy_df)
new_sharpe = KPI.sharpe(strategy_df,0.025)
new_dd = KPI.max_dd(strategy_df)

#calculating individual stock's KPIs
cagr = {}
sharpe_ratios = {}
max_drawdown = {}
for ticker in tickers:
    print("calculating KPIs for ",ticker)      
    cagr[ticker] =  KPI.CAGR(interday_data.ohlc_renko[ticker])
    sharpe_ratios[ticker] =  KPI.sharpe(interday_data.ohlc_renko[ticker],0.025)
    max_drawdown[ticker] =  KPI.max_dd(interday_data.ohlc_renko[ticker])