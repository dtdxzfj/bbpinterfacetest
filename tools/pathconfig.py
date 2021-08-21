#!/anaconda3/envs/FEALPy/bin python3.8
# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @File: pathconfig.py
# @Author: ZFJ
# @Time: 4月 10, 2021
# ---

# 存放对应的配置文件路径
import os


class PathConfig:
    basepath = os.path.dirname(os.path.split(__file__)[0])
    logpath = os.path.join(basepath, 'output', 'loginfo.txt')  # 操作日志路径
    excelpath = os.path.join(basepath, 'data.xlsx')  # excel文件路径
    configpath = os.path.join(basepath, 'config.ini')  # 配置文件路径
    loginpath = os.path.join(basepath, 'logininfo.ini')  # 登录信息文件路径

# if __name__ == "__main__":
#     print(PathConfig.basepath, PathConfig.logpath, PathConfig.configpath)
