#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Sricor
# @Date: 2022-4-20

"""
cron 0 08 * * * index.py
new Env('易班打卡');
"""

import os
import yiban
import utils
import logging
import datetime
import requests
import threading
from base64 import b64decode

config = {
    "user": [
        {"name": "xxx", "mobile": "xxx", "password": "xxx"},
        {"name": "xxx", "mobile": "xxx", "password": "xxx"}
    ],

    "submit_data": {
        "WFId": "",
        "Data": { 
            "9843754e97aad058523524bdb8991bcd": "否", 
            "72fe9c2c81a48fd0968edbbb3f2c1c42": "36.5", 
            "769bbfbfb026629f1ddb0294a9c0d257": "location", 
            "90b5b83950ae456fefebb0f751406e2d": [{ 
                "name": "348816E7-275F-42D8-9118-625FB45D8D48.png", 
                "type": "image/png", 
                "size ": 472092, 
                "status": "done", 
                "percent ": 100, 
                "fileName": "workflow/202110/18/4c3599675b629e14e80ffe19c507b806.png ", 
                "path": "workflow/202110/18/4c3599675b629e14e80ffe19c507b806.png "
            }], 
            "0242914b8746275c5073ccdb156f9d1d":[{ 
                "name": "86E7DCB9-7FEE-441F-B921-039302A1048B.png", 
                "type": "image/png", 
                "size": 179394, 
                "status": "done", 
                "percent": 100, 
                "fileName": "workflow/202110/23/30150ea922a720e7fb732eb7150cc532.png ", 
                "path": "workflow/202110/23/30150ea922a720e7fb732eb7150cc532.png "
            }],
            "1bac180dd37455f7c16a36336c0411a8":{
                "time":"2022-04-20 12:00",
                "longitude":0,
                "latitude":0,
                "address":"location"
            }
        },

        "Extend": { 
            "TaskId": "", 
            "title": "任务信息", 
            "content": [
                {"label": "任务名称", "value": "每日学生疫情上报"},
                {"label": "发布机构", "value": "学生处"},
                {"label": "发布人", "value": "邸灿"}
            ]
        }
    },
}

msg = [] # 消息列表
env = os.getenv('YIBAN') # 自用 环境变量 base64 url形式获取config
if env != None:
    config_url = b64decode(env).decode("utf-8")
    resp = requests.get(config_url).json()
    config= resp


def submit(name: str, mobile: str, password: str, submit_data: dict, count=0):
    """ 
    单线程 提交
    :param name: 名称
    :param mobile: 手机号
    :param password: 密码
    :param submit_data: 提交表单
    """
    while count < 3: # 重试3次
        try:
            y = yiban.submit(name=name, mobile=mobile, password=password, submit_data=submit_data)
            msg.append(f"{y['name']}: {y['msg']}")
            break
        except Exception as e:
            print(e)
            count += 1
            if count == 3: # 超过三次
                msg.append(f"{mobile}: Error")


@utils.Debug(level=logging.INFO) # DEBUG
def main_handler():
    msg.append(f"易班打卡: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    threads = [] # 线程池
    for i in config['user']:
        threads.append(threading.Thread(target=submit, args=(i['name'], i['mobile'], i['password'], config['submit_data'])))
    for t in threads:
        t.start() # 启动线程
    for t in threads:
        t.join() # 守护线程
    return_msg = "\n".join(msg)
    if 'corpid' in config:
        utils.WechatAppPush(config['corpid'], config['corpsecret'], config['agentid'])(return_msg)()  # 企业微信推送
    return return_msg

if __name__ == '__main__':
    print(main_handler())
