#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 17 19:21:24 2021

@author: nishant.gupta
"""

from add_stats import add_stats
from data_reader import data_reader 
from util import util
from super_trend_utils import super_trend_utils

ema_period = 50
have_cut_off_time_check = 0
five_minute_data = data_reader.read("AXIS_TWO_MONTH_5_MINUTE_DATA.xlsx")
five_minute_data = add_stats.ema(five_minute_data, ema_period)

five_minute_data['st'], five_minute_data['st_upt'], five_minute_data['st_dt'] = \
    super_trend_utils.get_supertrend(five_minute_data['High'], five_minute_data['Low'],
                   five_minute_data['Close'], 10, 3)

five_minute_data = five_minute_data[1:]

total_pnl, five_minute_data['Status'], five_minute_data['Signal'] = \
    super_trend_utils.implement_st_strategy(five_minute_data, have_cut_off_time_check)
    
super_trend_utils.plot_super_trend_band(five_minute_data)