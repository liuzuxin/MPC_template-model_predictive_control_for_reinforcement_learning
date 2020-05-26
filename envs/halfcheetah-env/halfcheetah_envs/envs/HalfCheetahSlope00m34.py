'''
@Author: Wenhao Ding
@Email: wenhaod@andrew.cmu.edu
@Date: 2020-04-15 12:09:20
@LastEditTime: 2020-05-13 14:17:27
@Description: 
'''

from .HalfCheetahEnv_template import HalfCheetahEnv

class HalfCheetahSlope00m34(HalfCheetahEnv):
    def __init__(self):
        super().__init__(model_xml_path='half_cheetah00m34.xml')
