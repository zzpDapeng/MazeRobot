#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : Dapeng
# @FileName: Maze.py
# @Fuction: 
# @Environment: 
# @Time    : 2020/5/27 19:01
import tkinter as tk
import numpy as np
import random
import time

PIXEL = 50

COIN_SCORE = 50
END_SCORE = 100
BLANK_SCORE = -1
WALL_SCORE = -5


class Maze(tk.Tk, object):

	def __init__(self,size):
		super(Maze, self).__init__()

		self.title("迷宫机器人")
		self.geometry('{0}x{0}'.format(PIXEL*size))

		self.size = size
		self.action_list = ['u','d','l','r']
		self.action_num = len(self.action_list)
		self.robot_location=np.array([0,0]) #机器人位置
		self.init_reward()

		# 调试不同迭代次数
		# self.reward=np.load('reward_5_1.npy')
		# self.rewarding = self.reward.copy()

		# 调试不同奖励参数
		# self.load_reward()

		self.coin_dict={} #硬币图id列表
		self.coin_list=[] #地图硬币列表
		self.wall_list=[] #地图墙列表

		self.init_maze()

	def mpath(self,maze, x1, y1, x2, y2):
		dirs = [lambda x, y: (x + 1, y),
				lambda x, y: (x - 1, y),
				lambda x, y: (x, y - 1),
				lambda x, y: (x, y + 1)]
		stack = []
		stack.append((x1, y1))
		while len(stack) > 0:
			curNode = stack[-1]
			if curNode[0] == x2 and curNode[1] == y2:
				# 到达终点
				# for p in stack:
				# 	print(p)
				return True
			for dir in dirs:
				nextNode = dir(curNode[0], curNode[1])
				if maze[nextNode[0]][nextNode[1]] == 0:
					# 找到了下一个
					stack.append(nextNode)
					maze[nextNode[0]][nextNode[1]] = -1  # 标记为已经走过，防止死循环
					break
			else:  # 四个方向都没找到
				maze[curNode[0]][curNode[1]] = -1  # 死路一条,下次别走了
				stack.pop()  # 回溯
		return False

	def init_reward(self):
		'''
		按量随机，数量稳定
		随机生成size*size大小的迷宫（二维矩阵）
		路-1
		起点：（0，0）
		终点100：（size-1，size-1）
		墙-5：随机（size+size/2个）
		硬币10：随机（size/2）
		:param size: 
		:return:
		'''
		connected = False

		while not connected:
			self.reward = np.zeros((self.size,self.size),dtype=int)
			# choosen = np.random.choice(range(1,self.size*self.size-1),self.size*2) # 可重复随机取
			choosen = np.array(random.sample(range(1,self.size*self.size-1),self.size*2)) # 不重复随机取
			self.coin_list = choosen[:int(self.size/2)]
			self.wall_list = choosen[int(self.size/2):]
			# print("choosen=",choosen)
			# print("wall=",self.wall_list.size)
			# print("coin=",self.coin_list.size)
			for x in range(self.size):
				for y in range(self.size):
					if self.coin_list.__contains__(x*self.size + y):
						self.reward[x][y] = COIN_SCORE
					elif self.wall_list.__contains__(x*self.size + y):
						self.reward[x][y] = WALL_SCORE
					elif x*self.size + y == self.size*self.size - 1:
						self.reward[x][y] = END_SCORE
					else:
						self.reward[x][y] = BLANK_SCORE
			self.rewarding=self.reward.copy()  #每个episode动态更新的reward
			np.save('reward_5_1.npy',self.reward)
			check = np.zeros((self.size + 2, self.size + 2))
			for x in range(self.size):
				for y in range(self.size):
					if self.reward[x][y] == BLANK_SCORE:
						check[x + 1][y + 1] = 0
					elif self.reward[x][y] == COIN_SCORE:
						check[x + 1][y + 1] = 0
					elif self.reward[x][y] == WALL_SCORE:
						check[x + 1][y + 1] = 1
					elif self.reward[x][y] == END_SCORE:
						check[x + 1][y + 1] = 0
			check[0] = 1
			check[self.size + 1] = 1
			check[:, 0] = 1
			check[:, self.size + 1] = 1
			connected = self.mpath(check, 1, 1, self.size, self.size)

		return True

	def load_reward(self):
		coin_score = 50
		end_score = 100
		blank_score = -1
		wall_score = -5
		self.reward=np.load('reward_8_1.npy')
		for x in range(self.size):
			for y in range(self.size):
				if self.reward[x][y]==coin_score:
					self.reward[x][y] = COIN_SCORE
				elif self.reward[x][y]==end_score:
					self.reward[x][y] = END_SCORE
				elif self.reward[x][y]==blank_score:
					self.reward[x][y] = BLANK_SCORE
				else:
					self.reward[x][y] = WALL_SCORE
		self.rewarding = self.reward.copy()

	def get_reward(self):
		return self.reward, self.coin_list, self.wall_list

	# def redraw(self):
	# 	for x in range(self.size):
	# 		for y in range(self.size):
	# 			# 起点
	# 			if x*self.size + y == 0:
	# 				self.robot = self.canvas.create_rectangle((y+0.1)*PIXEL,(x+0.1)*PIXEL,(y+0.9)*PIXEL,(x+0.9)*PIXEL,fill='red')
	# 			elif self.reward[x][y] == 10:
	# 				oval = self.canvas.create_oval((y+0.1)*PIXEL,(x+0.1)*PIXEL,(y+0.9)*PIXEL,(x+0.9)*PIXEL, fill='yellow')
	# 				self.coin_dict[(x,y)]=oval

	def init_maze(self):

		self.canvas = tk.Canvas(self, bg='white', height=PIXEL*self.size, width=PIXEL*self.size)
		# 迷宫网格
		for x in range(0,PIXEL*self.size,PIXEL):
			self.canvas.create_line(x,0,x,PIXEL*self.size)
		for y in range(0,PIXEL*self.size,PIXEL):
			self.canvas.create_line(0,y,PIXEL*self.size,y)

		# 填充起点、终点、硬币、墙
		for x in range(self.size):
			for y in range(self.size):
				# 起点
				if x*self.size + y == 0:
					self.robot = self.canvas.create_rectangle((y+0.1)*PIXEL,(x+0.1)*PIXEL,(y+0.9)*PIXEL,(x+0.9)*PIXEL,fill='red')
				# 终点
				elif self.reward[x][y] == END_SCORE:
					self.end = self.canvas.create_rectangle((y+0.1)*PIXEL,(x+0.1)*PIXEL,(y+0.9)*PIXEL,(x+0.9)*PIXEL,fill='green')
				# 墙
				elif self.reward[x][y] == WALL_SCORE:
					self.canvas.create_rectangle((y+0.1)*PIXEL,(x+0.1)*PIXEL,(y+0.9)*PIXEL,(x+0.9)*PIXEL, fill='black')
				# # 硬币
				# elif self.reward[x][y] == 10:
				# 	oval = self.canvas.create_oval((y+0.1)*PIXEL,(x+0.1)*PIXEL,(y+0.9)*PIXEL,(x+0.9)*PIXEL, fill='yellow')
				# 	self.coin_dict[(x,y)]=oval
		self.canvas.pack()

	def judge(self,action):
		'''
		判断对于当前robot_location执行动作action是否可行。（判断越界）
		:param action: 
		:return: 
		'''
		if (action == 'u' ) & (self.robot_location[0]== 0):
			return False
		elif (action == 'd' ) & (self.robot_location[0]==self.size-1):
			return False
		elif (action == 'l' ) & (self.robot_location[1]==0):
			return False
		elif (action == 'r' ) & (self.robot_location[1]==self.size-1):
			return False
		else:
			return True

	def restart(self):
		self.robot_location=[0,0]
		self.rewarding=self.reward.copy()
		# 删除起点和剩余硬币
		self.canvas.delete(self.robot)
		coin_view_list = list(self.coin_dict.values())
		for coin in coin_view_list:
			self.canvas.delete(coin)

		# 重画起点和硬币
		self.robot = self.canvas.create_rectangle((0.1)*PIXEL,(0.1)*PIXEL,(0.9)*PIXEL,(0.9)*PIXEL,fill='red')
		for x in range(self.size):
			for y in range(self.size):
				# 硬币
				if self.reward[x][y] == COIN_SCORE:
					oval = self.canvas.create_oval((y + 0.1) * PIXEL, (x + 0.1) * PIXEL, (y + 0.9) * PIXEL,
												   (x + 0.9) * PIXEL, fill='yellow')
					self.coin_dict[(x, y)] = oval
		return self.robot_location

	def step(self, action):
		'''
		
		:param action: 行动
		:return: 机器人下一位置self.robot_location， 奖励reward，是否结束done
		'''
		reward = 0
		done = False
		if self.judge(action):

			# s_ = self.robot_location
			s_ = self.robot_location.copy()

			move_pixel=[0,0]

			# 改变机器人位置robot_location，即s'
			if action=='u':
				s_[0] -= 1
				move_pixel[1] -= PIXEL
			elif action=='d':
				s_[0] += 1
				move_pixel[1] += PIXEL
			elif action=='l':
				s_[1] -= 1
				move_pixel[0] -= PIXEL
			elif action=='r':
				s_[1] += 1
				move_pixel[0] += PIXEL

			# 执行这一action获得的及时奖赏reward
			x = s_[0]
			y = s_[1]
			# print('方向：',action)
			# print('当前位置：', self.robot_location)
			# print('下一位置：',x,y)
			reward = self.rewarding[x][y]
			# print('reward=',reward,end='\n\n')

			# 捡到硬币则s'更新成功，更新rewarding表，删除硬币，从10改为-1
			if reward == COIN_SCORE:
				self.robot_location=s_[0:]
				self.canvas.delete(self.coin_dict[(x,y)])
				self.coin_dict.pop((x,y))
				self.canvas.move(self.robot,move_pixel[0],move_pixel[1])
				done=False
				self.rewarding[self.robot_location[0]][self.robot_location[1]]=BLANK_SCORE
			# 撞墙
			elif reward == WALL_SCORE:
				# 机器人位置不更新为s_  更新了？？
				done=False
			# 走到空白
			elif reward == BLANK_SCORE:
				self.robot_location=s_[0:]
				self.canvas.move(self.robot,move_pixel[0],move_pixel[1])
				done=False
			# 走到终点
			elif reward == END_SCORE:
				self.robot_location=s_[0:]
				self.canvas.move(self.robot,move_pixel[0],move_pixel[1])
				done=True
			else:
				raise Exception("Reward Error！")

		return self.robot_location, reward, done

	def render(self,progress):
		time.sleep(0.1*progress)
		self.update()

