'''
@Author: 
@Email: 
@Date: 2020-03-23 00:00:07
@LastEditTime: 2020-05-16 20:21:25
@Description:
'''

import logging
from gym.envs.registration import register
import inspect
import gym
import os

'''
# copy xml files to gym path
gym_path = os.path.dirname(inspect.getfile(gym))
gym_fetch_path = os.path.join(gym_path, 'envs/robotics/assets/fetch')
xml_path = os.path.abspath(os.path.dirname(__file__)) + '/envs/assets/'
print('copy .xml files to gym package')
print('from ', xml_path)
print('to', gym_fetch_path)

cmd = 'cp ' + xml_path + '* ' + gym_fetch_path
os.system(cmd)
'''


logger = logging.getLogger(__name__)
max_episode_steps = 400

register(
    id='Hopperm00-v1',
    entry_point='hopper_envs.envs:Hopperm00',
    max_episode_steps=max_episode_steps,
    reward_threshold=4800,
)
