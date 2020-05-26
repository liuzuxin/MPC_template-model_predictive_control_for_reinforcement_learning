'''
@Author: Mengdi Xu
@Email: 
@Date: 2020-03-23 00:00:07
@LastEditTime: 2020-04-15 22:32:41
@Description:
'''

import logging
from gym.envs.registration import register

logger = logging.getLogger(__name__)

"""Carpole SwingUp"""


register(
    id='CartPoleSwingUpEnvCm05Pm04Pl05-v0',
    entry_point='cartpole_envs.envs:CartPoleSwingUpEnvCm05Pm04Pl05',
    max_episode_steps=500,
    reward_threshold=475.0,
)
register(
    id='CartPoleSwingUpEnvCm05Pm04Pl07-v0',
    entry_point='cartpole_envs.envs:CartPoleSwingUpEnvCm05Pm04Pl07',
    max_episode_steps=500,
    reward_threshold=475.0,
)

register(
    id='CartPoleSwingUpEnvCm05Pm06Pl05-v0',
    entry_point='cartpole_envs.envs:CartPoleSwingUpEnvCm05Pm06Pl05',
    max_episode_steps=500,
    reward_threshold=475.0,
)
register(
    id='CartPoleSwingUpEnvCm05Pm06Pl07-v0',
    entry_point='cartpole_envs.envs:CartPoleSwingUpEnvCm05Pm06Pl07',
    max_episode_steps=500,
    reward_threshold=475.0,
)

register(
    id='CartPoleSwingUpEnvCm05Pm08Pl05-v0',
    entry_point='cartpole_envs.envs:CartPoleSwingUpEnvCm05Pm08Pl05',
    max_episode_steps=500,
    reward_threshold=475.0,
)
register(
    id='CartPoleSwingUpEnvCm05Pm08Pl07-v0',
    entry_point='cartpole_envs.envs:CartPoleSwingUpEnvCm05Pm08Pl07',
    max_episode_steps=500,
    reward_threshold=475.0,
)

###########


register(
    id='CartPoleSwingUpEnvCm05Pm05Pl05-v0',
    entry_point='cartpole_envs.envs:CartPoleSwingUpEnvCm05Pm05Pl05',
    max_episode_steps=500,
    reward_threshold=475.0,
)
register(
    id='CartPoleSwingUpEnvCm05Pm07Pl07-v0',
    entry_point='cartpole_envs.envs:CartPoleSwingUpEnvCm05Pm07Pl07',
    max_episode_steps=500,
    reward_threshold=475.0,
)


register(
    id='CartPoleSwingUpEnvCm05Pm10Pl05-v0',
    entry_point='cartpole_envs.envs:CartPoleSwingUpEnvCm05Pm10Pl05',
    max_episode_steps=500,
    reward_threshold=475.0,
)
register(
    id='CartPoleSwingUpEnvCm10Pm05Pl05-v0',
    entry_point='cartpole_envs.envs:CartPoleSwingUpEnvCm10Pm05Pl05',
    max_episode_steps=500,
    reward_threshold=475.0,
)


register(
    id='CartPoleSwingUpEnvCm10Pm07Pl07-v0',
    entry_point='cartpole_envs.envs:CartPoleSwingUpEnvCm10Pm07Pl07',
    max_episode_steps=500,
    reward_threshold=475.0,
)
register(
    id='CartPoleSwingUpEnvCm10Pm10Pl05-v0',
    entry_point='cartpole_envs.envs:CartPoleSwingUpEnvCm10Pm10Pl05',
    max_episode_steps=500,
    reward_threshold=475.0,
)

register(
    id='CartPoleSwingUpEnvCm10Pm05Pl10-v0',
    entry_point='cartpole_envs.envs:CartPoleSwingUpEnvCm10Pm05Pl10',
    max_episode_steps=500,
    reward_threshold=475.0,
)
register(
    id='CartPoleSwingUpEnvCm05Pm05Pl10-v0',
    entry_point='cartpole_envs.envs:CartPoleSwingUpEnvCm05Pm05Pl10',
    max_episode_steps=500,
    reward_threshold=475.0,
)

register(
    id='CartPoleSwingUpEnvCm10Pm02Pl10-v0',
    entry_point='cartpole_envs.envs:CartPoleSwingUpEnvCm10Pm02Pl10',
    max_episode_steps=500,
    reward_threshold=475.0,
)
register(
    id='CartPoleSwingUpEnvCm20Pm02Pl10-v0',
    entry_point='cartpole_envs.envs:CartPoleSwingUpEnvCm20Pm02Pl10',
    max_episode_steps=500,
    reward_threshold=475.0,
)

register(
    id='CartPoleSwingUpEnvCm20Pm01Pl05-v0',
    entry_point='cartpole_envs.envs:CartPoleSwingUpEnvCm20Pm01Pl05',
    max_episode_steps=500,
    reward_threshold=475.0,
)
register(
    id='CartPoleSwingUpEnvCm10Pm01Pl05-v0',
    entry_point='cartpole_envs.envs:CartPoleSwingUpEnvCm10Pm01Pl05',
    max_episode_steps=500,
    reward_threshold=475.0,
)

"""CartPole Stability"""
register(
    id='CartPoleEnvPoleM10l05-v0',
    entry_point='cartpole_envs.envs:CartPoleEnvPoleM10l05',
    max_episode_steps=500,
    reward_threshold=475.0,
)

register(
    id='CartPoleEnvPoleM10l10-v0',
    entry_point='cartpole_envs.envs:CartPoleEnvPoleM10l10',
    max_episode_steps=500,
    reward_threshold=475.0,
)

register(
    id='CartPoleEnvPoleM10l15-v0',
    entry_point='cartpole_envs.envs:CartPoleEnvPoleM10l15',
    max_episode_steps=500,
    reward_threshold=475.0,
)

register(
    id='CartPoleEnvPoleM20l05-v0',
    entry_point='cartpole_envs.envs:CartPoleEnvPoleM20l05',
    max_episode_steps=500,
    reward_threshold=475.0,
)

register(
    id='CartPoleEnvPoleM20l10-v0',
    entry_point='cartpole_envs.envs:CartPoleEnvPoleM20l10',
    max_episode_steps=500,
    reward_threshold=475.0,
)

register(
    id='CartPoleEnvPoleM20l15-v0',
    entry_point='cartpole_envs.envs:CartPoleEnvPoleM20l15',
    max_episode_steps=500,
    reward_threshold=475.0,
)

register(
    id='CartPoleEnvPoleM01l05-v0',
    entry_point='cartpole_envs.envs:CartPoleEnvPoleM01l05',
    max_episode_steps=500,
    reward_threshold=475.0,
)

register(
    id='CartPoleEnvPoleM01l07-v0',
    entry_point='cartpole_envs.envs:CartPoleEnvPoleM01l07',
    max_episode_steps=500,
    reward_threshold=475.0,
)

register(
    id='CartPoleEnvPoleM04l04-v0',
    entry_point='cartpole_envs.envs:CartPoleEnvPoleM04l04',
    max_episode_steps=500,
    reward_threshold=475.0,
)

register(
    id='CartPoleEnvPoleM04l05-v0',
    entry_point='cartpole_envs.envs:CartPoleEnvPoleM04l05',
    max_episode_steps=500,
    reward_threshold=475.0,
)

register(
    id='CartPoleEnvPoleM04l06-v0',
    entry_point='cartpole_envs.envs:CartPoleEnvPoleM04l06',
    max_episode_steps=500,
    reward_threshold=475.0,
)

register(
    id='CartPoleEnvPoleM04l07-v0',
    entry_point='cartpole_envs.envs:CartPoleEnvPoleM04l07',
    max_episode_steps=500,
    reward_threshold=475.0,
)



register(
    id='CartPoleEnvPoleM06l04-v0',
    entry_point='cartpole_envs.envs:CartPoleEnvPoleM06l04',
    max_episode_steps=500,
    reward_threshold=475.0,
)

register(
    id='CartPoleEnvPoleM06l05-v0',
    entry_point='cartpole_envs.envs:CartPoleEnvPoleM06l05',
    max_episode_steps=500,
    reward_threshold=475.0,
)

register(
    id='CartPoleEnvPoleM06l06-v0',
    entry_point='cartpole_envs.envs:CartPoleEnvPoleM06l06',
    max_episode_steps=500,
    reward_threshold=475.0,
)

register(
    id='CartPoleEnvPoleM06l07-v0',
    entry_point='cartpole_envs.envs:CartPoleEnvPoleM06l07',
    max_episode_steps=500,
    reward_threshold=475.0,
)




register(
    id='CartPoleEnvPoleM07l04-v0',
    entry_point='cartpole_envs.envs:CartPoleEnvPoleM07l04',
    max_episode_steps=500,
    reward_threshold=475.0,
)

register(
    id='CartPoleEnvPoleM07l05-v0',
    entry_point='cartpole_envs.envs:CartPoleEnvPoleM07l05',
    max_episode_steps=500,
    reward_threshold=475.0,
)

register(
    id='CartPoleEnvPoleM07l06-v0',
    entry_point='cartpole_envs.envs:CartPoleEnvPoleM07l06',
    max_episode_steps=500,
    reward_threshold=475.0,
)

register(
    id='CartPoleEnvPoleM07l07-v0',
    entry_point='cartpole_envs.envs:CartPoleEnvPoleM07l07',
    max_episode_steps=500,
    reward_threshold=475.0,
)



register(
    id='CartPoleEnvPoleM08l04-v0',
    entry_point='cartpole_envs.envs:CartPoleEnvPoleM08l04',
    max_episode_steps=500,
    reward_threshold=475.0,
)

register(
    id='CartPoleEnvPoleM08l05-v0',
    entry_point='cartpole_envs.envs:CartPoleEnvPoleM08l05',
    max_episode_steps=500,
    reward_threshold=475.0,
)

register(
    id='CartPoleEnvPoleM08l06-v0',
    entry_point='cartpole_envs.envs:CartPoleEnvPoleM08l06',
    max_episode_steps=500,
    reward_threshold=475.0,
)

register(
    id='CartPoleEnvPoleM08l07-v0',
    entry_point='cartpole_envs.envs:CartPoleEnvPoleM08l07',
    max_episode_steps=500,
    reward_threshold=475.0,
)




register(
    id='CartPoleEnvPoleM09l04-v0',
    entry_point='cartpole_envs.envs:CartPoleEnvPoleM09l04',
    max_episode_steps=500,
    reward_threshold=475.0,
)

register(
    id='CartPoleEnvPoleM09l05-v0',
    entry_point='cartpole_envs.envs:CartPoleEnvPoleM09l05',
    max_episode_steps=500,
    reward_threshold=475.0,
)

register(
    id='CartPoleEnvPoleM09l06-v0',
    entry_point='cartpole_envs.envs:CartPoleEnvPoleM09l06',
    max_episode_steps=500,
    reward_threshold=475.0,
)

register(
    id='CartPoleEnvPoleM09l07-v0',
    entry_point='cartpole_envs.envs:CartPoleEnvPoleM09l07',
    max_episode_steps=500,
    reward_threshold=475.0,
)



