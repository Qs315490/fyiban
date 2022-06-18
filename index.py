import os
import utils
import requests
import datetime
from base64 import b64decode

from yiban.yiban import Yiban

"""
cron 0 08 * * * index.py
new Env('易班打卡');
"""

def main():
    config = {
        "Thread": False,
       
        "UserList":[
            # 用户列表 {"mobile": "手机号", "password": "密码"}
            {"name": "XXX", "mobile": "XXXX", "password": "XXX"}, 
        ],

        "SubmitData": {
            # 以下需手动抓包解密
            # 提交表单 BEGIN
            "WFId": "",
            "Data": {
                "9843754e97aad058523524bdb8991bcd": "否", 
                "72fe9c2c81a48fd0968edbbb3f2c1c42": "36.5", 
                "769bbfbfb026629f1ddb0294a9c0d257": "湘南学院", 
                "90b5b83950ae456fefebb0f751406e2d": [], 
                "0242914b8746275c5073ccdb156f9d1d":[],
                "1bac180dd37455f7c16a36336c0411a8":{}
            },

            "Extend": { 
                "TaskId": "", 
                "title": "任务信息", 
                "content": [
                    {"label": "任务名称", "value": "每日健康打卡"},
                    {"label": "发布机构", "value": ""},
                    {"label": "发布人", "value": ""}
                ]
            }
            # 提交表单 END
        }
    }

    # 消息头
    msg = f"易班打卡: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} \n"

    # 环境变量 base64 url形式获取config 可忽略
    env = os.getenv('YIBAN') 
    if env != None:
        config_url = b64decode(env).decode("utf-8")
        resp = requests.get(config_url).json()
        config = resp

    # 遍历账号列表 打卡
    for i in config["UserList"]:
        yb = Yiban(i["mobile"], i["password"])

        # 健康提交
        result = yb.helath_submit()

        # 当前存在其他任务
        result += " 当前存在其他任务："
        if len(yb.uncompleted_task()) != 0:
            for j in yb.uncompleted_task():
                result += j["Title"]
        
        # 拼接消息
        msg = result + "\n"

    # 企业微信推送 可自行修改
    if 'WechatPush' in config:
        utils.WechatAppPush(config['WechatPush']['corpid'], config['WechatPush']['corpsecret'], config['WechatPush']['agentid'])(msg)()  # 企业微信推送

if __name__ == "__main__":
    main()