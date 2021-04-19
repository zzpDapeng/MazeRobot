#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : Dapeng
# @FileName: Run.py
# @Fuction: 
# @Environment: 
# @Time    : 2020/5/27 19:01
import Maze
import Robot
import matplotlib.pyplot as plt

SIZE = 5
EPISODE =100

def update():
	reward_list = []
	delta_q_list = []
	for episode in range(EPISODE):
		print('episode ',episode)
		s =env.restart()
		all_reward=0
		all_q=0
		while True:
			x = episode / EPISODE
			# 延迟刷新界面

			# 慢速模式
			# env.render(1)

			# 匀加速模式
			# env.render(x)

			# 变减速模式
			env.render(1-(1-x**2)**0.5)

			# 极速模式
			# env.render(0)

			action = robot.epsilon_greedy_policy(s,x)

			s_, reward, done = env.step(action)

			all_reward+=reward

			all_q += robot.learn(s,action,reward,s_)

			s = s_

			if all_reward<-2000:
				done =True

			if done:
				print("reward:",all_reward)
				reward_list.append(all_reward)
				delta_q_list.append(all_q)
				# print('Q:\n',robot.Q_table)
				break
	plt.subplot(2,1,1)
	plt.ylabel('reward')
	plt.plot(range(len(reward_list)), reward_list)
	plt.subplot(2, 1, 2)
	plt.xlabel('episode')
	plt.ylabel('△Q')
	plt.plot(range(len(delta_q_list)), delta_q_list)
	plt.show()


if __name__ == '__main__':
	env =Maze.Maze(SIZE)
	robot = Robot.Robot(env)
	env.after(100,update)
	env.mainloop()