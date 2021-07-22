#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 18:51:26 2020

@author: nishant.gupta
"""

import datetime
import pandas as pd

from ai_trader_utils import model_params 
from model_tester import model_tester

tickers = ["ASIANPAINT.BO", "BAJFINANCE.BO"]

params = model_params(state_size = 10,\
                      memory_width = 2000,\
                      gamma = 0.95,\
                      epsilon = 1.0,\
                      epsilon_final = 0.01,\
                      epsilon_decay = 0.995,\
                      input_units = 32,\
                      hidden_layer1_units = 64,\
                      hidden_layer2_units = 128,\
                      activation_func = 'relu',\
                      activation_func_output = 'linear',\
                      loss_func = 'mse',\
                      learning_rate = 0.001,\
                      model_name = 'AI_trader')

start_date_train = datetime.date.today() - datetime.timedelta(750)
end_date_train = datetime.date.today() - datetime.timedelta(365)
start_date_test = datetime.date.today() - datetime.timedelta(365)
end_date_test = datetime.date.today()
trader_results =[]

columns = ["Ticker", "Investment", "Profit", "Num-Buy", "Num-Sell", "Holding %"]
investment_list = []
profit_list = []
holding_pct_list = []
num_buy_list = []
num_sell_list = []
total_profit = 0
for ticker in tickers:
    print("*****************Working on ticker*******************")
    print(ticker)
    tester = model_tester(ticker = ticker,\
                          episodes_used_for_training = 1,\
                          window_size = 10,\
                          batch_size = 32,\
                          model_params = params,\
                          start_date_train = start_date_train,\
                          end_date_train = end_date_train,\
                          start_date_test = start_date_test,\
                          end_date_test = end_date_test)
    
    test_result = tester.test()
    
    # Append the data into the list to be used while creating the dataframe
    profit_list.append(test_result.total_profit)
    investment_list.append(test_result.total_investment)
    num_buy = test_result.num_buy
    num_sell = test_result.num_sell
    num_buy_list.append(num_buy)
    num_sell_list.append(num_sell)
    holding_pct = 0
    if (num_buy != 0) :
        holding_pct = (num_buy - num_sell) / num_buy
    
    holding_pct_list.append(holding_pct)
    
    trader_results.append(test_result)
    total_profit += test_result.total_profit


df = pd.DataFrame(list(zip(tickers,\
                           investment_list,\
                           profit_list,\
                           num_buy_list,\
                           num_sell_list,\
                           holding_pct_list)),\
                          columns = columns)
df.set_index('Ticker', inplace = True)

