# -*- coding: utf-8 -*-
import logging
import ConfigParser
import os
import json

class ConfigBuilder:
    '''
    获取配置信息的操作，初始化时需指定 配置存放的位置filename,和section(需要获得的配置)
    '''
    def __init__(self, filename, section):
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(os.path.abspath(filename))

        self.filename = filename
        self.section = section
        self.config = dict()

        for con in self.cf.items(self.section):
            self.set_config(con[0],con[1])

    def set_config(self,key,values):
        '''
        修改配置文件
        :param key: 需要修改的键
        :param values:  需要修改的值
        :return:
        '''
        try:
            vals = json.loads(values)
            self.config[key] = vals
        except:
            self.config[key] = values
        return 0


    def update_config(self, key, value, write_file=False):
        '''
        对配置文件的配置项进行修改，如果write_file为真，则把修改写入到配置文件
        :param key: 需修改的配置项的 键
        :param value: 需修改的配置项的 值
        :param write_file: 是否把修改写入到配置文件，默认False（不写入）
        :return:
        '''
        # self.config[key] = value
        # setattr(self, key, value)
        self.set_config(key,value)
        if write_file:
            self.save_config(key, value)
        return 0

    def save_config(self, key, value):
        '''
        把指定的key，和value写入到配置文件
        :param key: 需要保存的键
        :param value: 需要保存的值
        :return:
        '''
        self.cf.set(self.section, key, value)
        self.cf.write(open(os.path.abspath(self.filename), "w"))
        return 0

    def todict(self):
        '''
        以字典的形式返回指定的配置集
        :return:
        '''
        return self.config



if __name__ == "__main__":
    cf = ConfigParser.ConfigParser()
    cf.read(os.path.abspath("config_sample.ini"))
    info = cf.get("MQLogConfig", "queue_names")
    print info
    todic = json.loads(info)
    print type(todic)
    print todic