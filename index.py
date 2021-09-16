import time
import json
import requests
from yiban import Yiban

def main(data=None, extend=None):
    msg = time.strftime("%m-%d", time.localtime()) + '易班打卡:\n'
    with open('./config.json', 'rb') as r:
        f = json.load(r)
        passport = f['yiban']
        try:
            for i in passport:
                mobile = i['mobile']
                password = i['password']
                load = Yiban(mobile, password).main()
                msg = msg + load + '\n'
        except:
            msg = '打卡程序异常'
        finally:
            print(msg)
            key = '5HsZbJ6diroqy65hprHyNS'
            if key != '':
               send(key, msg)
                

def send(key, msg):
    """
    key: 密钥
    msg: 推送内容
    推送服务:
    bark
    """
    requests.get(f'https://api.day.app/{key}/{msg}')
    
if __name__=='__main__':
    main()