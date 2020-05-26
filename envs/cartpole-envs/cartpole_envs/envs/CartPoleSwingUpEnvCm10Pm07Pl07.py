from .cartpole_swingup_temp import *


class CartPoleSwingUpEnvCm10Pm07Pl07(CartPoleSwingUpEnv_template):
    def __init__(self):
        super().__init__( masscart =1.0, masspole=0.7, polelength=0.7)