from json import dumps
from typing import Dict, List

from yiban.Core import SchoolBased

class EpidemicPrevention:
    def __init__(self, req):
        self.req = req

    def get_uncompleted_task(self) -> List[Dict]:
        response = self.req.get(
            url='https://api.uyiban.com/epidemicPrevention/client/index/notFinishWork',
            params={ 'CSRF': SchoolBased.csrf() }
        ).json()
        if response['code'] == 0:
            return response['data']

    def get_completed_task(self, page=1) -> None:
        response = self.req.get(
            url='https://api.uyiban.com/epidemicPrevention/client/index/allWork',
            params={
                'page': page,
                'IsApply': 2,
                'pageSize': 20,
                'CSRF': SchoolBased.csrf()
            }
        ).json()
        if response['code'] == 0:
            return response['data']
    
    def get_wf_process_id(self, wfid) ->None:
        response= self.req.get(
            url='https://api.uyiban.com/workFlow/c/my/getProcessDetail',
            params={
                'WFId': wfid,
                'CSRF': SchoolBased.csrf()
            }
        ).json()


    def submit_task(self, title, data: Dict) -> int:
        task_title = title
        task_data = data.copy()
        tasks = self.get_uncompleted_task()

        if len(tasks) == 0: return None

        for i in tasks:
            if task_title == i['Title']:
                task_wf_id = i['WIFI']
                task_id = i['TaskId']

                task_data['WFId'] = task_wf_id
                task_data['Extend']['TaskId'] = task_id
                task_data['Data'] = dumps(task_data['Data'], ensure_ascii=False)
                task_data['Extend'] = dumps(task_data['Extend'], ensure_ascii=False)
                task_data['CustomProcess'] = dumps(task_data['CustomProcess'], ensure_ascii=False)
                task_data = SchoolBased.aes_encrypt(dumps(task_data, ensure_ascii=False))

                response = self.req.post(
                    url='https://api.uyiban.com/workFlow/c/my/apply',
                    params={'CSRF': SchoolBased.csrf()},
                    data={'Str': task_data},
                ).json()
                
                if response['code'] == 0:
                    return True
                else:
                    raise Exception(f"{response['msg']}")