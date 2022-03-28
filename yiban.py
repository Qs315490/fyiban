#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Sricor
# @Date: 2021-11-01

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

        user_info = self.login(mobile, password)
        self.name = user_info['name']
        self.access_token = user_info['access_token']
        # print(user_info)
    
    def req(self, url, method='get', cookies={}, headers={}, timeout=10, allow_redirects=True, **kwargs):
        time.sleep(1) # 增加请求延时，避免请求过快 Error104
        data = kwargs.get("data")
        params = kwargs.get("params")
        cookies.update({'csrf_token': self.csrf})
        headers.update({"Origin": "https://c.uyiban.com", "User-Agent": "Yiban", "AppVersion": "5.0"})
        if method == 'get':
            return self.session.get(
                url     = url, 
                data    = data,
                params  = params,
                headers = headers, 
                cookies = cookies, 
                timeout = timeout,
                allow_redirects = allow_redirects
            )
        elif method == 'post':
            return self.session.post(
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

    def login(self, mobile, password):
        resp = self.req(
            method= 'post',
            url = 'https://mobile.yiban.cn/api/v4/passport/login',
            data = {
                'ct':       '2',
                'identify': '1',
                'mobile':   mobile,
                'password': rsa_encrypt(RSA_KEY, password),
            }
        ).json()
        # print(resp)
        if resp['response'] == 100:
            name = resp['data']['user']['name']
            access_token = resp['data']['access_token']
            return {'name': name, 'access_token': access_token}
        else:
            raise Exception(f'Login Error: {mobile} Message: {resp["message"]}')
    
    def submit_task(self):
        with open('config.json', encoding='utf-8') as f:
            json_data = json.load(f)
        submit_data = json_data['SubmitData']  # 提交表单数据
        for t in submit_data['Extend']['content']:
            if t['label'] == '任务名称':
                task_title = t['value'] # 任务名称

        task_list = []    # 任务列表
        result_data = {'code': 0, 'name':self.name, 'msg': ''}  # 返回字典

        # 校本化认证
        resp = self.req(
            url='http://f.yiban.cn/iapp/index', 
            params={'act': 'iapp7463'},
            cookies={'loginToken': self.access_token},
            allow_redirects=False
        )
        verify = re.findall(r"verify_request=(.*?)&", resp.headers.get("Location"))[0]
        resp = self.req(
            url='https://api.uyiban.com/base/c/auth/yiban', 
            params={'verifyRequest': verify, 'CSRF': self.csrf},
        )

        # 获取未完成任务列表
        resp = self.req(
            url='https://api.uyiban.com/officeTask/client/index/uncompletedList', 
            params={
                'StartTime': (datetime.datetime.now()+datetime.timedelta(days=-14)).strftime('%Y-%m-%d'),
                'EndTime': time.strftime("%Y-%m-%d 23:59", time.localtime()),
                'CSRF': self.csrf
            }
        ).json()

        # 校本化认证过期，尝试重新验证
        if resp['data'] is None:
            client_id = '95626fa3080300ea'
            redirect_uri = 'https://f.yiban.cn/iapp7463'
            resp = self.req(
                method = 'get',
                url = 'https://oauth.yiban.cn/code/html',
                params = {'client_id': client_id, 'redirect_uri': redirect_uri}
            )
            resp = self.req(
                method = 'post',
                url = 'https://oauth.yiban.cn/code/usersure', 
                data = {'client_id': client_id, 'redirect_uri': redirect_uri},
            )
            result_data['msg'] = '校本化认证失败，请重试'
            return result_data
        
        # 遍历未完成任务列表
        for i in resp['data']:
            # 判断任务标题
            if i['Title'] == task_title:
                task_id = i['TaskId']
                submit_data['WFId'] = self.req(
                    url='https://api.uyiban.com/officeTask/client/index/detail', 
                    params={'TaskId': task_id, 'CSRF': self.csrf}
                ).json()['data']['WFId']
                submit_data['Extend']['TaskId'] = task_id
                submit_data['Data'] = json.dumps(submit_data['Data'], ensure_ascii=False)
                submit_data['Extend'] = json.dumps(submit_data['Extend'], ensure_ascii=False)
                postData = json.dumps(submit_data, ensure_ascii=False)

                resp = self.req(
                    method='post',
                    url='https://api.uyiban.com/workFlow/c/my/apply',
                    params={'CSRF': self.csrf},
                    data={'Str': aes_encrypt(AES_KEY, AES_IV, postData)}
                ).json()

                # 打卡成功
                if resp['code'] == 0:
                    result_data['code'] = 1
                    result_data['msg'] = '打卡成功'
                    return result_data
                # Error
                else:
                    result_data['msg'] = resp['msg']
                    return result_data
            else:
                task_list.append(i['Tittle'])
                result_data['task'] = task_list

        # 无未打卡任务或存在其他任务
        result_data['code'] = 2
        if len(task_list) == 0:
            result_data['msg'] = '无未打卡任务'
        else:
            result_data['msg'] = f'当前存在其他任务：{task_list}'
        return result_data

if __name__ == '__main__':
    task = Yiban('1', '1').submit_task()
    print(task)
    # Yiban('1', '1')
