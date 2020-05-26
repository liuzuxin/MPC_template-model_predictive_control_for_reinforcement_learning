'''
@Author: Wenhao Ding
@Email: wenhaod@andrew.cmu.edu
@Date: 2020-04-15 12:09:20
@LastEditTime: 2020-05-04 18:59:57
@Description: 
'''

from .HalfCheetahEnv_template import HalfCheetahEnv

class HalfCheetahSlope00(HalfCheetahEnv):
    def __init__(self):
        super().__init__(model_xml_path='half_cheetah00.xml')
