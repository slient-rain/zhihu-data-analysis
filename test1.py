#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import traceback
from Log import FinalLogger
from UserData import  UserData
import datetime,time,random
from multiprocessing import  Pool
import logging
from auth import Logging
import os
from DAO import UserDataDAO ,Level3UserDataDAO
import matplotlib ,os
from UserData import UserData
matplotlib.use('Qt4Agg')
import matplotlib.pyplot as plt
from  numpy import *
from DAO import Level3UserDataDAO ,UserDataDAO,UserUrlDAO
from Statistics import Stats
# from ParallelFetch import ParallelFetch
# 写数据进程执行的代码:
def write(q):
    for value in ['A', 'B', 'C']:
        print 'Put %s to queue...' % value
        q.put(value)
        time.sleep(random.random())

# 读数据进程执行的代码:
def read(q):
    i=0
    while True:
        value = q.get(True)
        print 'Get %s from queue.' % value
        i+=1
        if(i==3):
            return [1,2,3]



def draw():

    plt.plot([1, 2, 3, 4], [1, 4, 9, 16], 'ro')
    plt.axis([0, 6, 0, 20])
    plt.show()
    plt.savefig(r'e:/MyFig.jpg')

def proxy(cls_instance, i):
    return cls_instance.get_user_data(i)

class ParallelFetch:
    PROCESSNUM = 1 #并行计算进程数，最大为16

    #Master进程，获取第一节点的关注人url，然后分配给Worker进程去抓取相应用户的用户信息
    def multi_process_get_user_data(self):
        print 'Master process  %s.' % os.getpid() ,'start to work'
        p=Pool(self.PROCESSNUM)
        for i in range(10):
            p.apply_async(proxy , args=(self,i,))
        p.close()
        p.join()



    #worker进程，根据Master进程分配的url列表去抓取相应用户的用户信息，并保存到数据库中
    def get_user_data(self,i):
        print ' Worker process  %s.' % i, 'start to work'
        # time.sleep(10)
        # Logging.error(u" Worker process  raise exception stop")
        # raise Exception(' Worker process  raise exception stop' )
        try:
            a=12/0
        except:
            s = traceback.format_exc()
            logger = FinalLogger.getLogger()
            print 'error'
            logger.error(s)

class excep_class:
    def __init__ (self):
        pass
    def except_fun (self):
        a=12
        b=0
        print(a/b)


def test():
    try:
        excep_class.except_fun(excep_class)
    except:
        s = traceback.format_exc()
        logger = FinalLogger.getLogger()
        s+='url'
        logger.error(s)
        return 'ok'
def proxy3(cls_instance, i):
    return cls_instance.get_user_data(i)


def get_user_data(level2_user):
    level3_user_set=set()
    try:
        level2_user_data = UserData(level2_user[2])
        level3_user_gen = level2_user_data.getFollowees()
        for level3_user in level3_user_gen:
            level3_user_set.add(level3_user.user_url)
    except:
        print '网页  ', level2_user[2], '未抓取完全，未获取到用户名'
        s = traceback.format_exc()
        s += ('error url is %s' % level2_user[2])
        logger = FinalLogger.getLogger()
        logger.error(s)
    return level3_user_set

if __name__=='__main__':
    pass
    level3_user_set=set()
    # level3_user_set.add("http;//")
    # level3_user_set.add("http;//1")
    # level3_user_set.add("http;//2")
    # level3_user_set.add("http;//3")
    dao = UserDataDAO()
    level2_user_data_set = dao.queryAll()
    for level2_user in level2_user_data_set:
        try:
            level2_user_data = UserData(level2_user[2])
            level3_user_gen = level2_user_data.getFollowees()
            for level3_user in level3_user_gen:
                level3_user_set.add(level3_user.user_url)
        except:
            s = traceback.format_exc()
            print s
            logger = FinalLogger.getLogger()
            logger.error(s)
            continue




    print level3_user_set
    urlDao=UserUrlDAO()
    urlDao.addMany(level3_user_set)