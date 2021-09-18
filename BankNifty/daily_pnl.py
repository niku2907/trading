#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 09:55:38 2021

@author: nishant.gupta
"""
from util import util

buy_prices = [35425, 35490, 35522, 35518, 35549, 35653, 35690, 35641, 35704, 35716]
sell_prices = [35486, 35492, 35534, 35532, 35574, 35637, 35682, 35662, 35702, 35720]

total_pnl = 0
lot_size = 25
num_lots = 1
pnl_per_lot = 0
for i in range(len(buy_prices)):
    current_pnl = util.get_pnl(buy_prices[i], sell_prices[i], num_lots, lot_size)
    total_pnl += current_pnl
    pnl_per_lot += current_pnl / (num_lots * lot_size)
