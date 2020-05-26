from .cartpoleENV_temp import *


class CartPoleEnvPoleM20l15(CartPoleEnv_template):
    def __init__(self):
        super().__init__( masscart =2.0, masspole=0.3, polelength=1.5)