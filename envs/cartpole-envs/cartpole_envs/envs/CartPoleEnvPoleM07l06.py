from .cartpoleENV_temp import *


class CartPoleEnvPoleM07l06(CartPoleEnv_template):
    def __init__(self):
        super().__init__( masscart =1.0, masspole=0.7, polelength=0.6)