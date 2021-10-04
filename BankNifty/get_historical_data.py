#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 22:08:22 2021

@author: nishant.gupta
"""


#curl "https://google.com/"
#curl 'https://kite.zerodha.com/oms/instruments/historical/260105/5minute?user_id=JB7207&oi=1&from=2021-04-17&to=2021-04-22'

import json
import pandas as pd
import requests

import datetime

from zerodha_ticker_id import name_zerodha_nse_id_dict
from zerodha_ticker_id import name_zerodha_nse_id_realty_dict
from zerodha_ticker_id import name_zerodha_nse_id_it_dict
from zerodha_ticker_id import name_zerodha_nse_id_fmcg_dict
from zerodha_ticker_id import shortlisted_tickers_dict
from zerodha_ticker_id import buy_stocks_dict

headers = {'authority':'kite.zerodha.com',\
           'accept':'application/json, text/plain, */*',\
           'authorization':'enctoken gAN8bQJcaU6qgwdGhUe4c5QwVDVFiMi/z5tlf+DKGbHiPGGWOPisvujRbJ8aZf7vb6kkpec1t7KTl0kefIf+wgi6mzicV6CtDcmnDqzQ5/nmLD7PX9FRXw=='}

def get_historical_data(ticker_id, ticker_name, num_two_months, num_minute_data):
    
    start_date = datetime.date.today()-datetime.timedelta(num_two_months*60)
    num_months = num_two_months * 2
    file_name = "1_YEAR_TICKER_DATA/" + ticker_name + "_" + str(num_months) + "_MONTH_" + num_minute_data +\
        "_MINUTE_DATA.xlsx" 
    data = []
    for i in range(num_two_months):
        
        end_date = start_date + datetime.timedelta(60)
        print("Start: ", start_date, " End: ", end_date)
        url = 'https://kite.zerodha.com/oms/instruments/historical/' + ticker_id + '/' + num_minute_data
        url += 'minute?user_id=JB7207&oi=1&from=' +\
            str(start_date) + '&to=' + str(end_date)
        res = requests.get(url, headers = headers)
        json_data = json.loads(res.text)['data']['candles']
    
        for entry in json_data:
            date = entry[0]
            open_price = entry[1]
            high_price = entry[2]
            low_price = entry[3]
            close_price = entry[4]
            row = {'Date':date, 'Open':open_price, 'High':high_price, 'Low':low_price, 'Close':close_price}
            data.append(row)
        
        start_date = end_date + datetime.timedelta(1)
        
    df = pd.DataFrame(data)
    df.set_index('Date', inplace=True)
    df.to_excel(file_name)

def get_historical_daily_data(ticker_id, ticker_name, num_two_months):
    
    start_date = datetime.date.today()-datetime.timedelta(num_two_months*60)
    num_months = num_two_months * 2
    file_name = "1_YEAR_TICKER_DATA/" + ticker_name + "_" + str(num_months) + "_MONTH_DAILY_DATA.xlsx" 
    data = []
    for i in range(num_two_months):
        
        end_date = start_date + datetime.timedelta(60)
        print("Start: ", start_date, " End: ", end_date)
        url = 'https://kite.zerodha.com/oms/instruments/historical/' + ticker_id + '/'
        url += 'day?user_id=JB7207&oi=1&from=' +\
            str(start_date) + '&to=' + str(end_date)
        res = requests.get(url, headers = headers)
        json_data = json.loads(res.text)['data']['candles']
    
        for entry in json_data:
            date = entry[0]
            open_price = entry[1]
            high_price = entry[2]
            low_price = entry[3]
            close_price = entry[4]
            row = {'Date':date, 'Open':open_price, 'High':high_price, 'Low':low_price, 'Close':close_price}
            data.append(row)
        
        start_date = end_date + datetime.timedelta(1)
        
    df = pd.DataFrame(data)
    df.set_index('Date', inplace=True)
    df.to_excel(file_name)
    
def generate_5_minute_data(num_two_months):
    for ticker_id, ticker_name in name_zerodha_nse_id_dict.items():
        get_historical_data(ticker_id, ticker_name, num_two_months, "5")
        
def generate_10_minute_data(num_two_months):
    for ticker_id, ticker_name in name_zerodha_nse_id_dict.items():
        get_historical_data(ticker_id, ticker_name, num_two_months, "10")

def generate_15_minute_data(num_two_months):
    for ticker_id, ticker_name in name_zerodha_nse_id_dict.items():
        get_historical_data(ticker_id, ticker_name, num_two_months, "15")
        
def generate_daily_data(num_two_months):
    for ticker_id, ticker_name in buy_stocks_dict.items():
        get_historical_daily_data(ticker_id, ticker_name, num_two_months)
        
def generate_hourly_data(num_two_months):
    for ticker_id, ticker_name in name_zerodha_nse_id_dict.items():
        get_historical_data(ticker_id, ticker_name, num_two_months, "60")

def generate_half_hourly_data(num_two_months):
    for ticker_id, ticker_name in name_zerodha_nse_id_dict.items():
        get_historical_data(ticker_id, ticker_name, num_two_months, "30")


#generate_5_minute_data(18)
#generate_10_minute_data(6)
generate_daily_data(6)
#generate_hourly_data(6)
#generate_half_hourly_data(12)
#generate_15_minute_data(6)