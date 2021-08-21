#!/anaconda3/envs/FEALPy/bin python3.8
# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @File: opdas.py
# @Author: ZFJ
# @Time: 8月 15, 2021
# ---
# 参考网址：https://www.jianshu.com/p/47f66ff4ab7b

from collections import namedtuple
# 可命名元组，支持按属性搜索,
# 用法：namedtuple（‘名称’，【属性列表】），赋值给一个变量，这个变量可以与名称一致也可以不一致
# 实例：时间元组，或者csv中文件包含有项的属性和值得数据，护着sqllie的数据表
# fangzi =namedtuple('jiage',['mianji','weizhi','lougao','jishi'])
# wode  = fangzi(109,'tianjin',14,'sanshi')
# print(wode)
# print(wode.jishi) # 可以使用元组中的属性值来搜索
# print(wode[2]) # 也支持通过下滑数字来搜索
# wode._asdict() # 转化为顺序字典orderdict
from collections import deque
# 双端队列，又称双向队列，类似于c中的链表结构，可以从左边插入和取值，也可以从右边插入和取值
# 其他的属性，跟列表一样，也可以在啥双端队列上使用
# 用法：deque([12,3,4,],maxlen=10)，长度可以用于固定队列，队列满之后再次添加胡聪另一端弹出数据
# dq =deque([21,243,2,654,324,23423,42342])
# dq.append(112)
# dq.appendleft(4534)
# dq.pop()
# dq.popleft()
# # deque([12,3,4,],maxlen=10)


from collections import OrderedDict

# 有序字典，py3.6之后，字典基本都是有序的，有序字典可以保留添加的顺序
o = OrderedDict()
o['k1'] = 'v1'
o['k3'] = 'v3'
o['k2'] = 'v2'
# print(o)
oo = dict(k1=1, k3=2, k2=3)
# print(oo)
# 两个顺序是一样，是因为3.6之后保留添加顺序

from collections import ChainMap
# 多个字典聚合到一起，构成一个顺序队列，取值从前往后，优先取前面的值，不存在就往后取值

from collections import defaultdict
# 默认字典，字典初始化时如果对应的键不存在，就会报错，儿默认字典不会存在这个问题，会返回一个默认值
# defdict =defaultdict(int) # 创建时需要制定默认值得数据类型，int的默认值为0，list为空，
# defdic = defaultdict(lambda :'default')  # 也可以使用匿名函数制定默认值
# print(defdic['a'])

from collections import Counter
# # 字典的计数器，可以对可哈希对象的计数，键为数据，值为计算数量，用于统计数据中出现的个数，返回一个无序字典
# cou = Counter('wrsjkleiryewirqrioqwy24124yui24y1uidakjs')
# #传入需要计数的数据，返回一个Counter计数对象，支持转化为字典
# print(cou)  # 返回一个Counter计数对象，里面是一个字典
# print(dict(cou))  # 转为字典类型
# print(cou.most_common(3)) # 返回一个里元素列表，里面可以指定返回指定返回多少个数据，返回前三个最大的数据
# print(cou['e'])  # 支持按照元素取值，统计某个元素出现的次数
# cou.clear()  清除倍计算数据


import hashlib

# 所有函数都得手动打出，
aa = hashlib.md5('2131'.encode('utf-8'))  # 加盐算法，动态加盐，使用用户名或者编号动态生成，提高安全性
bb = hashlib.md5()
aa.update('ghjgj'.encode('utf-8'))
print(aa.hexdigest())  # 打印被编码之后的字符串
