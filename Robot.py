#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : Dapeng
# @FileName: Robot.py
# @Fuction: 
# @Environment: 
# @Time    : 2020/5/27 19:01
import numpy as np
import random


class Robot:

	def __init__(self, env, Eta=0.9, Gamma=0.9):
		self.env = env
		self.size = env.size
		self.action_num = 4
		self.Eta = Eta
		self.Gamma = Gamma
		self.Q_table = np.zeros((self.size, self.size, self.action_num))

	def epsilon_greedy_policy(self,state,epsilon):
		if random.uniform(0,1) < epsilon:
			x=state[0]
			y=state[1]
			action_index = np.argmax(self.Q_table[x][y])
			return self.env.action_list[action_index]
		else:
			rand_index = random.randint(0,3)
			return self.env.action_list[rand_index]

	def learn(self, state, action, reward, state_):
		x = state[0]
		y = state[1]
		x_ = state_[0]
		y_ = state_[1]

		action_index = self.env.action_list.index(action)

		Q = self.Q_table[x][y][action_index]

		action_index_ = np.argmax(self.Q_table[x_][y_])
		Q_ = self.Q_table[x_][y_][action_index_]

		self.Q_table[x][y][action_index] = Q + self.Eta * (reward + self.Gamma * Q_ - Q)

		return Q_-Q
