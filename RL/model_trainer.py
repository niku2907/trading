#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 17:19:09 2020

@author: nishant.gupta
"""

from ai_trader_utils import AI_trader_utils
from tqdm import tqdm

class model_trainer:
    def __init__(self, trader, episodes, window_size, batch_size, ticker, start_date, end_date):
        self.trader = trader
        self.episodes = episodes
        self.window_size = window_size
        self.batch_size = batch_size
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        
    def train(self):
        data = AI_trader_utils.dataset_loader(self.ticker, self.start_date, self.end_date)
        data_samples = len(data) - 1
        for episode in range(1, self.episodes + 1):
            print("[Trainer] Episode: {}/{}".format(episode, self.episodes))
            state = AI_trader_utils.state_creator(data, 0, (self.window_size) + 1)
  
            total_profit = 0
            self.trader.inventory = []
  
            for t in tqdm(range(data_samples)):
                action = self.trader.trade(state)
                next_state = AI_trader_utils.state_creator(data, t+1, (self.window_size) + 1)
                reward = 0
    
                if (action == 1): #Buying
                    self.trader.inventory.append(data[t])
                    print("[Trainer] Bought at: ", data[t])
                elif (action == 2 and len(self.trader.inventory) > 0): #Selling
                    buy_price = self.trader.inventory.pop(0)
                    reward = max(data[t] - buy_price, 0)
                    profit = data[t] = buy_price
                    total_profit += profit
                    print("[Trainer] Sold at: ", data[t])
                
                    if (profit > 0):
                        print("[Trainer] Made profit of: ", profit)
                    else:
                        print("[Trainer] Made loss of: ", profit)
                
                else:
                    print("[Trainer] ****Holding*****")
                
                if (t == data_samples - 1):
                    done = True
                else:
                    done = False
      
                self.trader.memory.append((state, action, reward, next_state, done))
    
                state = next_state
    
                if done:
                    print("########################")
                    print("[Trainer] TOTAL PROFIT : {}".format(total_profit))
                    print("########################")
    
                if len(self.trader.memory) > self.batch_size:
                    self.trader.batch_train(self.batch_size)
      
                if episode % 10 == 0:
                    self.trader.model.save("ai_trader_{}_{}.h5".format(self.ticker, episode))