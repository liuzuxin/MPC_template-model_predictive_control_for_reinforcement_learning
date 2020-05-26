from .cartpole_swingup_temp import *


class CartPoleSwingUpEnvCm20Pm01Pl05(CartPoleSwingUpEnv_template):
    def __init__(self):
        super().__init__( masscart =2.0, masspole=0.1, polelength=0.5)