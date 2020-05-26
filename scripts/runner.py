'''
@Author: Zuxin Liu
@Email: zuxinl@andrew.cmu.edu
@Date:   2020-05-25 21:31:49
@LastEditTime: 2020-05-25 22:17:58
@Description:
'''
#import warnings
#warnings.filterwarnings("ignore", category=UserWarning)
#warnings.filterwarnings("ignore", category=RuntimeWarning)
import numpy as np
import gym

from mpc.controllers import MPC
from mpc.models.dynamic_model import DynamicModel
from mpc.models.reward_model import RewardModel

def run(env, config, args):

	nn_config = config['NN_config']
	mpc_config = config['mpc_config']
	reward_config = config['reward_config']

	state_dim = env.observation_space.shape[0]
	action_dim = env.action_space.shape[0]
	action_low, action_high = env.action_space.low, env.action_space.high
	print("obs dim, act dim: ", state_dim, action_dim)
	print("act low high: ", action_low, action_high)
	nn_config["model_config"]["state_dim"] = state_dim
	nn_config["model_config"]["action_dim"] = action_dim
	reward_config["model_config"]["state_dim"] = state_dim
	reward_config["model_config"]["action_dim"] = action_dim
	optimizer_name = mpc_config["optimizer"]
	mpc_config[optimizer_name]["action_low"] = action_low
	mpc_config[optimizer_name]["action_high"] = action_high
	mpc_config[optimizer_name]["action_dim"] = action_dim

	model = DynamicModel(NN_config=nn_config)

	if args.use_reward_model:
		reward_config["model_config"]["load_model"] = True
		reward_model = RewardModel(reward_config=reward_config)
	else:
		reward_model = None

	# initial MPC controller
	mpc_controller = MPC(mpc_config=mpc_config, reward_model=reward_model)

	if args.train_reward_model:
		reward_model = RewardModel(reward_config=reward_config)
	"""NN pretrain"""
	pretrain_episodes = 40
	for epi in range(pretrain_episodes):
		obs = env.reset()
		done = False
		while not done:
			action = env.action_space.sample()
			obs_next, reward, done, state_next = env.step(action)
			model.add_data_point([0, obs, action, obs_next - obs])
			if args.train_reward_model: 
				reward_model.add_data_point([0, obs_next, action, [reward]])
			obs = obs_next
	# training the model
	model.fit()
	if args.train_reward_model:
		print("********** fitting reward model **********")
		reward_model.fit()

	"""testing the model with MPC while training """
	test_episode = 3
	test_epoch = 20
	
	for ep in range(test_epoch):
		print('epoch: ', ep)
		
		for epi in range(test_episode):
			obs = env.reset()
			acc_reward, done = 0, False
			mpc_controller.reset()
			i = 0
			while not done:
				i+= 1
				if args.render:
					env.render()
				action = np.array([mpc_controller.act(model=model, state=obs)])
				obs_next, reward, done, state_next = env.step(action)

				model.add_data_point([0, obs, action, obs_next - obs])
				if args.train_reward_model: 
					reward_model.add_data_point([0, obs_next, action, [reward]])

				obs = obs_next
				acc_reward += reward

			print('step: ', i, 'acc_reward: ', acc_reward)
			env.close()

			if done:
				print('******************')
				print('acc_reward', acc_reward)

		print('********** fitting the dynamic model **********')
		model.fit()
		if args.train_reward_model:
			print("********** fitting reward model **********")
			reward_model.fit()
