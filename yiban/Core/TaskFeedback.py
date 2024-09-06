#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Sricor, Moozae
# @Date: 2022-10-28

""" TaskFeedback Class """

from json import dumps
from time import strftime, localtime, time
from datetime import datetime, timedelta
from logging import log

from yiban.Core import SchoolBased
from yiban.Core.BaseReq import BaseReq


class TaskFeedback:
    def __init__(self, req: BaseReq):
        self.req = req

    def get_uncompleted_task(self) -> list[dict]:
        """获取未完成任务"""
        response = self.req.get(
            url="https://api.uyiban.com/officeTask/client/index/uncompletedList",
            params={
                "StartTime": (datetime.now() + timedelta(days=-14)).strftime(
                    "%Y-%m-%d"
                ),
                "EndTime": strftime("%Y-%m-%d 23:59", localtime()),
                "CSRF": SchoolBased.csrf(),
            },
        ).json()

        if response["code"] == 0:
            return response["data"]
        else:
            raise Exception(f"Get Uncompleted Tasks Error {response['msg']}")

    def get_completed_task(self) -> list[dict]:
        """获取已完成任务"""
        response = self.req.get(
            url="https://api.uyiban.com/officeTask/client/index/completedList",
            params={
                "StartTime": (datetime.now() + timedelta(days=-14)).strftime(
                    "%Y-%m-%d"
                ),
                "EndTime": strftime("%Y-%m-%d 23:59", localtime()),
                "CSRF": SchoolBased.csrf(),
            },
            headers=SchoolBased.headers(),
        ).json()

        if response["code"] == 0:
            return response["data"]
        else:
            raise Exception(f"Get School Based Completed Tasks Error {response['msg']}")

    def get_sign_task(self) -> dict:
        """获取晚点签到任务"""
        response = self.req.get(
            url="https://api.uyiban.com/nightAttendance/student/index/signPosition",
            params={"CSRF": SchoolBased.csrf()},
            headers=SchoolBased.headers(),
        ).json()

        if response["code"] == 0:
            return response["data"]["Range"]
        else:
            raise Exception(f"Get Night Attendance Sign Tasks Error {response['msg']}")

    def get_task_id(self, task_title) -> str | None:
        """
        获取未完成任务中的 TaskId （以任务标题形式）
        :param task_title: （必须）任务标题
        :return:
        """
        for i in self.get_uncompleted_task():
            if i["Title"] == task_title:
                return i["TaskId"]

        # 未找到任务
        return None

    def get_task_wf_id(self, task_id) -> str:
        """
        获取任务 WFId
        :param task_id: （必须）任务ID
        :return: str | None
        """
        response = self.req.get(
            url="https://api.uyiban.com/officeTask/client/index/detail",
            params={"TaskId": task_id, "CSRF": SchoolBased.csrf()},
        ).json()

        log(10, f"Get Task WFId Response {response}")

        if response["code"] == 0:
            return response["data"]["WFId"]
        else:
            raise Exception(f"Get Task WFId Error {response['msg']}")

    def submit_task(self, data: dict) -> bool | None:
        """
        :param data: （必须）任务提交表单
        :return: Bool Result
        :return: None 无未打卡任务
        """
        # 任务列表为空 无未完成任务
        if len(self.get_uncompleted_task()) == 0:
            return None

        task_title = ""  # 任务标题
        task_data = data.copy()  # 为避免对实参修改

        for i in task_data["Extend"]["content"]:
            if i["label"] == "任务名称":
                task_title = i["value"]

        task_id = self.get_task_id(task_title)  # 通过任务标题获取 TaskId

        if task_id is None:
            return False

        task_wf_id = self.get_task_wf_id(task_id)  # 通过 TaskId 获取 WFId

        task_data["WFId"] = task_wf_id
        task_data["Extend"]["TaskId"] = task_id
        task_data["Data"] = dumps(task_data["Data"], ensure_ascii=False)
        task_data["Extend"] = dumps(task_data["Extend"], ensure_ascii=False)
        task_data = SchoolBased.aes_encrypt(dumps(task_data, ensure_ascii=False))

        response = self.req.post(
            url="https://api.uyiban.com/workFlow/c/my/apply",
            params={"CSRF": SchoolBased.csrf()},
            data={"Str": task_data},
        ).json()

        if response["code"] == 0:
            return response["data"]
        else:
            raise Exception(f"Submit Task Error {response['msg']}")

    def submit_sign(self, data: str) -> str:
        """
        提交晚点签到任务
        :param data: （必须）签到提交表单
        :return: str Result
        """
        # 到达签到时间 开始签到
        time_range = self.get_sign_task()
        if time_range["StartTime"] < time() < time_range["EndTime"]:
            push_data = {
                "Code": "",
                "PhoneModel": "",
                "SignInfo": data,
                "OutState": "1",
            }
            response = self.req.post(
                url="https://api.uyiban.com/nightAttendance/student/index/signIn",
                params={"CSRF": SchoolBased.csrf()},
                data=push_data,
            ).json()
            print(response)
            if response["code"] == 0 and response["data"] is True:
                return "签到成功"
            else:
                return response["msg"]
        # 未到签到时间 无需签到
        else:
            return "签到失败 未到签到时间"


# 任务信息接口
# url = 'https://api.uyiban.com/officeTask/client/index/detail'
# {
#     'code': 0,
#     'msg': '',
#     'data': {
#         'Id': '',
#         'Title': '',
#         'Type': 1, 'ReceiverSendBack': 0,
#         'TypeId': '',
#         'AllowSendBackHours': 0,
#         'AllowSendBackTimes': 1,
#         'PubOrgName': '',
#         'PubPersonName': '',
#         'AllowTimeout': 1,
#         'AttachmentIds': '[]',
#         'PubOrgId': '',
#         'IsPubPersonShow': 1,
#         'CreateTime': 1656172805,
#         'StartTime': 1656172800,
#         'EndTime': 1656230400,
#         'Displayed': 1,
#         'TimeState': 1,
#         'WFId': '',
#         'AttachmentList': [],
#         'WorkflowState': 0,
#         'InitiateId': '',
#         'RetreatReason': '',
#         'EvaluationState': 0,
#         'EvaluationReason': '',
#         'State': 'uncompleted',
#         'RecordState': 0,
#         'CanSendBack': 0,
#         'SendBackEndTime': 1656230400,
#         'IsLost': 0,
#         'Feedback': 0,
#         'ChangeReason': ''
#     }
# }

# 获取未完成任务接口信息
# url = 'https://api.uyiban.com/officeTask/client/index/uncompletedList'
# {
#     'code': 0,
#     'msg': '',
#     'data': [
#         {
#             'TaskId': '',
#             'OrgId': '',
#             'TimeoutState': 1,
#             'State': 0,
#             'Title': '',
#             'Type': 1,
#             'StartTime': 0,
#             'EndTime': 0
#         }
#     ]
# }

# 获取完成任务接口信息
# url = 'https://api.uyiban.com/officeTask/client/index/completedList'
# {
#     'code': 0,
#     'msg': '',
#     'data': [
#         {
#             "TaskId": "",
#             "State": 2,
#             "OrgId": "",
#             "FeedbackTime": ,
#             "Title": "",
#             "Type": 1,
#             "StartTime": ,
#             "EndTime":
#         }
#     ]
# }

# 获取晚点签到任务接口
# url = 'https://api.uyiban.com/nightAttendance/student/index/signPosition'
# {
#     'code': 0,
#     'msg': '',
#     'data': {
#         'State': 1,
#         'Msg': '',
#         'OutState': '',
#         'Remark': '',
#         'FileUrl': '',
#         'Type': '',
#         'Position': [
#             {
#                 'Id': '',
#                 'UniversityId': '',
#                 'Campus': '',
#                 'BuildingId': ,
#                 'Type': '',
#                 'Title': '',
#                 'Address': '',
#                 'LngLat': '',
#                 'Range': 0,
#                 'MapType': 2,
#                 'Points': [

#                 ],
#                 'AddressName': '',
#                 'CreateTime':
#             }
#         ],
#         'Range': {
#             'StartTime': ,
#             'EndTime': ,
#             'SignDay': 1,
#             'RelatType': '1',
#             'RelatTimeType': '2'
#         },
#         'IsNeedPhoto': 2,
#         'AttachmentFileName': ''
#     }
# }

# 提交表单接口信息
# url = 'https://api.uyiban.com/workFlow/c/my/apply'
# {
#     'code': 0,
#     'msg': '',
#     'data': ''
# }

# 提交签到接口信息
# url='https://api.uyiban.com/nightAttendance/student/index/signIn'
# {
#     'code': 0,
#     'msg': '',
#     'data': ''
# }
