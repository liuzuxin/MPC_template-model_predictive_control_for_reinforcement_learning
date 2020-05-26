'''
@Author: Wenhao Ding
@Email: wenhaod@andrew.cmu.edu
@Date: 2020-04-15 12:09:20
@LastEditTime: 2020-04-17 20:29:50
@Description: 
'''

from .FetchSlideEnv_template import FetchSlideEnv_template

class FetchSlideEnvm20f01(FetchSlideEnv_template):
    def __init__(self):
        super().__init__(reward_type='dense', model_xml_path='slide_m20f01.xml')
