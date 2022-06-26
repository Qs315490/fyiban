import logging
from yiban import Yiban

task_data = {
    "WFId": "",
    "Data": {
        "9843754e97aad058523524bdb8991bcd": "否",
        "72fe9c2c81a48fd0968edbbb3f2c1c42": "36.5",
        "769bbfbfb026629f1ddb0294a9c0d257": "",
        "90b5b83950ae456fefebb0f751406e2d": [{
            "name": "348816E7-275F-42D8-9118-625FB45D8D48.png",
            "type": "image/png",
            "size ": 472092,
            "status": "done",
            "percent ": 100,
            "fileName": "workflow/202110/18/4c3599675b629e14e80ffe19c507b806.png ",
            "path": "workflow/202110/18/4c3599675b629e14e80ffe19c507b806.png "
        }],
        "0242914b8746275c5073ccdb156f9d1d": [{
            "name": "86E7DCB9-7FEE-441F-B921-039302A1048B.png",
            "type": "image/png",
            "size": 179394,
            "status": "done",
            "percent": 100,
            "fileName": "workflow/202110/23/30150ea922a720e7fb732eb7150cc532.png ",
            "path": "workflow/202110/23/30150ea922a720e7fb732eb7150cc532.png "
        }],
        "1bac180dd37455f7c16a36336c0411a8": {
            "time": "2022-05-20 00:00",
            "longitude": 0,
            "latitude": 0,
            "address": ""
        }
    },

    "Extend": {
        "TaskId": "",
        "title": "任务信息",
        "content": [
            {"label": "任务名称", "value": ""},
            {"label": "发布机构", "value": ""},
            {"label": "发布人", "value": ""}
        ]
    }
}

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

yb = Yiban()
yb.get_user_name()
yb.get_user_access_token()
yb.get_uncompleted_task()
yb.get_completed_task()
yb.submit_task(task_data)

