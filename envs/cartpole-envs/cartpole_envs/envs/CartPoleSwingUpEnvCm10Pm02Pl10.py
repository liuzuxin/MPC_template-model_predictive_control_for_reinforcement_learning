from .cartpole_swingup_temp import *


class CartPoleSwingUpEnvCm10Pm02Pl10(CartPoleSwingUpEnv_template):
    def __init__(self):
        super().__init__( masscart =1.0, masspole=0.2, polelength=1.0)