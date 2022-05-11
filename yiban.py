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
        >>> y = Yiban('account', 'password')
        >>> y.sunmit_task(task_data)

    """

    def __init__(self, mobile: str, password: str, name: str = '') -> None:
        self._name = name
        self._mobile = mobile
        self._password = password
        self._access_token = ''
        self._csrf = '000000'
        self._session = requests.session() # Keep alive
        self._login()

    def _error_msg(self, msg: str, level: int = 40) -> None:
        logging.log(msg=f"{self._name} {msg}", level=level)
        raise Exception (msg)

    def _log_msg(self, msg: str, level: int = 20) -> None:
        logging.log(msg=f"{self._name} {msg}", level=level)

    def _req(self, url: str, method: str = 'get', timeout: int = 10, allow_redirects: bool = True, **kwargs) -> requests :
        """
        Use requests.session() to construct request function
        Keep alive
        """
        time.sleep(2) # Increase request delay to avoid requests too fast Error104
        data = {}
        params = {}
        cookies = {'csrf_token': self._csrf}
        headers = {"Origin": "https://c.uyiban.com", "User-Agent": "Yiban", "AppVersion": "5.0"}
        if 'data' in kwargs:  data.update(kwargs.get("data"))
        if 'params' in kwargs:  params.update(kwargs.get("params"))
        if 'cookies' in kwargs:  cookies.update(kwargs.get("cookies"))
        if 'headers' in kwargs:  headers.update(kwargs.get("headers"))
        if method == 'get':
            return self._session.get(
                url     = url, 
                data    = data,
                params  = params,
                headers = headers, 
                cookies = cookies, 
                timeout = timeout,
                allow_redirects = allow_redirects
            )
        elif method == 'post':
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
            self._error('Requests method error')

    def _login(self) -> None:
        """ Login function """
        resp = self._req(
            url='https://mobile.yiban.cn/api/v4/passport/login',
            method='post',
            data={
                'ct'       : '2',
                'identify' : '1',
                'mobile'   : self._mobile,
                'password' : self._encrypt_rsa(self._password),
            }
        ).json()
        # print(resp)
        if resp['response'] == 100:
            self._name = resp['data']['user']['name']
            self._access_token = resp['data']['access_token']
            self._log_msg("Login successd")
        else:
            self._error_msg(f"Login error {self._mobile} {resp['message']}")

    def _reauth(self, count) -> None:
        """ Reauth function """
        self.log_msg('Task not found, try to reauth', level=30)
        client_id = '95626fa3080300ea'
        redirect_uri = 'https://f.yiban.cn/iapp7463'
        self._req(
            url='https://oauth.yiban.cn/code/html',
            params={'client_id': client_id, 'redirect_uri': redirect_uri}
        )
        self._req(
            method='post',
            url='https://oauth.yiban.cn/code/usersure', 
            data={'client_id': client_id, 'redirect_uri': redirect_uri},
        )
        # print(resp)
        time.sleep(1)
        self._auth(count)

    def _auth(self, count: int = 0) -> list:
        """ Auth function """
        while count < 3: # retry three times
            # auth
            resp = self._req(
                url='http://f.yiban.cn/iapp/index', 
                params={'act': 'iapp7463'},
                cookies={'loginToken': self._access_token},
                allow_redirects=False
            )
            verify = re.findall(r"verify_request=(.*?)&", resp.headers.get("Location"))[0]
            resp = self._req(
                url='https://api.uyiban.com/base/c/auth/yiban', 
                params={'verifyRequest': verify, 'CSRF': self._csrf},
            )

            # get uncompleted task
            resp = self._req(
                url='https://api.uyiban.com/officeTask/client/index/uncompletedList', 
                params={
                    'StartTime': (datetime.datetime.now()+datetime.timedelta(days=-14)).strftime('%Y-%m-%d'),
                    'EndTime': time.strftime("%Y-%m-%d 23:59", time.localtime()),
                    'CSRF': self._csrf
                }
            ).json()

            # if task data not found
            # certification has expired, try to reauth
            # self._log_msg(resp)
            if resp['data'] is None:
                count += 1
                self._reauth(count)
            else:
                return resp['data'] # uncompleted task list
        self._error_msg('Auth error') # retry failed

    def _get_submit_data(self, task_data: dict) -> dict:
        """
        Task function
        if found uncompleted task return task_data else return task list
        :param submit_data:
        
        """
        task_uncompleted_list = self._auth()

        for t in task_data['Extend']['content']:
            if t['label'] == '任务名称':
                task_title = t['value'] # task tittle

        if len(task_uncompleted_list) == 0:
            self._log_msg('All task completed')
            return None
        else:
            # set taskdata
            # taskid wfid
            for i in task_uncompleted_list:
                if i['Title'] == task_title:
                    task_data['Extend']['TaskId'] = i['TaskId']
                    task_data['WFId'] = self._req(
                        url='https://api.uyiban.com/officeTask/client/index/detail', 
                        params={'TaskId': i['TaskId'], 'CSRF': self._csrf}
                    ).json()['data']['WFId']
                    return task_data

    def submit_task(self, submit_data: dict) -> dict:
        result_msg = {'name': self._name, 'code': 0, 'msg': ''}
        try:
            task_data = submit_data.copy() # copy dict 
        except:
            self._error_msg("Task data error")

        task_data = self._get_submit_data(task_data)
        if task_data == None:
            result_msg['msg'] = '无打卡任务'
            return result_msg
        task_data['Data'] = json.dumps(task_data['Data'], ensure_ascii=False)
        task_data['Extend'] = json.dumps(task_data['Extend'], ensure_ascii=False)
        task_data = self._encrypt_aes(json.dumps(task_data, ensure_ascii=False))
        resp = self._req(
            method='post',
            url='https://api.uyiban.com/workFlow/c/my/apply',
            params={'CSRF': self._csrf},
            data={'Str': task_data}
        ).json()
        # print(resp)
        if resp['code'] == 0:
            self._log_msg('Submit succeed')
            result_msg['msg'] = '打卡成功'
        else:
            # Error
            self._log_msg(resp['msg'])
            result_msg['msg'] = resp['msg']

        return result_msg

    def _encrypt_rsa(self, data):
        """ Login password encrypt function """
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

    def _encrypt_aes(self, data):
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

def submit(mobile: str, password: str, submit_data : dict, name: str = ''):
    return Yiban(mobile, password, name).submit_task(submit_data)

if __name__ == '__main__':
    Yiban('mobile', 'password').submit_task()
