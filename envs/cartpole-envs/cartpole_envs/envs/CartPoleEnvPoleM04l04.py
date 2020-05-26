from .cartpoleENV_temp import *


class CartPoleEnvPoleM04l04(CartPoleEnv_template):
    def __init__(self):
        super().__init__( masscart =1.0, masspole=0.4, polelength=0.4)