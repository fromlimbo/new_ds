# -*- coding: utf-8 -*-
import requests
import logging
import json

class Reporter(object):
    '''
    向制定目的发送get或post请求，返回状态码和结果。__init__ 初始化为要接的对象， reportGet，reportPost，分别为get请求和post请求
    '''

    def __init__(self, config=None):
        self.config = config
        #REPORT_ADDRESS必须包含协议http或https
        self.url =  self.config.REPORT_SERVER +":"+self.config.REPORT_PORT + self.config.REPORT_ADDRESS


    def report_get(self, jsondata, timeout=3):
        """
        用get方法回报结果

        :param jsondata: 传输给服务器的json数据
        :param timeout: 连接超时时间，默认是3秒
        :return: (res_status, content),状态码和相应内容
        """
        try:
            json.loads(jsondata)
        except Exception as e:
            raise e
        else:
            getdata = {"data":jsondata}
            try:
                response = requests.get(url=self.url,params=getdata,timeout=timeout)
            except Exception as e:
                logging.warn("connection error")
                return -1
            else:
                res_status = response.status_code
                content = response.content
                return (res_status,content)


    def report_post(self, jsondata, timeout=3):
        """
        用post方法回报结果

        :param jsondata: 传输给服务器的json数据
        :param timeout: 连接超时时间，默认是3秒
        :return: (res_status,content),状态码和相应内容
        """

        try:
            postdata = {"data":jsondata}
        except Exception as e:
            raise  e
        else:
            try:
                response = requests.post(self.url,data=postdata,timeout=timeout)
            except Exception as e:
                logging.warn("connection error")
                return -1
            else:
                res_status = response.status_code
                content = response.content
                return (res_status, content)
