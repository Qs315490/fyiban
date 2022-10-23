"""校本化 Api"""
from typing import Dict, List, AnyStr

from yiban.Core import SchoolBased
from yiban.Core import TaskFeedback
from yiban.Core import SchoolBasedAuth
from yiban.Core import EpidemicPrevention

class Task:
    def __init__(self, access_token):
        req = SchoolBasedAuth(access_token)._auth() 

        self.task_feedback = TaskFeedback(req)             # 任务反馈
        self.epidemic_prevention = EpidemicPrevention(req) # 疫情防控

    def get_task_feedback_completed_task(self):
        return self.task_feedback.get_completed_task()

    def get_task_feedback_uncompleted_task(self):
        return self.task_feedback.get_uncompleted_task()
    
    def submit_task_feedback(self, data):
        self.task_feedback.submit_task(data)

    def get_epidemic_prevention_uncompleted_task(self):
        return self.epidemic_prevention.get_uncompleted_task()

    def get_epidemic_prevention_completed_task(self):
        return self.epidemic_prevention.get_completed_task()

    def submit_epidemic_prevention(self, title, data):
        return self.epidemic_prevention.submit_task(title, data)


    @staticmethod
    def task_aes_encrypt(data):
        return SchoolBased.aes_encrypt(data)

    @staticmethod
    def task_aes_decrypt(data):
        return SchoolBased.aes_decrypt(data)