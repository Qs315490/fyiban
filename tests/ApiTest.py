import logging

import TestConfig

from yiban import Yiban

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

yb = Yiban("", "")