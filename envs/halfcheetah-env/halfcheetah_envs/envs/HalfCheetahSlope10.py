'''
@Author: Wenhao Ding
@Email: wenhaod@andrew.cmu.edu
@Date: 2020-04-15 12:09:20
@LastEditTime: 2020-05-08 20:10:44
@Description: 
'''

from .HalfCheetahEnv_template import HalfCheetahEnv

class HalfCheetahSlope10(HalfCheetahEnv):
    def __init__(self):
        super().__init__(model_xml_path='half_cheetah10.xml')
