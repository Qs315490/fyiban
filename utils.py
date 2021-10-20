#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Sricor
# @Date: 2021-10-20
# 推送

import json
import requests

def wechat(corpid, agentid, corpsecret, msg):
    """
    企业微信推送
    corpid: 企业ID
    agentid: 应用ID
    corpsecret: 应用密钥
    """
    data = {
        "touser" : "@all",
        "msgtype" : "text",
        "agentid" : agentid,
        "text" : {"content" : msg},
    }
    access_token = requests.get(
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken', 
        params = {'corpid': corpid, 'corpsecret': corpsecret}
    ).json()['access_token']

    requests.post(
        url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send', 
        params = {'access_token': access_token}, 
        data = json.dumps(data)
    )
