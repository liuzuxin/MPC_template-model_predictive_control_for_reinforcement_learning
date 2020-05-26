'''
@Author: 
@Email: 
@Date: 2020-03-23 00:00:07
@LastEditTime: 2020-05-17 20:31:12
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
max_episode_steps = 200

register(
    id='HalfCheetahSlope00-v1',
    entry_point='halfcheetah_envs.envs:HalfCheetahSlope00',
    max_episode_steps=max_episode_steps,
    reward_threshold=4800,
)

register(
    id='HalfCheetahSlope10-v1',
    entry_point='halfcheetah_envs.envs:HalfCheetahSlope10',
    max_episode_steps=max_episode_steps,
    reward_threshold=4800,
)

register(
    id='HalfCheetahSlope15-v1',
    entry_point='halfcheetah_envs.envs:HalfCheetahSlope15',
    max_episode_steps=max_episode_steps,
    reward_threshold=4800,
)


register(
    id='HalfCheetahSlope00m04-v1',
    entry_point='halfcheetah_envs.envs:HalfCheetahSlope00m04',
    max_episode_steps=max_episode_steps,
    reward_threshold=4800,
)

register(
    id='HalfCheetahSlope00m34-v1',
    entry_point='halfcheetah_envs.envs:HalfCheetahSlope00m34',
    max_episode_steps=max_episode_steps,
    reward_threshold=4800,
)
