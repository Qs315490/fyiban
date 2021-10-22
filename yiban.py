#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Sricor
# @Date: 2021-10-20

import re
import time
import json
import requests
import datetime
from crypter import rsa_encrypt, aes_encrypt

AES_KEY = '2knV5VGRTScU7pOq'
AES_IV = 'UmNWaNtM0PUdtFCs'
RSA_KEY = '''-----BEGIN PUBLIC KEY-----
        MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA6aTDM8BhCS8O0wlx2KzA
        Ajffez4G4A/QSnn1ZDuvLRbKBHm0vVBtBhD03QUnnHXvqigsOOwr4onUeNljegIC
        XC9h5exLFidQVB58MBjItMA81YVlZKBY9zth1neHeRTWlFTCx+WasvbS0HuYpF8+
        KPl7LJPjtI4XAAOLBntQGnPwCX2Ff/LgwqkZbOrHHkN444iLmViCXxNUDUMUR9bP
        A9/I5kwfyZ/mM5m8+IPhSXZ0f2uw1WLov1P4aeKkaaKCf5eL3n7/2vgq7kw2qSmR
        AGBZzW45PsjOEvygXFOy2n7AXL9nHogDiMdbe4aY2VT70sl0ccc4uvVOvVBMinOp
        d2rEpX0/8YE0dRXxukrM7i+r6lWy1lSKbP+0tQxQHNa/Cjg5W3uU+W9YmNUFc1w/
        7QT4SZrnRBEo++Xf9D3YNaOCFZXhy63IpY4eTQCJFQcXdnRbTXEdC3CtWNd7SV/h
        mfJYekb3GEV+10xLOvpe/+tCTeCDpFDJP6UuzLXBBADL2oV3D56hYlOlscjBokNU
        AYYlWgfwA91NjDsWW9mwapm/eLs4FNyH0JcMFTWH9dnl8B7PCUra/Lg/IVv6HkFE
        uCL7hVXGMbw2BZuCIC2VG1ZQ6QD64X8g5zL+HDsusQDbEJV2ZtojalTIjpxMksbR
        ZRsH+P3+NNOZOEwUdjJUAx8CAwEAAQ==
        -----END PUBLIC KEY-----
        '''

class Yiban():
    def __init__(self, mobile, password):
        self.csrf = '000000'
        self.session = requests.session()
        self.result = {'code': 0, 'name': '', 'msg': ''}

        # get name&access_token
        resp = requests.post(
            url = 'https://mobile.yiban.cn/api/v4/passport/login',
            headers = {'AppVersion': '5.0'}, 
            data = {
                'mobile': mobile,
                'password': rsa_encrypt(RSA_KEY, password),
                'ct': '2',
                'identify': '1'
            }
        ).json()
        if 'access_token' in resp['data']:
            self.result['name'] = resp['data']['user']['name']
            self.access_token = resp['data']['access_token']
        else:
            raise Exception('Login Error')
    
    def req(self, url, method='get', params=None, data=None, allow_redirects=True, timeout=10):
        """
        requests
        增加请求延时，避免请求过快 Error104
        """
        time.sleep(1)
        cookies = { 'loginToken': self.access_token, 'csrf_token': self.csrf}
        headers = {"Origin": "https://c.uyiban.com", "User-Agent": "Yiban", "AppVersion": "5.0"}
        if method == 'get':
            return self.session.get(
                url = url, 
                params = params,
                data = data,
                headers = headers, 
                cookies = cookies, 
                timeout = timeout,
                allow_redirects = allow_redirects
            )
        elif method == 'post':
            return self.session.post(
                url = url, 
                params = params,
                data = data, 
                headers = headers, 
                cookies = cookies, 
                timeout = timeout,
                allow_redirects = allow_redirects
            )
        else:
            return 'Requests method error'

    def submit(self, postData):
        """
        SubmitTask
        postData: 提交表单 
        """
        try:
            resp = self.req(
                url = 'http://f.yiban.cn/iapp/index', 
                params = {'act': 'iapp7463'},
                allow_redirects = False
            )
            verify = re.findall(r"verify_request=(.*?)&", resp.headers.get("Location"))[0]

            resp = self.req(
                url = 'https://api.uyiban.com/base/c/auth/yiban', 
                params = {'verifyRequest': verify, 'CSRF': self.csrf},
            ).json()

        except Exception as e:
            self.result['msg'] = f'[Error]Auth: {e}'
            return self.result

        try:
            resp = self.req(
                url = 'https://api.uyiban.com/officeTask/client/index/uncompletedList', 
                params = {
                    'StartTime': (datetime.datetime.now() + datetime.timedelta(days=-14)).strftime('%Y-%m-%d'),
                    'EndTime': time.strftime("%Y-%m-%d 23:59", time.localtime()),
                    'CSRF': self.csrf
                }
            ).json()

            if resp['data'] is None:
                """
                校本化认证过期，尝试重新验证
                """
                resp = self.req(
                    method = 'post',
                    url = 'https://oauth.yiban.cn/code/usersure', 
                    data = {'client_id': '95626fa3080300ea', 'redirect_uri': 'https://f.yiban.cn/iapp7463'}
                )
                raise Exception('认证失败')
            else:
                # 任务列表
                taskList = []

                # 任务名称
                for t in postData['Extend']['content']:
                    if t['label'] == '任务名称':
                        taskTitle = t['value']
                
                # 任务打卡
                for i in resp['data']:
                    if i['Title'] == taskTitle:
                        TaskId = i['TaskId']

                        postData['WFId'] = self.req(
                            url = 'https://api.uyiban.com/officeTask/client/index/detail', 
                            params = {'TaskId': TaskId, 'CSRF': self.csrf}
                        ).json()['data']['WFId']
                        postData['Extend']['TaskId'] = TaskId
                        postData['Data'] = json.dumps(postData['Data'], ensure_ascii=False)
                        postData['Extend'] = json.dumps(postData['Extend'], ensure_ascii=False)
                        postData = json.dumps(postData, ensure_ascii=False)

                        resp = self.req(
                            method = 'post',
                            url = f'https://api.uyiban.com/workFlow/c/my/apply',
                            params = {'CSRF': self.csrf},
                            data = {'Str': aes_encrypt(AES_KEY, AES_IV, postData)}
                        ).json()

                        if resp['code'] == 0:
                            self.result['code'] = 1
                            self.result['msg'] = '打卡成功'
                            return self.result
                        else:
                            self.result['msg'] = resp['msg']
                            return self.result
                    else:
                        taskList.append(i['Tittle'])
                        self.result['task'] = taskList
                        continue

                self.result['code'] = 2
                if len(taskList) == 0:
                    self.result['msg'] = '无未打卡任务'
                else:
                    self.result['msg'] = '当前存在其他任务：'.join(taskList)
                return self.result

        except Exception as e:
            self.result['msg'] = f'[Error]Submit: {e}'
            return self.result
