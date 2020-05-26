from .cartpole_swingup_temp import *


class CartPoleSwingUpEnvCm10Pm10Pl05(CartPoleSwingUpEnv_template):
    def __init__(self):
        super().__init__( masscart =1.0, masspole=1.0, polelength=0.5)