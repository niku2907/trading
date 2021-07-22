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

headers = {'authority':'kite.zerodha.com',\
           'accept':'application/json, text/plain, */*',\
           'authorization':'enctoken 5r8XZXo+mk3ZwtFfaFLXJC51UkD5yGa3IJSgPKgJ6+RkTuPoUxwpFWnn7wM8krHv6aTeT2NH5/zUJZIjtXxFdg8Q6bt4oXFKFx26wBYGH6AKYtsAxHlS+Q=='}

counter = 50

start_date = datetime.date.today()-datetime.timedelta(counter*60)

data = []
for i in range(counter):
    
    end_date = start_date + datetime.timedelta(60)
    print("Start: ", start_date, " End: ", end_date)
    url = 'https://kite.zerodha.com/oms/instruments/historical/260105/minute?user_id=JB7207&oi=1&from=' +\
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
df.to_excel("NIFTYBANK_HISTORICAL_DATA.xlsx")