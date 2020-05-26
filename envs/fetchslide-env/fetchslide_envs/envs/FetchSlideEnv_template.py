'''
@Author: Wenhao Ding
@Email: wenhaod@andrew.cmu.edu
@Date: 2020-04-15 12:09:20
@LastEditTime: 2020-04-29 01:22:08
@Description: 
    Original version from: 
        https://github.com/openai/gym/blob/master/gym/envs/robotics/fetch/slide.py
    The reference for XML file:
        http://www.mujoco.org/book/XMLreference.html
'''

import numpy as np
import logging
import os

from gym import utils
#from gym.envs.robotics import fetch_env
from .fetch_env import FetchEnv

logger = logging.getLogger(__name__)


class FetchSlideEnv_template(FetchEnv, utils.EzPickle):
    def __init__(self, reward_type='sparse', model_xml_path='slide_m20f10.xml'):
        root_path = os.path.abspath(os.path.dirname(__file__))
        model_xml_path = os.path.join(root_path, 'assets', model_xml_path)
        initial_qpos = {
            'robot0:slide0': 0.4,
            'robot0:slide1': 0.48,
            'robot0:slide2': 0.0,
            # position and rotation of the object
            # The first 3 are the position and the next 4 are the rotation quaternion.
            'object0:joint': [1.7, 1.1, 0.41, 1., 0., 0., 0.],
        }

        FetchEnv.__init__(
            self, model_xml_path, has_object=True, block_gripper=True, n_substeps=20,
            initial_object_vel=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 
            gripper_extra_height=-0.02, target_in_the_air=False, 
            object_offset=np.array([0.0, -0.1, 0.0]), target_offset=np.array([0.0, -0.6, 0.0]),
            obj_range=0.00, target_range=0.00, distance_threshold=0.05,
            initial_qpos=initial_qpos, reward_type=reward_type)
        utils.EzPickle.__init__(self)
