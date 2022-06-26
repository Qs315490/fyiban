from typing import Dict, List

from yiban.Core import STask


class Task:
    def __init__(self, access_token):
        self.task = STask(access_token)

    def get_uncompleted_task(self) -> List[Dict]:
        """获取未完成任务"""
        return self.task.get_uncompleted_task()

    def get_completed_task(self) -> List[Dict]:
        """获取已完成任务"""
        return self.task.get_completed_task()

    def submit_task(self, task_data: dict) -> bool:
        """
        校本化 打卡提交
        :param task_data: （必须）提交表单
        :return:
        """
        return self.task.submit_task(task_data)
