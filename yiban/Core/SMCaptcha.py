import requests
from json import loads
from random import randint
from datetime import datetime
from time import time
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
from base64 import b64decode

host = "https://captcha1.fengkongcloud.cn"
jshost = "https://castatic.fengkongcloud.cn/"


class CryptoJS:
    @staticmethod
    def DESEncrypt(key: str, data: str):
        key_bytes = key.encode("utf-8")
        data_bytes = pad(data.encode("utf-8"), DES.block_size)
        chipher = DES.new(key_bytes, DES.MODE_ECB)
        back = chipher.encrypt(data_bytes)
        return back.hex()

    @staticmethod
    def DESDecrypt(key: str, data: str):
        key_bytes = key.encode("utf-8")
        data_bytes = bytes.fromhex(data)
        cipher = DES.new(key_bytes, DES.MODE_ECB)
        decrypted = cipher.decrypt(data_bytes)
        # return unpad(decrypted, DES.block_size).decode("utf-8")
        return decrypted.decode("utf-8")


class SMCaptcha:
    def __init__(self):
        self.session = requests.Session()
        self.organization = "IY3HadrRSlgwwKWo63gi"  # 数美后台查看
        self.product = "popup"
        self.appId = "Yiban_Web"
        self.mode = "select"
        self.width = 300
        self.captchaUuid = self.getCaptchaUuid()
        self.sdkver = "1.1.3"
        self.rversion = "1.0.4"
        self.channel = "DEFAULT"
        self.lang = "zh-cn"
        # register 后才有
        self.rid = ""
        self.k = ""
        self.l = ""

    def getCaptchaUuid(self):
        str_tmp = ""
        chars = "ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678"
        for _ in range(0, 18):
            str_tmp += chars[randint(0, len(chars) - 1)]
        date_time = datetime.now()
        date_time_str = date_time.strftime("%Y%m%d%H%M%S")
        return f"{date_time_str}{str_tmp}"

    def conf(self):
        params = {
            "model": self.mode,
            "channel": self.channel,
            "rversion": self.rversion,
            "captchaUuid": self.captchaUuid,
            "appId": self.appId,
            "organization": self.organization,
            "lang": self.lang,
            "sdkver": self.sdkver,
            "callback": "s",
        }
        back = self.session.get(f"{host}/ca/v1/conf", params=params)
        json_str = back.text[2:-1]
        json_obj = loads(json_str)
        return json_obj

    def download_sdk(self):
        back = self.conf()
        sdk_url = jshost + back["detail"]["js"]

    def register(self):
        params = {
            "captchaUuid": self.captchaUuid,
            "organization": self.organization,
            "callback": "s",
            "sdkver": self.sdkver,
            "rversion": self.rversion,
            "appId": self.appId,
            "channel": self.channel,
            "lang": self.lang,
            "model": self.mode,
            "data": "{}",
        }
        back = self.session.get(f"{host}/ca/v1/register", params=params)
        json_str = back.text[2:-1]
        json_obj: dict = loads(json_str)
        detail = json_obj["detail"]
        self.rid = detail["rid"]
        self.k = detail["k"]
        self.l = detail["l"]
        return json_obj

    def fverify(self):
        if self.rid == "":
            return ""
        params = {
            "rid": self.rid,
            "rversion": self.rversion,
            "sdkver": self.sdkver,
            "protocol": 180,
            "captchaUuid": self.captchaUuid,
            "ostype": "web",
            "act.os": "web_pc",
            "organization": self.organization,
            "callback": "s",
            "mp": "",
            "kq": "",
            "xy": "",
            "ww": "",
            "nu": "",
            "tb": "",
            "oc": "",
            "en": "",
            "jo": "",
            "dy": "",
            "mu": "",
            "qd": "",
        }
        self.session.get(f"{host}", params=params)

    def sm_select(self, data: list[list[int]]):
        """轨迹生成"""
        base_data = {}
        time_now = round(time() * 1000)
        for i in data:
            i[0] = int(i[0] / 300)
            i[1] = int(i[1] / 150)
            i.append(time_now)
            time_now += randint(100, 500)
        base_data["museData"] = data
        base_data["startTime"] = time_now - randint(800, 20000)
        base_data["endTime"] = data[-1][2]
        base_data["mouseEndX"] = (0,)
        base_data["trueWidth"] = (300,)
        base_data["trueHeight"] = (150,)
        base_data["selectData"] = data
        base_data["blockWidth"] = None
        return base_data

    def get_captcha(self):
        back = self.register()


def main():
    sm = SMCaptcha()
    sm.conf()
    sm.register()
    b64 = b64decode(sm.k)
    print(CryptoJS.DESDecrypt("sshummei", b64.hex()))


if __name__ == "__main__":
    main()
