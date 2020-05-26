from .cartpole_swingup_temp import *


class CartPoleSwingUpEnvCm05Pm04Pl05(CartPoleSwingUpEnv_template):
    def __init__(self):
        super().__init__( masscart =0.5, masspole=0.4, polelength=0.5)