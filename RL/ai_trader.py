#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 16:02:16 2020

@author: nishant.gupta
"""

import random
import numpy as np
import tensorflow as tf

from collections import deque

class AI_trader_model:
  def __init__(self, params):
    # Action space this model is Hold, Buy, Sell
    self.action_space = 3
    self.memory = deque(maxlen = params.memory_width)
    self.inventory = []
    self.params = params
    
    # Build the model
    self.model = self.model_builder()
    
  def model_builder(self):
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Dense(units = self.params.input_units, activation = self.params.activation_func,\
                                    input_dim = self.params.state_size))
    model.add(tf.keras.layers.Dense(units = self.params.hidden_layer1_units,\
                                    activation = self.params.activation_func))
    model.add(tf.keras.layers.Dense(units = self.params.hidden_layer1_units,\
                                    activation = self.params.activation_func))
    model.add(tf.keras.layers.Dense(units = self.action_space,\
                                    activation = self.params.activation_func_output))
    
    # Compile the model
    model.compile(loss = self.params.loss_func, optimizer = tf.keras.optimizers.Adam(lr = self.params.learning_rate))
    
    return model
  
  def trade(self, state):
    if random.random() <= self.params.epsilon:
      return random.randrange(self.action_space)
    
    actions = self.model.predict(state)
    return np.argmax(actions[0])
  
  
  def batch_train(self, batch_size):
    batch = []
    for i in range(len(self.memory) - batch_size + 1, len(self.memory)):
      batch.append(self.memory[i])
      
    for state, action, reward, next_state, done in batch:
      reward = reward
      if not done:
        reward = reward + self.params.gamma * np.amax(self.model.predict(next_state)[0])

      target = self.model.predict(state)
      target[0][action] = reward
      
      self.model.fit(state, target, epochs = 1, verbose = 0)
      
    if self.params.epsilon > self.params.epsilon_final:
      self.params.epsilon *= self.params.epsilon_decay