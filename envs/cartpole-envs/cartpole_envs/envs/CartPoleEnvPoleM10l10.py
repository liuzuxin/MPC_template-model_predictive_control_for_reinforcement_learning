from .cartpoleENV_temp import *


class CartPoleEnvPoleM10l10(CartPoleEnv_template):
    def __init__(self):
        super().__init__( masscart =1.0, masspole=0.2, polelength=1.0)