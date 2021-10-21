#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Sricor
# @Date: 2021-10-20
# 易班校本化打卡

import time
import random
from yiban import Yiban
from utils import wechat

# 打卡列表
# mobile: 账号
# password: 密码
UserList = [
        {"name": "", "mobile": "", "password": ""}, 
        {"name": "", "mobile": "", "password": ""}, 
        {...}, 
    ]

# 微信推送
#agentid = ''
#corpid = ''
#corpsecret = ''

# 提交表单
# 需要手动抓包填写
PostData = {
    "WFId": "",
    "Data": {
        "9843754e97aad058523524bdb8991bcd": "否", 
        "72fe9c2c81a48fd0968edbbb3f2c1c42": f'36.{random.randint(3,8)}', 
        "769bbfbfb026629f1ddb0294a9c0d257": "示例位置", 
        "90b5b83950ae456fefebb0f751406e2d": [{ 
            "name": "348816E7-275F-42D8-9118-625FB45D8D48.png ", 
            "type": "image/png ", 
            "size ": 472092, 
            "status": "done ", "percent ": 100, 
            "fileName": "workflow/202110/18/4c3599675b629e14e80ffe19c507b806.png ", 
            "path": "workflow/202110/18/4c3599675b629e14e80ffe19c507b806.png "
            }],
        "0242914b8746275c5073ccdb156f9d1d": [{ 
            "name": "86E7DCB9-7FEE-441F-B921-039302A1048B.png", 
            "type": "image/png ", 
            "size": 175580, 
            "status": "done ", 
            "percent": 100, 
            "fileName": "workflow/202110/18/b82da80c3a4dc4ad6f4a1ebe325fb033.png ", 
            "path": "workflow/202110/18/b82da80c3a4dc4ad6f4a1ebe325fb033.png "
            }]
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

def main():
    msg = f"{time.strftime('%m-%d',time.localtime(time.time()))} 易班打卡："
    for i in UserList:
        try:
            result = Yiban(i['mobile'], i['password']).submit(PostData)
            msg = f'{msg}\n {result["name"]}: {result["msg"]}'
            print(result)
        except:
            msg = f'{msg}\n {i["name"]}: Error'
            continue
        finally:
            time.sleep(1)
    return msg

if __name__ == '__main__':
    msg = main()
    print(msg)
    #wechat(corpid, agentid, corpsecret, msg) # 企业微信推送
