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
from zerodha_ticker_id import shortlisted_tickers_dict
from zerodha_ticker_id import buy_stocks_dict
from zerodha_ticker_id import sell_stocks_dict
from zerodha_ticker_id import mid_cap_stocks_dict
from zerodha_ticker_id import mid_cap_sell_stocks_dict
from zerodha_ticker_id import next_fifty_stocks_dict
from zerodha_ticker_id import buy_stocks_dict_low_capital
from zerodha_ticker_id import sell_stocks_dict_low_capital
from zerodha_ticker_id import sell_stocks_dict_low_capital_new
from zerodha_ticker_id import name_zerodha_nse_fno_dict
from zerodha_ticker_id import fno_shortlists_dict
from zerodha_ticker_id import current_stocks_dict

all_stocks_dict = {**name_zerodha_nse_id_dict, **mid_cap_stocks_dict, **next_fifty_stocks_dict}

headers = {'authority':'kite.zerodha.com',\
           'accept':'application/json, text/plain, */*',\
           'authorization':'enctoken 3bIXBTeHv1hYogAUPAwVXzZfi8N2F/QFj5bRzDX1Ocg85pBHUboTmp7WBC1bSHIBViYaPG2at0eqglnO3crte5sLICOiK9BwLbAIxbix9SBXSYhubdHZPQ=='}

def get_file_name(ticker_name, num_two_months, num_minute_data):
    prev_num_years = (num_two_months * 2) / 12
    file_prefix = str(int(prev_num_years)) + "_YEAR_TICKER_DATA/"
    file_name = file_prefix + ticker_name + "_" + str(num_two_months * 2) + "_MONTH_"
    if (num_minute_data != -1):
        file_name += num_minute_data + "_MINUTE_DATA.xlsx"
    else:
        file_name += "DAILY_DATA.xlsx"
    return file_name

def get_historical_data(ticker_id, ticker_name, num_two_months, num_minute_data):
    
    start_date = datetime.date.today()-datetime.timedelta(num_two_months*60)
    file_name = get_file_name(ticker_name, num_two_months, num_minute_data) 
    data = []
    print("*********Minute Ticker: ", ticker_name)
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
    file_name = get_file_name(ticker_name, num_two_months, num_minute_data = -1) 
    data = []
    print("*********Daily TIcker: ", ticker_name)
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
    for ticker_id, ticker_name in current_stocks_dict.items():
        get_historical_data(ticker_id, ticker_name, num_two_months, "5")
        
# def generate_10_minute_data(num_two_months):
#     for ticker_id, ticker_name in buy_stocks_dict_low_capital.items():
#         get_historical_data(ticker_id, ticker_name, num_two_months, "10")

def generate_15_minute_data(num_two_months):
    for ticker_id, ticker_name in current_stocks_dict.items():
        get_historical_data(ticker_id, ticker_name, num_two_months, "15")
        
def generate_daily_data(num_two_months):
    for ticker_id, ticker_name in current_stocks_dict.items():
        get_historical_daily_data(ticker_id, ticker_name, num_two_months)
        
def generate_hourly_data(num_two_months):
    for ticker_id, ticker_name in current_stocks_dict.items():
        get_historical_data(ticker_id, ticker_name, num_two_months, "60")

# def generate_half_hourly_data(num_two_months):
#     for ticker_id, ticker_name in buy_stocks_dict_low_capital.items():
#         get_historical_data(ticker_id, ticker_name, num_two_months, "30")


generate_5_minute_data(24)
generate_daily_data(24)
generate_hourly_data(24)
#generate_15_minute_data(6)