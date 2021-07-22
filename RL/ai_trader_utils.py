#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 16:19:17 2020

@author: nishant.gupta
"""

import math
import numpy as np
import pandas_datareader.data as pdr

class model_params:
    def __init__(self, state_size, memory_width, gamma, epsilon, epsilon_final, epsilon_decay, input_units,\
                 hidden_layer1_units, hidden_layer2_units, activation_func, activation_func_output, loss_func,\
                 learning_rate, model_name):
        self.state_size = state_size
        self.memory_width = memory_width
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_final = epsilon_final
        self.epsilon_decay = epsilon_decay
        self.input_units = input_units
        self.hidden_layer1_units = hidden_layer1_units
        self.hidden_layer2_units = hidden_layer2_units
        self.activation_func = activation_func
        self.activation_func_output = activation_func_output
        self.loss_func = loss_func
        self.learning_rate = learning_rate
        self.model_name = model_name
       
class trader_result:
    def __init__(self, num_profit, num_loss, total_profit, num_buy, num_sell, total_investment):
        self.num_profit = num_profit
        self.num_loss = num_loss
        self.total_profit = total_profit
        self.num_buy = num_buy
        self.num_sell = num_sell
        self.total_investment = total_investment
        

class AI_trader_utils :
    def sigmoid(x):
        try:
            return 1 / (1 + math.exp(-x))
        except:
            print("Got error while sigmoid: ", x)
            return 0

    def dataset_loader(stock_name, start_date, end_date):
        dataset = pdr.get_data_yahoo(stock_name, start_date, end_date)
        close = dataset['Close']
        return close

    def state_creator(data, timestep, window_size):
        starting_id = timestep - window_size + 1
  
        if starting_id >= 0:
            windowed_data = data[starting_id:timestep+1]
        else:
            windowed_data = - starting_id * [data[0]] + list(data[0:timestep+1])
    
        state = []
        for i in range(window_size - 1):
            state.append(AI_trader_utils.sigmoid(windowed_data[i+1] - windowed_data[i]))
    
        return np.array([state])