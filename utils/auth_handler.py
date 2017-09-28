# -*- coding: utf-8 -*-

import requests
import json

class AuthHandler(object):
    '''
    认证工具类
    '''

    def __init__(self, config=None):
        '''
        构造函数

        :param config:配置类
        '''
        self.userName=config.USER_NAME
        self.password=config.PASSWORD
        self.url=config.AUTH_URL

    def authenticate(self):
        '''
        认证
        :return: 0 认证成功，-1 认证失败
        '''
        headers = {'content-type': 'application/json'}
        r = requests.post(url=self.url, data="{\"userName\":\""+ self.userName+"\", \"password\":\""+ self.password+"\"}",
                          headers=headers)
        retval=r.json()
        if retval.haskey('id_token'):
            self.token=retval['id_token']
            return 0
        else:
            return -1

    def get_token(self):
        '''
        返回认证成功后的token
        :return: token
        '''
        return self.token



