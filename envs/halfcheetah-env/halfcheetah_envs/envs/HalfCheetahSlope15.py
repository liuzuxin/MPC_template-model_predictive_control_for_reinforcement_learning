'''
@Author: Wenhao Ding
@Email: wenhaod@andrew.cmu.edu
@Date: 2020-04-15 12:09:20
@LastEditTime: 2020-05-04 18:56:52
@Description: 
'''

from .HalfCheetahEnv_template import HalfCheetahEnv

class HalfCheetahSlope15(HalfCheetahEnv):
    def __init__(self):
        super().__init__(model_xml_path='half_cheetah15.xml')
