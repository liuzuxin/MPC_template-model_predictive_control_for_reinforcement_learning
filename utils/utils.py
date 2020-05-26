'''
@Author: Zuxin Liu
@Email: zuxinl@andrew.cmu.edu
@Date:   2020-03-24 01:01:29
@LastEditTime: 2020-03-24 11:05:41
@Description:
'''

import torch
import os
import yaml
import numpy as np
import matplotlib.pyplot as plt
import torch.utils.data as data
from tqdm import tqdm
'''
for i in range(1):
    arg_dict = {}
    arg_dict["env"] = "PendulumEnv"
    arg_dict["dim_in"] = 4
    arg_dict["dim_out"] = 2
    arg_dict["dim_states"] = 2
    arg_dict["dim_actions"] = 1
    arg_dict["dim_angles"] = 1
    arg_dict["target_reward"] = -0.08
    training_envs, test_envs = get_envs(**arg_dict)

    state space shape:  (3,)
    state space lower bound:  [ -1.  -1. -20.]
    state space upper bound:  [ 1.  1. 20.]
    action space shape:  (1,)
    action space lower bound:  [-2.]
    action space upper bound:  [2.]
    reward range:  (-inf, inf)
    Randomly sample actions for 200 episodes, with maximum 1000 steps per episodes
     average reward per episode: -916.5413219987428, std: 38.92018114891107 
     average steps per episode:  1000.0
     average reward per step:  -0.9165413219987428
'''


def warm_up(env, episodes=100, max_step = 200, render=False):
    """
    Collect training dynamic data from random policy

    Parameters:
    ----------
        @param object - env : gym env object
        @param int - episodes : determine how many episodes data to collect
        @param int - max_step : max steps for each episode
        @param bool - render : render the env

    Return:
    ----------
        @param list of numpy array - state_action_pairs : list of training data (state + action)
        @param list of numpy array - delta_states : list of label (next_state - state)
    """
    state_action_pairs, delta_states = [], []
    training_set = []
    state = env.reset()
    if render:
        env.render()
    for epi in tqdm(range(episodes)):
        for step in range(max_step):
            action = env.action_space.sample()
            state_next, reward, done, _ = env.step(action)
            state_action_pair = np.concatenate((state, action))
            delta_state = state_next-state
            state_action_pairs.append(state_action_pair)
            delta_states.append(delta_state)
            state = state_next
            if render:
                env.render()

    return state_action_pairs, delta_states

class MyDataset(data.Dataset):
    def __init__(self, datas, labels):
        self.datas = torch.tensor(datas)
        self.labels = torch.tensor(labels)

    def __getitem__(self, index):  # return tensor
        datas, target = self.datas[index], self.labels[index]
        return datas, target

    def __len__(self):
        return len(self.datas)

def load_config(config_path="config.yml"):
    if os.path.isfile(config_path):
        f = open(config_path)
        return yaml.load(f, Loader=yaml.FullLoader)
    else:
        raise Exception("Configuration file is not found in the path: "+config_path)

def print_config(config_path="config.yml"):
    if os.path.isfile(config_path):
        f = open(config_path)
        config = yaml.load(f)
        print("************************")
        print("*** model configuration ***")
        print(yaml.dump(config["model_config"], default_flow_style=False, default_style=''))
        print("*** train configuration ***")
        print(yaml.dump(config["training_config"], default_flow_style=False, default_style=''))
        print("************************")
        print("*** dataset configuration ***")
        print(yaml.dump(config["dataset_config"], default_flow_style=False, default_style=''))
        print("************************")
        print("*** MPC controller configuration ***")
        print(yaml.dump(config["mpc_config"], default_flow_style=False, default_style=''))
    else:
        raise Exception("Configuration file is not found in the path: "+config_path)

def anylize_env(env, test_episodes = 100,max_episode_step = 500, render = False):
    print("state space shape: ", env.observation_space.shape)
    print("state space lower bound: ", env.observation_space.low)
    print("state space upper bound: ", env.observation_space.high)
    print("action space shape: ", env.action_space.shape)
    print("action space lower bound: ", env.action_space.low)
    print("action space upper bound: ", env.action_space.high)
    print("reward range: ", env.reward_range)
    rewards = []
    steps = []
    for episode in range(test_episodes):
        env.reset()
        step = 0
        episode_reward = 0
        for _ in range(max_episode_step):
            if render:
                env.render()
            step += 1
            action = env.action_space.sample()
            next_state, reward, done, _ = env.step(action)
            episode_reward += reward
            if done:
               # print("done with step: %s " % (step))
                break
        steps.append(step)
        rewards.append(episode_reward)
    env.close()
    print("Randomly sample actions for %s episodes, with maximum %s steps per episodes"
          % (test_episodes, max_episode_step))
    print(" average reward per episode: %s, std: %s " % (np.mean(rewards), np.std(rewards) ))
    print(" average steps per episode: ", np.mean(steps))
    print(" average reward per step: ", np.sum(rewards)/np.sum(steps))

def min_max_scaler(d_in):  # scale the data to the range [0,1]
    d_max = np.max(d_in)
    d_min = np.min(d_in)
    d_out = (d_in - d_min) / (d_max - d_min)
    return d_out, d_min, d_max


