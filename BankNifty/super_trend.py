#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 17 19:21:24 2021

@author: nishant.gupta
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from math import floor
from termcolor import colored as cl

from add_stats import add_stats
from data_reader import data_reader 
from util import util

ema_period = 50
five_minute_data = data_reader.read("NIFTYBANK_ONE_MONTH_15_MINUTE_DATA.xlsx")
five_minute_data = add_stats.ema(five_minute_data, ema_period)

five_minute_data['st'], five_minute_data['st_upt'], five_minute_data['st_dt'] = \
    add_stats.get_supertrend(five_minute_data['High'], five_minute_data['Low'],
                   five_minute_data['Close'], 10, 3)

five_minute_data = five_minute_data[1:]

plt.plot(five_minute_data['Close'], linewidth = 2, label = 'CLOSING PRICE')
plt.plot(five_minute_data['st'], color = 'green', linewidth = 2,\
         label = 'ST UPTREND 10,3')
plt.plot(five_minute_data['st_dt'], color = 'r', linewidth = 2,\
         label = 'ST DOWNTREND 10,3')
plt.legend(loc = 'upper left')
plt.show()



five_minute_data['buy_price'], five_minute_data['sell_price'], five_minute_data['signal'] =\
    add_stats.implement_st_strategy(five_minute_data['Close'], five_minute_data['st'])
    
# SUPERTREND SIGNALS

plt.plot(five_minute_data['Close'], linewidth = 2)
plt.plot(five_minute_data['st'], color = 'green', linewidth = 2, label = 'ST UPTREND')
plt.plot(five_minute_data['st_dt'], color = 'r', linewidth = 2, label = 'ST DOWNTREND')
plt.plot(five_minute_data.index, five_minute_data['buy_price'], marker = '^',\
         color = 'green', markersize = 12, linewidth = 0, label = 'BUY SIGNAL')
plt.plot(five_minute_data.index, five_minute_data['sell_price'], marker = 'v',\
         color = 'r', markersize = 12, linewidth = 0, label = 'SELL SIGNAL')
plt.title('five_minute_data ST TRADING SIGNALS')
plt.legend(loc = 'upper left')
plt.show()