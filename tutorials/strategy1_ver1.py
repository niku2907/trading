#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 01:22:28 2020

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
# Two versions of the same strategy based on enable_using_fib_retraction
# This strategy uses fibonacci bands to make a decision. The fibonacci bands yield very good results
# when they are they are used for going short or long. However, this strategy is not assuming those
# cases (coz. I am still not confident about using the Margin cash)

from Common import DecisionParams
from interday_testing_helper import interday_testing_helper
from Strategy import Strategy1
from Strategy_Runner import Strategy_Runner

tickers = ["ASIANPAINT.BO",\
           "AXISBANK.BO",\
           "BAJAJ-AUTO.BO",\
           "BHARTIARTL.BO",\
           "HCLTECH.BO", \
           "HDFCBANK.BO",\
           "HEROMOTOCO.BO",\
           "HINDUNILVR.BO",\
           "INDUSINDBK.BO",\
           "INFY.BO",\
           "ITC.BO",\
           "KOTAKBANK.BO",\
           "LT.BO",\
           "M&M.BO",\
           "MARUTI.BO",\
           "NESTLEIND.BO",\
           "NTPC.BO",\
           "ONGC.BO",\
           "POWERGRID.BO",\
           "SBIN.BO",\
           "SUNPHARMA.BO",\
           "TATASTEEL.BO",\
           "TCS.BO",\
           "TECHM.BO",\
           "ULTRACEMCO.BO"]

interday_data = interday_testing_helper.get_interday_collated_data(tickers, n = 735, delta = 0)
buy_params = DecisionParams(rsi_level = 50, min_obv_slope = 40, max_obv_slope = 90, adx = 23)

sell_params = DecisionParams(rsi_level = 45, min_obv_slope = -90, max_obv_slope = -60, \
                           adx = 13, stop_loss_pct = 0.9, stop_loss_adx_threshold = 30)

strategy = Strategy1(buy_params = buy_params, sell_params = sell_params, \
                     adx_threshold_for_fib_buy = 50, adx_threshold_for_fib_sell = 50, \
                     enable_using_fib_retraction = False)

strategy_runner = Strategy_Runner(strategy, tickers, interday_data, num_simultaneous_buy = 100)
result = strategy_runner.Run()

# Adding following variables as Spyder is not able to unpack user defined datatype and hence
# values are not visible in the Variable explorer
cummulative_ohlc_data = result.modified_interday_data.ohlc_renko
cummulative_interesting_data = result.modified_interday_data.collated_data
cummulative_cagr = result.cummulative_cagr
cummulative_sharpe_ratio = result.cummulative_sharpe_ratio
cummulative_dd = result.cummulative_dd

individual_cagr = result.individual_cagr
individual_sharpe_ratio = result.individual_sharpe_ratio
individual_dd = result.individual_dd

num_profit = result.num_profits
num_loss = result.num_losses
resultant_money = result.resultant_money
holdings_data = result.holdings_data
holdings_data = holdings_data.sort_values("Pct hold")
interday_testing_helper.send_mail_for_interesting_stocks(cummulative_ohlc_data, tickers, holdings_data,\
                                                         version = "V1")

latest_data = interday_testing_helper.get_latest_day_data(cummulative_ohlc_data, holdings_data, tickers)
print("Latest Data")
print(latest_data)