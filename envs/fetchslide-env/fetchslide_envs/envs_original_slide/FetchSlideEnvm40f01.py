'''
@Author: Wenhao Ding
@Email: wenhaod@andrew.cmu.edu
@Date: 2020-04-15 12:09:20
@LastEditTime: 2020-04-17 20:29:58
@Description: 
'''

from .FetchSlideEnv_template import FetchSlideEnv_template

class FetchSlideEnvm40f01(FetchSlideEnv_template):
    def __init__(self):
        super().__init__(reward_type='dense', model_xml_path='slide_m40f01.xml')
