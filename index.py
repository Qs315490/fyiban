#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Sricor
# @Date: 2022-4-20

"""

index.py

1.修改USER账号信息

2.进行抓包，手动提交一次易班打卡

3.crypter.py解密POST表单中Str

4.修改SUBMIT_DATA中提交表单数据

"""

from yiban import Yiban
import datetime
import logging


USER = [
    {'mobile': 'xxx', 'password': 'xxx'}, 
    {'mobile': 'xxx', 'password': 'xxx'}
]

SUBMIT_DATA = {
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
}

def timer(func):
    def wrapper():
        LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
        DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
        logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT)
        print("易班打卡: ", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "🔔")
        start = datetime.datetime.now()
        print(func())
        stop = datetime.datetime.now()
        print(f'Time: {(stop - start).seconds}s')
        return None
    return wrapper

@timer
def main_handler():
    for i in USER:
        try:
            Yiban(i['mobile'], i['password']).submit_task(SUBMIT_DATA)
        except:
            print(f"{i['mobile']} Error")

if __name__ == '__main__':
    main_handler()
