from .cartpole_swingup_temp import *


class CartPoleSwingUpEnvCm20Pm02Pl10(CartPoleSwingUpEnv_template):
    def __init__(self):
        super().__init__( masscart =2.0, masspole=0.2, polelength=1.0)