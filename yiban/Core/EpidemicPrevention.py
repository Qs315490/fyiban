#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Sricor
# @Date: 2022-10-25

""" EpidemicPrevention Class """

from json import dumps

from yiban.Core import SchoolBased
from yiban.Core.BaseReq import BaseReq

class EpidemicPrevention:
    def __init__(self, req: BaseReq):
        self.req = req

    def get_uncompleted_task(self) -> list[dict]:
        response:dict = self.req.get(
            url="https://api.uyiban.com/epidemicPrevention/client/index/notFinishWork",
            params={"CSRF": SchoolBased.csrf()},
        ).json()
        if response["code"] == 0:
            data:list[dict] = response["data"]
            return data

    def get_completed_task(self, page=1) -> None:
        response = self.req.get(
            url="https://api.uyiban.com/epidemicPrevention/client/index/allWork",
            params={
                "page": page,
                "IsApply": 2,
                "pageSize": 20,
                "CSRF": SchoolBased.csrf(),
            },
        ).json()
        if response["code"] == 0:
            return response["data"]

    def get_wf_process_id(self, wfid) -> None:
        response = self.req.get(
            url="https://api.uyiban.com/workFlow/c/my/getProcessDetail",
            params={"WFId": wfid, "CSRF": SchoolBased.csrf()},
        ).json()

    def submit_task(self, title, data: dict) -> int:
        task_title = title
        task_data = data.copy()
        tasks = self.get_uncompleted_task()

        if len(tasks) == 0:
            return 0

        for i in tasks:
            if task_title == i["Title"]:
                task_wf_id = i["WIFI"]
                task_id = i["TaskId"]

                task_data["WFId"] = task_wf_id
                task_data["Extend"]["TaskId"] = task_id
                task_data["Data"] = dumps(task_data["Data"], ensure_ascii=False)
                task_data["Extend"] = dumps(task_data["Extend"], ensure_ascii=False)
                task_data["CustomProcess"] = dumps(
                    task_data["CustomProcess"], ensure_ascii=False
                )
                task_data = SchoolBased.aes_encrypt(
                    dumps(task_data, ensure_ascii=False)
                )

                response = self.req.post(
                    url="https://api.uyiban.com/workFlow/c/my/apply",
                    params={"CSRF": SchoolBased.csrf()},
                    data={"Str": task_data},
                ).json()

                if response["code"] == 0:
                    return 0
                else:
                    raise Exception(f"{response['msg']}")
