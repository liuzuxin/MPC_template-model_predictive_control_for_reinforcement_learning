'''
@Author: Zuxin Liu
@Email: 
@Date: 2020-04-01 01:26:48
@LastEditTime: 2020-05-25 22:12:51
@Description: 
'''

import os, sys, yaml
#import warnings
#warnings.filterwarnings("ignore", category=UserWarning)
#warnings.filterwarnings("ignore", category=RuntimeWarning)

import numpy as np
import gym
import argparse

sys.path.append('../envs/cartpole-envs')
sys.path.append('../')
import cartpole_envs
import runner

def prepare_dynamics(gym_config):
    dynamics_name = gym_config['dynamics_name']
    seed = gym_config['seed']
    dynamics_set = []
    for i in range(len(dynamics_name)):
        env = gym.make(dynamics_name[i])
        # env.seed(seed)
        dynamics_set.append(gym.make(dynamics_name[i]))
    
    # use pre-defined env sequence
    task = [dynamics_set[i] for i in gym_config['task_dynamics_list']]
    return task

def load_config(config_path="config.yml"):
    if os.path.isfile(config_path):
        f = open(config_path)
        return yaml.load(f, Loader=yaml.FullLoader)
    else:
        raise Exception("Configuration file is not found in the path: "+config_path)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--use_reward_model', type=int, default=0)
    parser.add_argument('--train_reward_model', type=int, default=0)
    parser.add_argument('--render', type=int, default=1)
    args = parser.parse_args()

    config = load_config('../config/config.yml')
    
    # prepare task
    gym_config = config['gym_config']
    task = prepare_dynamics(gym_config)
    env = task[0]
    print("Pole length for this env: ", task[0].l)   

    runner.run(env, config, args)
