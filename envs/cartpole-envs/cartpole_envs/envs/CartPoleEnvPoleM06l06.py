from .cartpoleENV_temp import *


class CartPoleEnvPoleM06l06(CartPoleEnv_template):
    def __init__(self):
        super().__init__( masscart =1.0, masspole=0.6, polelength=0.6)