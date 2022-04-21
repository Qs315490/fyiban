#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Sricor
# @Date: 2022-4-20


import re
import json
import time
import logging
import requests
import datetime
from base64 import b64encode
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5, AES

class Yiban:
    """
    Basic Usage::
        >>> from yiban import Yiban
        >>> y = Yiban('account', 'password')
        >>> y.sunmit_task(task_data)

    """

    def __init__(self, mobile: str, password: str) -> None:
        self.__name = ''
        self.__mobile = mobile
        self.__password = password
        self.__access_token = ''
        self.__csrf = '000000'
        self.__session = requests.session() # Keep alive
        self.__login()
    
    def log_msg(self, msg: str, level=20) -> None:
        """
        Logging function
        CRITICAL 50
        ERROR    40
        WARNING  30
        INFO     20
        DEBUG    10
        NOTSET   0
        """
        logging.log(msg=f"{self.__name} {msg}", level=level)
    
    def req(self, url: str, method='get', timeout=10, allow_redirects=True, **kwargs) -> requests :
        """
        Use requests.session() to construct request function
        Keep alive
        """
        time.sleep(2) # Increase request delay to avoid requests too fast Error104
        cookies = {'csrf_token': self.__csrf}
        headers = {"Origin": "https://c.uyiban.com", "User-Agent": "Yiban", "AppVersion": "5.0"}
        try:
            data = kwargs.get("data")
            params = kwargs.get("params")
            cookies.update(kwargs.get("cookies"))
            headers.update(kwargs.get("headers"))
        except:
            pass
        if method == 'get':
            return self.__session.get(
                url     = url, 
                data    = data,
                params  = params,
                headers = headers, 
                cookies = cookies, 
                timeout = timeout,
                allow_redirects = allow_redirects
            )
        elif method == 'post':
            return self.__session.post(
                url     = url, 
                data    = data,
                params  = params,
                headers = headers, 
                cookies = cookies, 
                timeout = timeout,
                allow_redirects = allow_redirects
            )
        else:
            return 'Requests method error'

    def __login(self) -> None:
        """
        Login function
        :param self.__mobile:
        :param self.__password:
        """
        resp = self.req(
            method='post',
            url='https://mobile.yiban.cn/api/v4/passport/login',
            data={
                'ct'       : '2',
                'identify' : '1',
                'mobile'   : self.__mobile,
                'password' : self.__encrypt_rsa(self.__password),
            }
        ).json()
        # print(resp)
        if resp['response'] == 100:
            self.__name = resp['data']['user']['name']
            self.__access_token = resp['data']['access_token']
            self.log_msg("Login successd")
        else:
            error_msg = f"Login error {resp['message']}"
            self.log_msg(error_msg, 40)
            raise Exception(error_msg)

    def __reauth(self) -> None:
        """
        Reauth function
        """
        self.log_msg('Task not found, try to reauth', level=30)
        client_id = '95626fa3080300ea'
        redirect_uri = 'https://f.yiban.cn/iapp7463'
        self.req(
            url='https://oauth.yiban.cn/code/html',
            params={'client_id': client_id, 'redirect_uri': redirect_uri}
        )
        self.req(
            method='post',
            url='https://oauth.yiban.cn/code/usersure', 
            data={'client_id': client_id, 'redirect_uri': redirect_uri},
        )
        # print(resp)
        time.sleep(1)
        self.__auth()

    def __auth(self, count=0):
        # auth
        while count <= 3:
            resp = self.req(
                url='http://f.yiban.cn/iapp/index', 
                params={'act': 'iapp7463'},
                cookies={'loginToken': self.__access_token},
                allow_redirects=False
            )
            verify = re.findall(r"verify_request=(.*?)&", resp.headers.get("Location"))[0]
            resp = self.req(
                url='https://api.uyiban.com/base/c/auth/yiban', 
                params={'verifyRequest': verify, 'CSRF': self.__csrf},
            )

            # get uncompleted task
            resp = self.req(
                url='https://api.uyiban.com/officeTask/client/index/uncompletedList', 
                params={
                    'StartTime': (datetime.datetime.now()+datetime.timedelta(days=-14)).strftime('%Y-%m-%d'),
                    'EndTime': time.strftime("%Y-%m-%d 23:59", time.localtime()),
                    'CSRF': self.__csrf
                }
            ).json()

            # if task data not found
            # certification has expired, try to reauth
            # self.log_msg(resp)
            if resp['data'] is None:
                count+=1
                self.__reauth()
            else:
                return resp['data']

        error_msg = 'Auth error'
        self.log_msg(error_msg, level=40)
        raise Exception(error_msg)

    def get_submit_data(self, task_data: dict) -> dict:
        """
        Task function
        if found uncompleted task return task_data else return task list
        :param submit_data:
        
        """
        self.log_msg('Get submit data')
        task_list = []
        try:
            task_data = json.loads(task_data)
            print("json_load")
        except:
            pass
        for t in task_data['Extend']['content']:
            if t['label'] == '任务名称':
                task_title = t['value'] # task tittle

        task_uncompleted = self.__auth()
        for i in task_uncompleted:
            task_list.append(i['Title'])
        
        if len(task_list) == 0:
            self.log_msg('All task completed')
            return None
        else:
            # get wfid taskid
            for i in task_uncompleted:
                if i['Title'] == task_title:
                    task_data['Extend']['TaskId'] = i['TaskId']
                    task_data['WFId'] = self.req(
                        url='https://api.uyiban.com/officeTask/client/index/detail', 
                        params={'TaskId': i['TaskId'], 'CSRF': self.__csrf}
                    ).json()['data']['WFId']
                    return task_data

    def submit_task(self, task_data: dict) -> dict:
        """

        return: {'name': self.__name, 'code': resp['code'], 'msg': resp['msg']}

        task_data example:
        {
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
        """
        result_msg = {'name': self.__name, 'code': 0, 'msg': ''}
        try:
            submit_data = task_data.copy() # copy dict 
        except:
            error_msg = "task data error"
            self.log_msg(error_msg, 40)
            raise Exception(error_msg)

        submit_data = self.get_submit_data(submit_data)
        if submit_data == None:
            result_msg['msg'] = '无打卡任务'
            return result_msg
        submit_data['Data'] = json.dumps(submit_data['Data'], ensure_ascii=False)
        submit_data['Extend'] = json.dumps(submit_data['Extend'], ensure_ascii=False)
        submit_data = self.__encrypt_aes(json.dumps(submit_data, ensure_ascii=False))
        resp = self.req(
            method='post',
            url='https://api.uyiban.com/workFlow/c/my/apply',
            params={'CSRF': self.__csrf},
            data={'Str': submit_data}
        ).json()
        # print(resp)
        if resp['code'] == 0:
            self.log_msg(resp)
            self.log_msg('Submit succeed')
            resp['msg'] = '打卡成功'
        else:
            # Error
            self.log_msg(resp['msg'])
            result_msg['msg'] = result_msg['msg']

        return result_msg
    
    def __encrypt_rsa(self, data):
        """
        Login password encrypt function
        """
        rsa_key = '''-----BEGIN PUBLIC KEY-----
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
        data = bytes(data, encoding="utf8") 
        encrypt = PKCS1_v1_5.new(RSA.importKey(rsa_key))
        sencrypt = b64encode(encrypt.encrypt(data))
        return sencrypt.decode("utf-8")

    def __encrypt_aes(self, data):
        """
        Submit data encrypt function
        """
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

if __name__ == '__main__':
    Yiban('mobile', 'password').submit_task()
