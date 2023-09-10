# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 18:36:44 2023

@author: NishantGupta
"""

import math
import pandas as pd
import requests
import sys

from data_reader import data_reader 
from datetime import date, datetime, timedelta
from enum import Enum
from util import util
from zerodha_ticker_id import rsi_screener_tickers
    
def get_ticker_id(interesting_name):
    #TODO: Refactor this
    missing_stocks = []
    interesting_id = -1
    for ticker_id, ticker_name in rsi_screener_tickers.items():
        if ticker_name == interesting_name:
            interesting_id = ticker_id
            break
        
    return interesting_id

def preprocess():
    screener_output_file = "BREAKOUT_SCREENER_BACKTEST_FILE_09_08_23_v3.csv"
    #screener_output_file = "RSI_SCREENER_BACKTEST_FILE_05_08_23.csv"
    screener_output_data = data_reader.read_csv(screener_output_file)
    stocks_interesting_dates = {}
    interesting_ticker_dict = {}
    missing_stocks = set()
    for i in range(len(screener_output_data)):
        stock = screener_output_data['symbol'][i]        
        if (stocks_interesting_dates.get(stock)) is None:
            stocks_interesting_dates[stock] = []
            
        interesting_date = screener_output_data['date'][i]
        date_object = date(int(interesting_date.split('-')[2]),\
                           int(interesting_date.split('-')[1]),\
                           int(interesting_date.split('-')[0]))
        stocks_interesting_dates[stock].append(date_object)
        ticker_id = get_ticker_id(stock)
        if (ticker_id == -1 and stock not in missing_stocks):
            #print("Stock: " + str(stock))
            missing_stocks.add(stock)
        else:
            interesting_ticker_dict.update({get_ticker_id(stock): stock})
        
        
    return stocks_interesting_dates, interesting_ticker_dict, missing_stocks

def get_dates_within_a_window(stocks_interesting_dates, window):
    stock_filtered_dates = {}
    for stock, all_dates in stocks_interesting_dates.items():
        next_interesting_date = datetime.now()
        if stock_filtered_dates.get(stock) is None:
            stock_filtered_dates[stock] = []
            stock_filtered_dates[stock].append(all_dates[0])
            next_interesting_date = all_dates[0] + timedelta(days = window)
            
        for current_date in all_dates[1:]:
            if current_date < next_interesting_date:
                continue
            
            stock_filtered_dates[stock].append(current_date)
            # if current_date == test_date:
            #     print("Current date: " + str(current_date) + "Stock: " + str(stock))
            next_interesting_date = current_date + timedelta(days = window)
            
    return stock_filtered_dates
            
            
            
        

stocks_interesting_dates, interesting_ticker_dict, missing_stocks = preprocess()
current_date = datetime.now().date()
stock_filtered_dates = get_dates_within_a_window(stocks_interesting_dates, 90)

date_wise_stocks = {}
for stock, date_list in stock_filtered_dates.items():
    for filtered_date in date_list:
        if date_wise_stocks.get(filtered_date) is None:
            date_wise_stocks[filtered_date] = []
        date_wise_stocks[filtered_date].append(stock)

