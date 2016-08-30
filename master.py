#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import random, time, Queue
from multiprocessing.managers import BaseManager
import traceback

from UserData import  UserData
import datetime,time,random
from multiprocessing import  Pool
import os,json
from UserData2 import UserData2
from DAO import UserDataDAO ,Level3UserDataDAO
from Log import  FinalLogger
try:
    import cPickle as pickle
except ImportError:
    import pickle

# 发送任务的队列:
task_queue = Queue.Queue()
# 接收结果的队列:
result_queue = Queue.Queue()

# 从BaseManager继承的QueueManager:
class QueueManager(BaseManager):
    pass

# 把两个Queue都注册到网络上, callable参数关联了Queue对象:
QueueManager.register('get_task_queue', callable=lambda: task_queue)
QueueManager.register('get_result_queue', callable=lambda: result_queue)
# 绑定端口5000, 设置验证码'abc':
manager = QueueManager(address=('', 5000), authkey='abc')
# 启动Queue:
manager.start()

def dict2UserData( d):
    return UserData2( d['_url'], d['_name'], d['_followeeNum'], d['_followerNum'], d['_anserNum'], d['_agreeNum'], d['_thanksNum'])

def master():
    # 获得通过网络访问的Queue对象:
    task = manager.get_task_queue()
    result = manager.get_result_queue()

    print 'Master process  %s.' % os.getpid(), 'start to start worker process'
    dao=UserDataDAO()
    level2_user_data_set=dao.query()
    print level2_user_data_set
    task.put(level2_user_data_set)

    # 从result队列读取结果:
    print('Try get results...')

    r_pickle=result.get(timeout=180)
#    r=pickle.load(r_pickle)
#    print 'result %s' %r
    print(json.loads(r_pickle, object_hook=dict2UserData))

master()
