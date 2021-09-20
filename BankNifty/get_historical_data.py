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

headers = {'authority':'kite.zerodha.com',\
           'accept':'application/json, text/plain, */*',\
           'authorization':'enctoken PiOHzj5nRrJ5Js3vEZTDluqE0NJhrxk3LI3hQJ3NIMcAZQjpE53HYXzywzpNTAiDHX5h1S5vAZta5GdmAzGb54D6T10DVcC3tiZdz4IxJIGOCyN+6DVUzg=='}

def get_historical_data(ticker_id, ticker_name, num_two_months, num_minute_data):
    
    start_date = datetime.date.today()-datetime.timedelta(num_two_months*60)
    num_months = num_two_months * 2
    file_name = "Ticker_Data/" + ticker_name + "_" + str(num_months) + "_MONTH_" + num_minute_data +\
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


def generate_5_minute_data(num_two_months):
    for ticker_id, ticker_name in name_zerodha_nse_id_dict.items():
        get_historical_data(ticker_id, ticker_name, 1, "5")
        
    for ticker_id, ticker_name in name_zerodha_nse_id_realty_dict.items():
        get_historical_data(ticker_id, ticker_name, 1, "5")
        
    for ticker_id, ticker_name in name_zerodha_nse_id_it_dict.items():
        get_historical_data(ticker_id, ticker_name, 1, "5")
        
    for ticker_id, ticker_name in name_zerodha_nse_id_fmcg_dict.items():
        get_historical_data(ticker_id, ticker_name, 1, "5")

generate_5_minute_data(1)