import logging

class Base:
    def _print(self, msg:str)     -> None: print(msg)
    def _debug_msg(self, msg:str) -> None: logging.log(msg = msg, level = 10)
    def _log_msg(self, msg:str)   -> None: logging.log(msg = msg, level = 20)
    def _err_msg(self, msg:str)   -> None: logging.log(msg = msg, level = 30)