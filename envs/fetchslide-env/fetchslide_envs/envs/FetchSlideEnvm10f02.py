'''
@Author: Wenhao Ding
@Email: wenhaod@andrew.cmu.edu
@Date: 2020-04-15 12:09:20
@LastEditTime: 2020-04-25 20:36:35
@Description: 
'''

from .FetchSlideEnv_template import FetchSlideEnv_template

class FetchSlideEnvm10f02(FetchSlideEnv_template):
    def __init__(self):
        super().__init__(reward_type='dense', model_xml_path='slide_m10f02.xml')
