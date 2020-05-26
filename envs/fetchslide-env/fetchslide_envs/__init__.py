'''
@Author: 
@Email: 
@Date: 2020-03-23 00:00:07
@LastEditTime: 2020-05-05 20:12:09
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


register(
    id='FetchSlideEnvm10f01-v1',
    entry_point='fetchslide_envs.envs:FetchSlideEnvm10f01',
    max_episode_steps=1000,
    reward_threshold=475.0,
)

register(
    id='FetchSlideEnvm20f01-v1',
    entry_point='fetchslide_envs.envs:FetchSlideEnvm20f01',
    max_episode_steps=1000,
    reward_threshold=475.0,
)

register(
    id='FetchSlideEnvm30f01-v1',
    entry_point='fetchslide_envs.envs:FetchSlideEnvm30f01',
    max_episode_steps=1000,
    reward_threshold=475.0,
)

register(
    id='FetchSlideEnvm40f01-v1',
    entry_point='fetchslide_envs.envs:FetchSlideEnvm40f01',
    max_episode_steps=1000,
    reward_threshold=475.0,
)


register(
    id='FetchSlideEnvm10f02-v1',
    entry_point='fetchslide_envs.envs:FetchSlideEnvm10f02',
    max_episode_steps=1000,
    reward_threshold=475.0,
)

register(
    id='FetchSlideEnvm10f03-v1',
    entry_point='fetchslide_envs.envs:FetchSlideEnvm10f03',
    max_episode_steps=1000,
    reward_threshold=475.0,
)

register(
    id='FetchSlideEnvm10f005-v1',
    entry_point='fetchslide_envs.envs:FetchSlideEnvm10f005',
    max_episode_steps=1000,
    reward_threshold=475.0,
)
