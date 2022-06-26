from re import findall
from json import dumps
from time import strftime, localtime
from base64 import b64encode, b64decode
from datetime import datetime, timedelta
from typing import Dict, List, AnyStr, Any

from Crypto.Cipher import AES

from yiban.Core import BaseYiban


class STask(BaseYiban):
    def __init__(self, access_token):
        super().__init__()
        self._csrf = '00000'
        self._access_token = access_token
        try:
            self._auth()
        except Exception as e:
            self._log(msg=f"STask Instantiation Failed. {e}", level=40)

    @staticmethod
    def _headers() -> Dict:
        return {"Origin": "https://c.uyiban.com", "User-Agent": "Yiban", "AppVersion": "5.0"}

    def _cookies(self) -> Dict:
        return {'loginToken': self._access_token, 'csrf_token': self._csrf}

    def _re_auth(self, verify: str) -> None:
        """
        校本化应用重认证
        :param verify: ...
        :return:
        """
        client_id = '95626fa3080300ea'
        redirect_uri = 'https://f.yiban.cn/iapp7463'
        self.get(
            url='https://api.uyiban.com/base/c/auth/yiban',
            params={'verifyRequest': verify, 'CSRF': self._csrf},
            headers=self._headers(),
            cookies=self._cookies()
        )

        self.get(
            url='https://oauth.yiban.cn/code/html',
            params={'client_id': client_id, 'redirect_uri': redirect_uri},
            headers=self._headers(),
            cookies=self._cookies()
        )

        self.post(
            url='https://oauth.yiban.cn/code/usersure',
            data={'client_id': client_id, 'redirect_uri': redirect_uri},
            headers=self._headers(),
            cookies=self._cookies()
        )

    def _auth(self) -> None:
        """用户认证"""
        response = self.get(
            url='https://f.yiban.cn/iapp/index',
            params={'act': 'iapp7463'},
            allow_redirects=False,
            headers=self._headers(),
            cookies=self._cookies()
        )
        verify = findall(r"verify_request=(.*?)&", response.headers.get("Location"))[0]

        self._re_auth(verify)

        response = self.get(
            url='https://api.uyiban.com/base/c/auth/yiban',
            params={'verifyRequest': verify, 'CSRF': self._csrf},
            headers=self._headers(),
            cookies=self._cookies()
        ).json()
        self._log(f"Auth Response {response}", 10)

        if response['code'] == 0:
            return None
        else:
            raise Exception(f"Auth Error {response['msg']}")

    def get_uncompleted_task(self) -> List[Dict]:
        """
        获取未完成任务
        :return: [
            {
                'TaskId': '',
                'OrgId': '',
                'TimeoutState': 1,
                'State': 0,
                'Title': '任务标题',
                'Type': 1,
                'StartTime': 1656172800,
                'EndTime': 1656230400
            }
        ]
        """
        response = self.get(
            url='https://api.uyiban.com/officeTask/client/index/uncompletedList',
            params={
                'StartTime': (datetime.now() + timedelta(days=-14)).strftime('%Y-%m-%d'),
                'EndTime': strftime("%Y-%m-%d 23:59", localtime()),
                'CSRF': self._csrf},
            headers=self._headers(),
            cookies=self._cookies()
        ).json()

        self._log(f"Get Uncompleted Tasks Response: {response}", 10)

        if response['code'] == 0:
            return response['data']
        else:
            raise Exception(f"Get Uncompleted Tasks Error {response['msg']}")

    def get_completed_task(self) -> List[Dict]:
        """获取已完成任务"""
        response = self.get(
            url='https://api.uyiban.com/officeTask/client/index/completedList',
            params={
                     'StartTime': (datetime.now() + timedelta(days=-14)).strftime('%Y-%m-%d'),
                     'EndTime': strftime("%Y-%m-%d 23:59", localtime()),
                     'CSRF': self._csrf},
            headers=self._headers(),
            cookies=self._cookies()
        ).json()

        self._log(f"Get Completed Tasks Response: {response}", 10)

        if response['code'] == 0:
            return response['data']
        else:
            raise Exception(f"Get Completed Tasks Error {response['msg']}")

    def get_task_id(self, task_title) -> AnyStr | None:
        """
        获取未完成任务中的 TaskId （以任务标题形式 ）
        :param task_title: （必须）任务标题
        :return:
        """
        for i in self.get_uncompleted_task():
            if i['Title'] == task_title:
                return i['TaskId']

        """未找到任务"""
        return None

    def get_task_wf_id(self, task_id) -> AnyStr:
        """
        获取任务 WFId
        :param task_id: （必须）任务ID
        :return: AnyStr | None
        """
        response = self.get(
            url='https://api.uyiban.com/officeTask/client/index/detail',
            params={'TaskId': task_id, 'CSRF': self._csrf},
            headers=self._headers(),
            cookies=self._cookies()
        ).json()

        self._log(f"Get Task WFId Response {response}", 10)

        if response['code'] == 0:
            return response["data"]["WFId"]
        else:
            raise Exception(f"Get Task WFId Error {response['msg']}")

    def submit_task(self, data: Dict) -> bool | None:
        """
        :param data: （必须）任务提交表单
        :return: bool | None
        """
        # 任务列表为空 无未完成任务
        if len(self.get_uncompleted_task()) == 0:
            self._log('All Tasks Completed')
            return None

        task_title = ''          # 任务标题
        task_data = data.copy()  # 为避免对实参修改

        for i in task_data['Extend']['content']:
            if i['label'] == '任务名称':
                task_title = i['value']

        task_id = self.get_task_id(task_title)     # 通过任务标题获取 TaskId

        # 未找到任务
        if task_id is None:
            self._log(f"Task Title '{task_title}' Not Found")
            return False

        task_wf_id = self.get_task_wf_id(task_id)  # 通过 TaskId 获取 WFId

        task_data['WFId'] = task_wf_id
        task_data['Extend']['TaskId'] = task_id
        task_data['Data'] = dumps(task_data['Data'], ensure_ascii=False)
        task_data['Extend'] = dumps(task_data['Extend'], ensure_ascii=False)
        task_data = self.aes_encrypt(dumps(task_data, ensure_ascii=False))

        # 提交表单
        response = self.post(
            url='https://api.uyiban.com/workFlow/c/my/apply',
            params={'CSRF': self._csrf},
            data={'Str': task_data},
            headers=self._headers(),
            cookies=self._cookies()
        ).json()

        self._log(f"Submit Task Response: {response}", 10)

        if response['code'] == 0:
            return True
        else:
            raise Exception(f"Submit Task Error {response['msg']}")

    @staticmethod
    def aes_encrypt(data: Any) -> AnyStr:
        """
        提交表单加密
        :param data: （必须）提交表单数据
        :return: AnyStr
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

    @staticmethod
    def aes_decrypt(data: Any) -> AnyStr:
        """
        提交表单解密
        :param data: （必须）提交表单加密数据
        :return: AnyStr
        """
        aes_key = '2knV5VGRTScU7pOq'
        aes_iv = 'UmNWaNtM0PUdtFCs'
        aes_key = bytes(aes_key, 'utf-8')
        aes_iv = bytes(aes_iv, 'utf-8')
        data = b64decode(b64decode(data))
        cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
        decrypted = cipher.decrypt(data)
        return decrypted.decode('Utf-8')


"""
任务信息接口
url = 'https://api.uyiban.com/officeTask/client/index/detail'
{
    'code': 0, 
    'msg': '', 
    'data': {
        'Id': '', 
        'Title': '', 
        'Type': 1, 'ReceiverSendBack': 0, 
        'TypeId': '', 
        'AllowSendBackHours': 0, 
        'AllowSendBackTimes': 1, 
        'PubOrgName': '',
        'PubPersonName': '', 
        'AllowTimeout': 1,
        'AttachmentIds': '[]', 
        'PubOrgId': '', 
        'IsPubPersonShow': 1, 
        'CreateTime': 1656172805, 
        'StartTime': 1656172800, 
        'EndTime': 1656230400, 
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
        'SendBackEndTime': 1656230400, 
        'IsLost': 0, 
        'Feedback': 0, 
        'ChangeReason': ''
    }
}
"""

"""
获取未完成任务接口信息
url = 'https://api.uyiban.com/officeTask/client/index/uncompletedList'
{
    'code': 0, 
    'msg': '', 
    'data': [
        {
            'TaskId': '', 
            'OrgId': '', 
            'TimeoutState': 1, 
            'State': 0, 
            'Title': '', 
            'Type': 1, 
            'StartTime': 0, 
            'EndTime': 0
        }
    ]
}
"""

"""
获取完成任务接口信息
url = 'https://api.uyiban.com/officeTask/client/index/completedList'
{
    'code': 0, 
    'msg': '', 
    'data': [
        {
            "TaskId": "",
            "State": 2,
            "OrgId": "",
            "FeedbackTime": ,
            "Title": "",
            "Type": 1,
            "StartTime": ,
            "EndTime": 
        }
    ]
}
"""

"""
提交表单接口信息
url = 'https://api.uyiban.com/workFlow/c/my/apply'
{
    'code': 0, 
    'msg': '', 
    'data': ''
}
"""
