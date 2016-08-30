#!/usr/bin/env python
#  -*- coding: utf-8 -*-

# taskworker.py

import time, sys, Queue
from multiprocessing.managers import BaseManager
import traceback

from UserData import  UserData
import datetime,time,random
from multiprocessing import  Pool
import os
#from DAO import UserDataDAO ,Level3UserDataDAO
from Log import  FinalLogger
try:
    import cPickle as pickle
except ImportError:
    import pickle
import json
# 创建类似的QueueManager:
class QueueManager(BaseManager):
    pass

# 由于这个QueueManager只从网络上获取Queue，所以注册时只提供名字:
QueueManager.register('get_task_queue')
QueueManager.register('get_result_queue')

# 连接到服务器，也就是运行taskmanager.py的机器:
server_addr = '52.78.135.36'
print('Connect to server %s...' % server_addr)
# 端口和验证码注意保持与taskmanager.py设置的完全一致:
m = QueueManager(address=(server_addr, 5000), authkey='abc')
# 从网络连接:
m.connect()
# 获取Queue的对象:
task = m.get_task_queue()
result = m.get_result_queue()

level2_user=task.get(timeout=10)
print 'get level2 user %s successfully' %level2_user[2]
#worker进程，按条提取level2 user 的url，然后抓取相应用户的关注着信息保存，并将level2 user的信息存入level3数据库中，并从level2数据库中删除相应记录
def get_user_data(level2_user):
    try:
        level2_user_url=level2_user[2]
        print 'Worker process  %s.' % os.getpid(), 'start to get user url  %s followee' % level2_user_url
        level2_user_data = UserData(level2_user_url)
        level3_user_set = level2_user_data.getFollowees()
        level3_user_data_list=[]
        starttime = datetime.datetime.now()
        index=0#抓取用户信息计数器
        i=0#有效用户信息计数器
        for level3_user in level3_user_set:
            print index
            level3_user_data=UserData(level3_user.user_url)
            if level3_user_data.getAnswerNum() != -1 and level3_user_data.getAgreeNum() != -1 and level3_user_data.getThanksNum() != -1 and level3_user_data.getFolloweeNum() != -1 and level3_user_data.getFollowerNum() != -1:
                level3_user_data_list.append(level3_user_data)
                i+=1
            # time.sleep(random.randint(0,3))
            index+=1
        print 'Worker process  %s.' % os.getpid(), 'has got user url  %s all  %d followee,start to return them to master' % (level2_user_url,i)
        endtime = datetime.datetime.now()
        print '计算时间(秒)：  ', (endtime - starttime).seconds
        return level3_user_data_list
    except:
        s = traceback.format_exc()

        print s
        logger=FinalLogger.getLogger()
        logger.error(s)
        time.sleep(10)
    return

res=get_user_data(level2_user)
res_pickle=json.dumps(res, default=lambda obj: obj.__dict__)
result.put(res_pickle)

# 处理结束:
print('worker exit.')
