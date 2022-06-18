#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Sricor
# @Date: 2022-6-18
# 易班校本化 健康打卡

import sys
import time
from json import dumps
from re import findall
from requests import session
from base64 import b64encode
from Crypto.Cipher import AES
from datetime import datetime, timedelta


sys.path.append("..")

from yiban.base import Base


class HealthSubmit(Base):
    def __init__(self, access_token) -> None:
        self._csrf = '00000'
        self._session = session()
        self._access_token = access_token
        self._auth()

    def get_task_uncompleted(self) -> list:
        # 获取未完成任务列表
        # {'code': 0, 'msg': '', 'data': []}
        # {'code': 999, 'msg': '未登录或登录已经超时', 'data': None}
        # {'code': 0, 'msg': '', 'data': [{'TaskId': '', 'OrgId': '', 'TimeoutState': 1, 'State': 0, 'Title': '每日健康打卡', 'Type': 1, 'StartTime': 1655481600, 'EndTime': 1655539200}]}

        self._debug_msg("Class HealthSubmit: get_task_uncompleted")
        
        start_time = (datetime.now() + timedelta(days=-14)).strftime('%Y-%m-%d 00:00')  # 查询开始时间
        end_time = time.strftime("%Y-%m-%d 23:59", time.localtime())                    # 查询结束时间
        response = self._req(url = "https://api.uyiban.com/officeTask/client/index/uncompletedList", 
            params = {
                'CSRF'     : self._csrf,
                'EndTime'  : end_time,
                'StartTime': start_time }).json()

        self._debug_msg(response) # DEBUG

        if response["code"] == 0:
            self._log_msg("Get uncompleted task successful. ")
            return response["data"]
        else:
            raise Exception (f"Get uncompleted task failed. {response['msg']}")

    def get_task_wfid(self, task_id) -> str:
        """ 
        {
            'code': 0, 
            'msg': '', 
            'data': {
                'Id': '', 
                'Title': '每日健康打卡', 
                'Type': 1, 
                'ReceiverSendBack': 0, 
                'TypeId': 'f08f668b41e4f259de7e8330dfced698', 
                'AllowSendBackHours': 0, 
                'AllowSendBackTimes': 1, 
                'PubOrgName': '', 
                'PubPersonName': '', 
                'Content': '', 
                'AllowTimeout': 1, 
                'AttachmentIds': '[]', 
                'PubOrgId': 'b8350a76122fe2c5750d8375c23cca45', 
                'IsPubPersonShow': 1, 
                'CreateTime': 1655481612, 
                'StartTime': 1655481600, 
                'EndTime': 1655539200, 
                'Displayed': 1, 
                'TimeState': 1, 
                'WFId': '', 
                'AttachmentList': [], 
                'WorkflowState': 0, 
                'InitiateId': '',
                'RetreatReason': '', 
                'EvaluationState': 0, 
                'EvaluationReason': '', 
                'State': 'uncompleted', 
                'RecordState': 0, 
                'CanSendBack': 0, 
                'SendBackEndTime': 1655539200, 
                'IsLost': 0, 
                'Feedback': 0, 
                'ChangeReason': ''
            }
        }
        """
        self._debug_msg("Class HealthSubmit: get_task_wfid")

        response = self._req(
            url='https://api.uyiban.com/officeTask/client/index/detail', 
            params={'TaskId': task_id, 'CSRF': self._csrf}).json()

        self._debug_msg(response) # DEBUG

        if response["code"] == 0:
            self._log_msg("Get task wfid successful. ")
            return response["data"]["WFId"]
        else:
            raise Exception (f"Get task wfid error.  {response['msg']}")


    def submit_task(self, data:dict) -> int:
        # 健康打卡提交

        self._debug_msg("Class HealthSubmit: submit_task")

        task_uncompleted_list = self.get_task_uncompleted()
        task_submit_data = data.copy()
        task_id   = ""  # 任务ID
        task_name = ""  # 任务名称
        task_wfid = ""  # 任务WFID

        # 获取任务名称
        for i in task_submit_data["Extend"]["content"]:
            if i["label"] == "任务名称":
                task_name = i["value"]
        
        if task_name == "": return 1
        
        # 获取任务ID
        for i in task_uncompleted_list:
            if i["Title"] == task_name:
                task_id = i["TaskId"]

        # 获取任务WFID
        task_wfid = self.get_task_wfid(task_id)

        # 整理表单
        task_submit_data["WFId"] = task_wfid
        task_submit_data["Extend"]["TaskId"] = task_id

        task_submit_data['Data'] = dumps(task_submit_data['Data'], ensure_ascii=False)
        task_submit_data['Extend'] = dumps(task_submit_data['Extend'], ensure_ascii=False)
        task_submit_data = self.__encrypt_aes(dumps(task_submit_data, ensure_ascii=False))

        # 提交接口
        response = self._req("POST", url = 'https://api.uyiban.com/workFlow/c/my/apply',
            params = {'CSRF': self._csrf},
            data = {'Str': task_submit_data}).json()

        self._debug_msg(response) # DEBUG

        if response["code"] == 0:
            self._log_msg("Submit task successful. ")
            return 0
        else:
            raise Exception (f"Submit task error. {response['msg']}")


    def _auth(self) -> None:
        # 用户认证

        response = self._req(url = 'http://f.yiban.cn/iapp/index', 
            params = {'act': 'iapp7463'},
            cookies = {'loginToken': self._access_token},
            allow_redirects = False )

        self._reauth()

        try:
            verify = findall(r"verify_request=(.*?)&", response.headers.get("Location"))[0]
        except:
            raise Exception ("Auth Error.")   # token 错误或过期 access_token expired error

        response = self._req(url = "https://api.uyiban.com/base/c/auth/yiban", 
            params = {"verifyRequest": verify, "CSRF": self._csrf}).json()

        if response["data"] == None:
            raise Exception ("Auth Error 02.")   # 认证失败

    def _reauth(self) -> None:
        # 用户应用重认证

        client_id = "95626fa3080300ea"
        redirect_uri = "https://f.yiban.cn/iapp7463"

        self._req(url = "https://oauth.yiban.cn/code/html",
            params = {"client_id": client_id, "redirect_uri": redirect_uri})

        self._req("POST", url = "https://oauth.yiban.cn/code/usersure", 
            data = {"client_id": client_id, "redirect_uri": redirect_uri})


    def _req(self, method:str = "GET", url:str = "", data:dict = {}, params:dict = {}, timeout:int = 10, allow_redirects:bool = True, **kwargs):
        cookies = {"csrf_token": self._csrf}
        headers = {"Origin": "https://c.uyiban.com", "User-Agent": "Yiban", "AppVersion": "5.0"}
        if 'cookies' in kwargs:  cookies.update(kwargs.get("cookies"))
        if 'headers' in kwargs:  headers.update(kwargs.get("headers"))
        if method == "GET":
            return self._session.get(
                url     = url, 
                data    = data,
                params  = params,
                headers = headers, 
                cookies = cookies, 
                timeout = timeout,
                allow_redirects = allow_redirects
            )
        elif method == "POST":
            return self._session.post(
                url     = url, 
                data    = data,
                params  = params,
                headers = headers, 
                cookies = cookies, 
                timeout = timeout,
                allow_redirects = allow_redirects
            )
        else:
            raise Exception("Request Method Error. ")
    
    def __encrypt_aes(self, data:object) -> str:
        """ Submit data encrypt function """
        aes_key = '2knV5VGRTScU7pOq'
        aes_iv = 'UmNWaNtM0PUdtFCs'
        aes_key = bytes(aes_key, 'utf-8')
        aes_iv = bytes(aes_iv, 'utf-8')
        data = bytes(data, 'utf-8')
        bs = AES.block_size
        padding = bs - len(data) % bs
        padding_text = bytes(chr(padding) * padding, 'utf-8')
        data = data + padding_text
        cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
        encrypted = b64encode(cipher.encrypt(data))
        return b64encode(encrypted)

if __name__ == "__main__":
    token = "3c9e5ecdb0a1d430d8e7d0fbbc65663"

    data = {
        "WFId": "",
        "Data": {
            "9843754e97aad058523524bdb8991bcd": "否", 
            "72fe9c2c81a48fd0968edbbb3f2c1c42": "36.5", 
            "769bbfbfb026629f1ddb0294a9c0d257": "P", 
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
                "time":"2022-05-20 00:00",
                "longitude":0,
                "latitude":0,
                "address":""
            }
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
    }

    t = HealthSubmit(token)

    t.submit_task(data)
    # t.get_task_uncompleted()
    # t.get_task_wfid("")

