# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 03:21:05 2023

@author: NishantGupta
"""

from data_reader import data_reader 
from datetime import date, datetime, timedelta
from util import util

screener_output_file = "SCREENER_BACKTEST_FILE.csv"
screener_output_data = data_reader.read_csv(screener_output_file)
stocks_interesting_dates = {}
for i in range(len(screener_output_data)):
    stock = screener_output_data['symbol'][i]
    if (stocks_interesting_dates.get(stock)) is None:
        stocks_interesting_dates[stock] = []
        
    interesting_date = screener_output_data['date'][i]
    date_object = date(int(interesting_date.split('-')[2]),\
                       int(interesting_date.split('-')[1]),\
                       int(interesting_date.split('-')[0]))
    stocks_interesting_dates[stock].append(date_object)
    

