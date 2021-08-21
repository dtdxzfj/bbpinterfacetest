#!/anaconda3/envs/FEALPy/bin python3.8
# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @File: mylog.py
# @Author: ZFJ
# @Time: 4月 10, 2021
# ---

import logging
# import inspect
from tools.pathconfig import PathConfig


# '[%(asctime)s][%(levelname)s][%(filename)s][line:%(lineno)d]:%(message)s'
# 常用日志格式

class MyLog:
    # stack = inspect.stack()[0]  # 获取堆栈信息，返回一个可命名元组

    @classmethod
    def mylogger(cls):
        mylogger = logging.getLogger(__name__)
        mylogger.setLevel(logging.DEBUG)
        if not mylogger.handlers:
            filehandler = logging.FileHandler(PathConfig.logpath, mode='a', encoding='utf-8')
            filehandler.setLevel(logging.DEBUG)
            filehandler.setFormatter(
                logging.Formatter(f'[%(asctime)s][%(levelname)s][%(filename)s][line:%(lineno)d]:%(message)s'))
            mylogger.addHandler(filehandler)
            streamhandler = logging.StreamHandler()
            streamhandler.setLevel(logging.DEBUG)
            streamhandler.setFormatter(
                logging.Formatter('[%(asctime)s][%(levelname)s]:%(message)s'))
            # 需要借助logging的格式化输出对应数据
            mylogger.addHandler(streamhandler)
        return mylogger

    @classmethod
    def logdebug(cls, msg):
        cls.mylogger().debug(msg)
        # cls.mylogger().debug("[{}.{}:{}] {}".format(*cls.__get_call_info(), msg))

    @classmethod
    def loginfo(cls, msg):
        cls.mylogger().info(msg)
        # cls.mylogger().info("[{}-{}-{}] {}".format(cls.stack.filename, cls.stack.function, cls.stack.lineno, msg))

    @classmethod
    def logwarning(cls, msg):
        cls.mylogger().warning(msg)
        # cls.mylogger().warning("[{}.{}:{}] {}".format(*cls.__get_call_info(), msg))

    @classmethod
    def logerror(cls, msg):
        cls.mylogger().error(msg)
        # cls.mylogger().error("[{}.{}:{}] {}".format(*cls.__get_call_info(), msg))

    @classmethod
    def logcritical(cls, msg):
        cls.mylogger().critical(msg)
        # cls.mylogger().critical("[{}.{}:{}] {}".format(*cls.__get_call_info(), msg))

# if __name__ == '__main__':
#     MyLog.loginfo('loginfo')
#     MyLog.logdebug('logdebug')
#     MyLog.logwarning('logwarning')
