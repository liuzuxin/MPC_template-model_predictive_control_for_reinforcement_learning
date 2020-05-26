from .cartpole_swingup_temp import *


class CartPoleSwingUpEnvCm10Pm05Pl05(CartPoleSwingUpEnv_template):
    def __init__(self):
        super().__init__( masscart =1.0, masspole=0.5, polelength=0.5)