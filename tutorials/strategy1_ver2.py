#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 02:28:16 2020

@author: nishant.gupta
"""

# Strategy1: This strategy used RSI + OBV slope
# Since OBV is a leading indicator, sudden drop or rise does not mean the corresponding change
# in the price, we are hence bouding the OBV slope inorder to avoid buy/sell during that period
# Tuned values:
# for BANKING sector :
# OBV values: BUY (-30, -50) & SELL (20, 23)
# RSI values: BUY (<50: neutral or bullish) & SELL (>55: Bullish)
# Reason to buy even in neutral condition is based on the data for banking sector
# For banking sector OBV slope n = 5 (last 5 days OBV slope)
# We have used ADX in this strategy as well but that does not have much impact on the CGR
# This is because ADX should be referred to when we are not sure about the trend but for 
# uptrend stock OBV slope and RSI are enough and we don't need to refer to the third indicator
# However, ADX is very useful when  a stock is constantly moving btn. Resistance and support
# Refer to interday_strategy1.py for such a case
# Two versions of the same strategy based on enable_using_fib_retraction
# If enable_using_fib_retraction is used following are the parameters:
# R1,S1 or R2,S2 or R3,S3 depends on the state the market is in right now
# in a very bullish market R2 or R3 should be used with S1 or S2
# in a very bearish market R1 should be used with S2 or S3

from Common import DecisionParams
from interday_testing_helper import interday_testing_helper
from Strategy import Strategy1
from Strategy_Runner import Strategy_Runner

tickers = ["BAJFINANCE.BO",\
           "HDFC.BO",\
           "ICICIBANK.BO",\
           "RELIANCE.BO",\
           "TITAN.BO"]


interday_data = interday_testing_helper.get_interday_collated_data(tickers, n = 735, delta = 0)
buy_params = DecisionParams(rsi_level = 50, min_obv_slope = 40, max_obv_slope = 90, adx = 0)

sell_params = DecisionParams(rsi_level = 50, min_obv_slope = -90, max_obv_slope = -60, \
                           adx = 16, stop_loss_pct = 0.8, stop_loss_adx_threshold = 30)

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
interday_testing_helper.send_mail_for_interesting_stocks(cummulative_ohlc_data, tickers, \
                                                         holdings_data, version = "V2")
latest_data = interday_testing_helper.get_latest_day_data(cummulative_ohlc_data, holdings_data, tickers)
print("Latest Data")
print(latest_data)