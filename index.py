#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Sricor
# @Date: 2021-10-20
# 易班校本化打卡

import time
import utils
import json
from yiban import Yiban



# 提交表单
# 需要手动抓包
# crypter.py aes_decrypt()解密填写
# 支持云函数
def main_handler(data=None, extend=None):
    msg = f"{time.strftime('%m-%d',time.localtime(time.time()))} 易班打卡："
    with open('config.json', encoding='utf-8') as f:
        json_data = json.load(f)
    # 打卡列表
    # mobile: 账号
    # password: 密码
    # 遍历用户列表
    for i in json_data['UserList']:
        try:
            result = Yiban(i['mobile'], i['password']).submit_task()
            msg = f'{msg}\n {result["name"]}: {result["msg"]}'
            print(result)
        except Exception as e:
            msg = f'{msg}\n {i["name"]}: Error {e}'
        finally:
            time.sleep(1)
    return msg

if __name__ == '__main__':
    msg = main_handler()
    print(msg)
    # 企业微信推送
    # agentid = ''
    # corpid = ''
    # corpsecret = ''
    # utils.wechat(corpid, agentid, corpsecret, msg) # 企业微信推送

    # bark推送
    # key = ''
    # utils.bark(key, msg) # bark推送
