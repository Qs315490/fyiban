from yiban.yiban import Yiban
import logging

config = {
    "Thread": False,

    "UserList":[
        {"name": "", "mobile": "", "password": ""}, 
    ],

    "SubmitData": {}
}

# DEBUG
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(level=20, format=LOG_FORMAT, datefmt=DATE_FORMAT)


# Test
mobile = ""
password = ""
yb = Yiban(mobile, password)

yb.uncompleted_task() # 未完成任务 list

msg = yb.helath_submit(config["SubmitData"])

print(msg)