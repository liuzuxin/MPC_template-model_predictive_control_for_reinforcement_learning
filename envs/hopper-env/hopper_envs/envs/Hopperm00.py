'''
@Author: Wenhao Ding
@Email: wenhaod@andrew.cmu.edu
@Date: 2020-04-15 12:09:20
@LastEditTime: 2020-05-13 22:51:00
@Description: 
'''

from .HopperEnv_template import HopperEnv

class Hopperm00(HopperEnv):
    def __init__(self):
        super().__init__(model_xml_path='hopper_00.xml')
