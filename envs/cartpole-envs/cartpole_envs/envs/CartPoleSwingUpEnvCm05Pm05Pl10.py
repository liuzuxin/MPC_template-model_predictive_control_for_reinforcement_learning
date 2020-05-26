from .cartpole_swingup_temp import *


class CartPoleSwingUpEnvCm05Pm05Pl10(CartPoleSwingUpEnv_template):
    def __init__(self):
        super().__init__( masscart =0.5, masspole=0.5, polelength=1.0)