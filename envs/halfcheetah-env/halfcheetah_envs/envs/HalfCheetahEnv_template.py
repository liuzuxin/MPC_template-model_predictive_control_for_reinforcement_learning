'''
@Author: 
@Email: 
@Date: 2020-04-15 12:09:20
@LastEditTime: 2020-05-17 21:01:25
@Description: 
'''
import numpy as np
from gym import utils
from gym.envs.mujoco import mujoco_env

import os


class HalfCheetahEnv(mujoco_env.MujocoEnv, utils.EzPickle):
    def __init__(self, model_xml_path):
        root_path = os.path.abspath(os.path.dirname(__file__))
        model_xml_path = os.path.join(root_path, 'assets', model_xml_path)
        mujoco_env.MujocoEnv.__init__(self, model_xml_path, 4)  # original skip_frame = 5
        utils.EzPickle.__init__(self)

    def step(self, action):
        xposbefore = self.sim.data.qpos[0]
        self.do_simulation(action, self.frame_skip)
        xposafter = self.sim.data.qpos[0]
        ob = self._get_obs()
        reward_ctrl = - 0.1 * np.square(action).sum()
        reward_run = (xposafter - xposbefore)/self.dt
        reward = reward_ctrl + reward_run

        done = False
        return ob, reward, done, dict(reward_run=reward_run, reward_ctrl=reward_ctrl)

    def _get_obs(self):
        return np.concatenate([
            self.sim.data.qpos.flat, # qpos[0] is the xpos of body, which is used for computing reward
            self.sim.data.qvel.flat,
        ])

    def reset_model(self):
        qpos = self.init_qpos + self.np_random.uniform(low=-.1, high=.1, size=self.model.nq)
        qvel = self.init_qvel + self.np_random.randn(self.model.nv) * .1
        self.set_state(qpos, qvel)
        return self._get_obs()

    def viewer_setup(self):
        self.viewer.cam.distance = self.model.stat.extent * 0.5
