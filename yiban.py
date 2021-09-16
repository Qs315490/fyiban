import re
import time
import json
import base64
import datetime
import requests
from urllib import parse
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5


class Yiban():
    def __init__(self, mobile, password) -> None:
        self.name = ''
        self.mobile = mobile
        self.password = self.doCrypto(password)
        self.CSRF = '000000'
        self.access_token = ''
        self.session = requests.session()
        self.reqCookie = {'csrf_token': self.CSRF}
        self.reqHeaders = {"Origin": "https://c.uyiban.com", "User-Agent": "Yiban-Pro", "AppVersion": "5.0"}

    def main(self):
        """
        执行函数
        重复5次
        :return: msg
        """
        i = 0
        while i <= 9:
            try:
                self.getToken()
                self.getAuth()
                return self.doSubmit()
            except:
                print(f"{self.mobile}：正在重试第{i}次")
                i += 1
                continue
        return (self.mobile + '：Error')

    def req(self, url, params=None, cookies=None):
        return self.session.get(url, params=params, cookies=cookies, headers=self.reqHeaders, timeout=3).json()

    def getToken(self):
        """
        登录函数
        请求成功json
        {
            "response": 100,
            "message": "请求成功",
            "is_mock": false,
            "data": {
                "user": {
                    "sex": "1", //性别
                    "name": "", //姓名
                    "nick": "nico", //昵称
                    "pic": {},
                    "user_id": 123456789,
                    "phone": "123456789",
                    "authority": "1",
                    "isSchoolVerify": false,
                    "school": {
                        "isVerified": false,
                        "schoolName": "易班体验大学",
                        "schoolId": 100,
                        "schoolOrgId": 2000000,
                        "collegeName": "",
                        "collegeId": 0,
                        "className": "",
                        "classId": 0,
                        "joinSchoolYear": "2021"
                    }
                },
                "access_token": "dc7910a9922d3d5f938130a1fdb8108b" //token
            }
        }
        """
        try:
            url = f'https://mobile.yiban.cn/api/v4/passport/login?mobile={self.mobile}&password={self.password}&ct=2&identify=1'
            resp = requests.post(url,headers=self.reqHeaders).json()
            self.access_token = resp['data']['access_token']
            self.name = resp['data']['user']['name']
            self.log("登录成功")
            #self.log(self.access_token)
        except KeyError:
            raise 'Error: getToken'

    def getAuth(self):
        """
        用户认证
        """
        try:
            """Verify"""
            url = 'http://f.yiban.cn/iapp/index?act=iapp7463'  # 校本化iapp7463
            resp = requests.session().get(url, cookies={'loginToken': self.access_token}, allow_redirects=False)
            verify = re.findall(r"verify_request=(.*?)&", resp.headers.get("Location"))[0]  # 正则verify
            #print(verify)


            """Auth"""
            url = 'https://api.uyiban.com/base/c/auth/yiban'
            params = {
                'verifyRequest': verify,
                'CSRF': self.CSRF,
            }
            resp = self.req(url, params, cookies=self.reqCookie)
            if resp['code'] != 0:  # 返回码为0则成功
                raise 'Error: getAuth'
            else:
                self.log("认证成功")

        except:
            raise 'Error: getAuth'

    def doSubmit(self):
        """
        打卡提交
        return: msg
        """
        url = 'https://api.uyiban.com/officeTask/client/index/uncompletedList'
        params = {
            "StartTime": self.getStartTime(),
            "EndTime": self.getEndTime(),
            "CSRF": self.CSRF,
        }
        resp = self.req(url, params, cookies=self.reqCookie)
        if resp['code'] != 0:
            raise 'Error: getTask'
        
        try:
            TaskId = resp['data'][0]['TaskId']
            url = 'https://api.uyiban.com/officeTask/client/index/detail'
            params = {
                'TaskId': TaskId,
                'CSRF': self.CSRF,
            }
            resp = self.req(url, params, cookies=self.reqCookie)
            WFId = resp['data']['WFId']

            with open('./config.json', 'rb') as r:
                f = json.load(r)
                data = f['data']
                extend = f['extend']
                if self.mobile == '18835903765':
                    data['769bbfbfb026629f1ddb0294a9c0d257'] = '山西省运城市新绛县横桥乡中村北'
                if self.mobile == '18553088858':
                    data['769bbfbfb026629f1ddb0294a9c0d257'] = '山东省菏泽市牡丹区曹州路市政府家属院11号楼'
                if self.mobile == '17508933571':
                    data['769bbfbfb026629f1ddb0294a9c0d257'] = '海南省昌江县石碌镇'
                if self.mobile == '13875324187':
                    data['769bbfbfb026629f1ddb0294a9c0d257'] = '湖南省益阳市桃江县松木塘镇'
                if self.mobile == '18169216537':
                    data['769bbfbfb026629f1ddb0294a9c0d257'] = '江西省宜春市万载县'
                extend['TaskId'] = TaskId
            data = json.dumps(data, ensure_ascii=False)
            extend = json.dumps(extend, ensure_ascii=False)


            url = f'https://api.uyiban.com/workFlow/c/my/apply/{WFId}?CSRF={self.CSRF}'
            data = {
                'data': data,
                'extend': extend,
            }
            resp = self.session.post(url, data, cookies=self.reqCookie, headers=self.reqHeaders).json()
            if resp['code'] == 0:
                return self.log("打卡成功")
            else:
                raise 'Error: doSubmit'
        except:
            return self.log("无未打卡信息")

    def log(self, msg):
        print(self.name +"："+msg)
        return self.name +"："+msg

    def getEndTime(self):
        return time.strftime("%Y-%m-%d 23:59", time.localtime())

    def getStartTime(self):
        now = datetime.datetime.now()
        delta = datetime.timedelta(days=-14)
        n_days = now + delta
        return n_days.strftime('%Y-%m-%d')

    def doCrypto(self, password):
        """
        v4接口
        密码加密
        Rsa,base64
        """
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
        return parse.quote(Sencrypt.decode("utf-8"))
