import re
import os
import time
import json
import base64
import requests
import datetime
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from submit import SubmitTask

CSRF = '000000'
COOKIE = {'csrf_token': CSRF}
HEADERS = {
	"Origin": "https://c.uyiban.com", 
	"User-Agent": "Yiban", 
	"AppVersion": "5.0"
}

def doCrypto(password):
    PUBLIC_KEY = '''-----BEGIN PUBLIC KEY-----
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
    encrypt = PKCS1_v1_5.new(RSA.importKey(PUBLIC_KEY))
    Sencrypt = base64.b64encode(encrypt.encrypt(bytes(password, encoding="utf8")))
    return Sencrypt.decode("utf-8")

def getStartTime():
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=-14)
    n_days = now + delta
    return n_days.strftime('%Y-%m-%d')

class Yiban():
    def __init__(self, mobile, password) -> None:
        self.result = {'code': 0, 'name': '', 'msg': ''}
        self.access_token = self.login(mobile, password)

    def login(self, mobile, password):
        resp = requests.post(
            url = 'https://mobile.yiban.cn/api/v4/passport/login',
            headers = {'AppVersion': '5.0'}, 
            data = {
            'mobile': mobile,
            'password': doCrypto(password),
            'ct': '2',
            'identify': '1'
            }
        ).json()
        if 'access_token' in resp['data']:
            self.result['name'] = resp['data']['user']['name']
            access_token = resp['data']['access_token']
            COOKIE['loginToken'] = access_token
            return access_token
        else:
            raise Exception('[Error]getToken')

    def submit_task(self, Str=None):
        """
        : param: Str 加密后提交数据
        打卡主函数
        暂未逆向解密js，此函数暂存
        """
        session = requests.session()
        try:
            resp = session.get(
                url = 'http://f.yiban.cn/iapp/index', 
                params = {'act': 'iapp7463'},
                headers = HEADERS,
                cookies = COOKIE,
                allow_redirects = False
            )
            verify = re.findall(r"verify_request=(.*?)&", resp.headers.get("Location"))[0]
            time.sleep(0.5)
            resp = session.get(
                url = 'https://api.uyiban.com/base/c/auth/yiban', 
                params = {'verifyRequest': verify, 'CSRF': CSRF},
                headers = HEADERS,
                cookies = COOKIE
            ).json()

        except Exception as e:
            self.result['msg'] = f'[Error]Auth: {e}'
            return self.result

        try:
            resp = session.get(
            url = 'https://api.uyiban.com/officeTask/client/index/uncompletedList', 
            params = {
                'StartTime': getStartTime(),
                'EndTime': time.strftime("%Y-%m-%d 23:59", time.localtime()),
                'CSRF': CSRF
            },
            headers = HEADERS,
            cookies = COOKIE).json()

            if resp['data'] is None:
                """
                校本化认证过期，尝试重新验证
                """
                resp = session.post(
                    url = 'https://oauth.yiban.cn/code/usersure', 
                    data = {'client_id': '95626fa3080300ea', 'redirect_uri': 'https://f.yiban.cn/iapp7463'} ,
                    headers = HEADERS,
                    cookies = COOKIE
                )
                time.sleep(5)
                raise Exception('认证失败')
            else:
                for t in resp['data']:
                    if t['Title'] == '每日学生疫情上报': # 打卡任务标题
                        taskid = t['TaskId']
                        wfid = session.get(
                            url = 'https://api.uyiban.com/officeTask/client/index/detail', 
                            params = {'TaskId': taskid, 'CSRF': CSRF},
                            headers = HEADERS,
                            cookies = COOKIE
                        ).json()['data']['WFId']
                        """
                        selenium自动化打卡, 返回提交对象
                        """
                        self.result['code'] = 1
                        self.result['data'] = self.subObject(
                            name = self.result['name'],
                            taskid = taskid,
                            wfid = wfid,
                            cookieValue = requests.utils.dict_from_cookiejar(session.cookies)['PHPSESSID']
                            )
                        return self.result
                        
                        """
                        requests提交请求，暂未解密js,暂存
                        resp = session.post(
                            url = f'https://api.uyiban.com/workFlow/c/my/apply',
                            params = {'CSRF': CSRF},
                            data = {'Str': Str}, 
                            headers = HEADERS,
                            cookies = COOKIE
                        ).json()         
                        if resp['code'] == 0:
                            self.result['code'] = 1
                            self.result['msg'] = '打卡成功'
                            return self.result
                        else:
                            self.result['msg'] = resp['msg']
                            return self.result               
                        """
                
                self.result['code'] = 2
                self.result['msg'] = '无未打卡任务'

        except Exception as e:
            self.result['msg'] = f'[Error]submitTask: {e}'

        finally:
            return self.result

    def subObject(self, name, taskid, wfid, cookieValue):
        """
        构造提交对象,转为selenium提交
        不同学校需要自行修改
        name: 名称
        location: 位置信息
        temperature: 体温
        cookieValue: PHPSESSID值
        journeyCode: 行程码图片路径 例如'C:/Users/Sricor/OneDrive/Data/img/1.jpg'
        healthCode: 健康码图片路径
        图片路径默认当前目录下xxx.jpg
        """
        path = os.path.dirname(__file__) # 获取当前文件目录
        data = {
            'name': name,  # 名称
            'unHealth': '否',  # 健康异常状态(非必须)
            'wfid': wfid,  # wfid
            'temperature': '36.5',  # 体温 默认36.5
            'location': '示例位置',  # 位置
            'journeyCode': os.path.join(path, 'journeyCode.jpg'),  # 行程码图片路径
            'healthCode': os.path.join(path, 'healthCode.jpg'),  # 健康码图片路径
            'cookie': {
                'name': 'PHPSESSID', 
                'value': cookieValue, 
                'domain': '.uyiban.com'},  # 登录状态cookie，只需要PHPSESSID
            'extend': {
                "TaskId": taskid, 
                "title": "任务信息", 
                "content": [
                    {"label": "任务名称", "value": "每日学生疫情上报"}, 
                    {"label": "发布机构", "value": "学生处"}, 
                    {"label": "发布人", "value": "邸灿"}
                    ]
                }, 
            }
        return data

if __name__ == '__main__':
    USER = [
        {"name": "", "mobile": "", "password": ""}, 
        {"name": "", "mobile": "", "password": ""}, 
    ]
    SubList = []
    for i in USER:
        try:
            # Code为0，程序未正常运行
            # Code为1，存在未打卡任务，构造data对象，存进预打卡列表
            # Code为2，未找到打卡任务，跳过
            # 若存在data 则添加到预打卡列表
            sub = Yiban(i['mobile'], i['password']).submit_task()
            print(sub)
            if 'data' in sub: 
                SubList.append(sub['data'])
        except:
            print(f"{i['name']}: Error")
            continue

    if len(SubList) != 0:
    	SubmitTask(SubList) # 转至自动化打卡
