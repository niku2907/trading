#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 17:47:18 2020

@author: nishant.gupta
"""

from ai_trader import AI_trader_model
from ai_trader_utils import AI_trader_utils
from ai_trader_utils import trader_result
from model_trainer import model_trainer
from tqdm import tqdm

class model_tester:
    def __init__(self, ticker, episodes_used_for_training, window_size, batch_size, model_params,\
                 start_date_train, end_date_train, start_date_test, end_date_test):
        self.ticker = ticker
        self.window_size = window_size
        self.episodes_used_for_training = episodes_used_for_training
        self.batch_size = batch_size
        self.model_params = model_params
        
        # Train the model
        self.trader = AI_trader_model(model_params)
        self.trainer = model_trainer(trader = self.trader,\
                                     episodes = episodes_used_for_training,\
                                     window_size = window_size,\
                                     batch_size = batch_size,\
                                     ticker = ticker,\
                                     start_date = start_date_train,\
                                     end_date = end_date_train)
        self.start_date_test = start_date_test
        self.end_date_test = end_date_test
        self.trainer.train()
        
        
    def test(self):
        print("***********Starting the testing phase***********")
        data = AI_trader_utils.dataset_loader(self.ticker, self.start_date_test, self.end_date_test)
        data_samples = len(data) - 1
        print("Length: ", data_samples)
        state = AI_trader_utils.state_creator(data, 0, self.window_size + 1)
  
        total_profit = 0
        num_profit = 0
        num_loss = 0
        num_buy = 0
        num_sell = 0
        total_investment = 0
        for t in tqdm(range(data_samples)):
            action = self.trader.trade(state)
            next_state = AI_trader_utils.state_creator(data, t+1, self.window_size + 1)
            reward = 0
    
            if (action == 1): #Buying
                self.trader.inventory.append(data[t])
                print("[Tester] Bought at: ", data[t])
                total_investment += data[t]
                num_buy += 1
            elif (action == 2 and len(self.trader.inventory) > 0): #Selling
                buy_price = self.trader.inventory.pop(0)
                reward = max(data[t] - buy_price, 0)
                profit = data[t] = buy_price
                total_profit += profit
                num_sell += 1
                print("[Tester] Sold at: ", data[t])
                
                if (profit > 0):
                    print("[Tester] Made profit of: ", profit)
                    num_profit += 1
                else:
                    print("[Tester] Made loss of: ", profit)
                    num_loss += 1
                
            else:
                print("[Tester] ****Holding*****")
                
            if (t == data_samples - 1):
                done = True
            else:
                done = False
      
            # Append the state of tester in the memory of the trader's model
            self.trader.memory.append((state, action, reward, next_state, done))
    
            state = next_state
    
            if done:
                print("########################")
                print("[Tester] TOTAL PROFIT : {}".format(total_profit))
                print("########################")
    
            if len(self.trader.memory) > self.batch_size:
                self.trader.batch_train(self.batch_size)
        
        result = trader_result(num_profit = num_profit, num_loss = num_loss, total_profit = total_profit,\
                               num_buy = num_buy, num_sell = num_sell, total_investment = total_investment)
        return result