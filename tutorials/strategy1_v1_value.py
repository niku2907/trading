#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 01:21:43 2020

@author: nishant.gupta
"""


from Common import DecisionParams
from interday_testing_helper import interday_testing_helper
from Strategy import Strategy1
from Strategy_Runner import Strategy_Runner

tickers = ["ITC.BO",\
"UPL.BO",\
"ONGC.BO",\
"IOC.BO",\
"RELIANCE.BO",\
"NATIONALUM.BO",\
"HINDPETRO.BO",\
"DLF.BO",\
"HEXAWARE.BO",\
"NCC.BO",\
"PHILIPCARB.BO",\
"ARVIND.BO",\
"BEML.BO",\
"BALRAMCHIN.BO",\
#"BSOFT.BO",\
"VSTIND.BO",\
"GSPL.BO",\
"BIRLACORPN.BO",\
"RAIN.BO",\
"TV18BRDCST.BO",\
"BALAMINES.BO",\
"RAYMOND.BO",\
"DBREALTY.BO",\
"CYIENT.BO",\
"SUDARSCHEM.BO",\
"DIVISLAB.BO",\
"FRETAIL.BO",\
#"ISEC.BO",\
"NBCC.BO",\
"GMRINFRA.BO",\
"JSWENERGY.BO",\
#"CHOLAHLDNG.BO",\
"LTI.BO",\
"MRPL.BO",\
"RAJESHEXPO.BO",\
"MFSL.BO",\
"EXIDEIND.BO",\
"RAMCOCEM.BO",\
"SUPREMEIND.BO"]

interday_data = interday_testing_helper.get_interday_collated_data(tickers, n = 735, delta = 0)

# Adding parameters for V2
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
interday_testing_helper.send_mail_for_interesting_stocks(cummulative_ohlc_data, tickers, holdings_data,\
                                                         version = "value")

latest_data = interday_testing_helper.get_latest_day_data(cummulative_ohlc_data, holdings_data, tickers)
print("Latest Data")
print(latest_data)