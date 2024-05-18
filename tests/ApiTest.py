import logging

import TestConfig

from yiban import Yiban

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

yb = Yiban("test", "password")
logging.info(yb.task_feedback.get_sign_task())
# logging.info(yb.submit_task_feedback())