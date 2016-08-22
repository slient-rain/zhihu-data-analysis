#!/usr/bin/env python
#  -*- coding: utf-8 -*-
import MySQLdb
from UserData import  UserData
import datetime ,time ,random
from multiprocessing import  Pool
import os
from DAO import UserDataDAO
from ParallelFetch import  ParallelFetch

import sys


def main():
    # url='http://www.zhihu.com/people/wang-jing-de'
    # level1_user_data = UserData(url)
    # level1_user_data.toString()
    userList=[]
    level1_user_url = "http://www.zhihu.com/people/zheng-li-jiu"
    level1_user_data=UserData(level1_user_url)
    level2_use_set=level1_user_data.getFollowees()
    i=0
    starttime = datetime.datetime.now()
    for level2_user in level2_use_set:
        print i, '  ',level2_user.get_user_id(), '  ',level2_user.user_url
        level2_user_data=UserData(level2_user.user_url)
        userList.append(level2_user_data)
        # level3_user_set=level2_user_data.getFollowees()
        i += 1
        #for level3_user in level3_user_set:
        #    level3_user_data=UserData(level3_user.user_url)
        #    userList.append(level3_user_data)
    endtime = datetime.datetime.now()
    for user in userList:
        user.toString()
    print '计算时间(秒)：  ',(endtime - starttime).seconds

def multi_process_get_user_data():
    print 'Master process  %s.' % os.getpid() ,'start to get user url list'
    level1_user_url = "http://www.zhihu.com/people/zheng-li-jiu"
    level1_user_data = UserData(level1_user_url)
    level2_user_set = level1_user_data.getFollowees()
    list=[]
    list.append(level1_user_data)
    dao=UserDataDAO()
    dao.addMany(list)
    # PROCESSNUM=4
    # i = 0
    # level2_user_list=[]
    # for i in range(PROCESSNUM):
    #     level2_user_list.append([])
    #
    # for level2_user in level2_user_set:
    #     if i%PROCESSNUM==0:
    #         level2_user_list[0].append(level2_user)
    #     elif i%PROCESSNUM==1:
    #         level2_user_list[1].append(level2_user)
    #     elif i%PROCESSNUM==2:
    #         level2_user_list[2].append(level2_user)
    #     elif i%PROCESSNUM==3:
    #         level2_user_list[3].append(level2_user)
    #     elif i%PROCESSNUM==4:
    #         level2_user_list[4].append(level2_user)
    #     elif i%PROCESSNUM==5:
    #         level2_user_list[5].append(level2_user)
    #     elif i%PROCESSNUM==6:
    #         level2_user_list[6].append(level2_user)
    #     elif i%PROCESSNUM==7:
    #         level2_user_list[7].append(level2_user)
    #     elif i%PROCESSNUM==8:
    #         level2_user_list[8].append(level2_user)
    #     elif i%PROCESSNUM==9:
    #         level2_user_list[9].append(level2_user)
    #     elif i % PROCESSNUM == 10:
    #         level2_user_list[10].append(level2_user)
    #     elif i % PROCESSNUM == 11:
    #         level2_user_list[11].append(level2_user)
    #     elif i % PROCESSNUM == 12:
    #         level2_user_list[12].append(level2_user)
    #     elif i % PROCESSNUM == 13:
    #         level2_user_list[13].append(level2_user)
    #     elif i % PROCESSNUM == 14:
    #         level2_user_list[14].append(level2_user)
    #     else :
    #         level2_user_list[15].append(level2_user)
    #     i+=1
    # #
    # result_set=[]
    # user_list = []
    # starttime = datetime.datetime.now()
    #
    # print 'Master process  %s.' % os.getpid(), 'start to create process pool and distribute task'
    # p=Pool(PROCESSNUM)
    # for i in range(PROCESSNUM):
    #     result_set.append(p.apply_async(get_user_data , args=(level2_user_list[i],)))
    # p.close()
    # p.join()
    # for result in result_set:
    #     user_list.extend(result.get())
    #
    # endtime = datetime.datetime.now()
    # print '计算时间(秒)：  ', (endtime - starttime).seconds
    # for user in user_list:
    #     user.toString()
    # print get_validated_user_num(user_list)

def get_validated_user_num(user_list):
    count = 0
    for user in user_list:
        if user.getFolloweeNum() != -1:
            count += 1
    return count

def get_user_data(level2_user_queue):
    print 'Worker process  %s.' % os.getpid(), 'start to get %d user url' % len(level2_user_queue)
    user_list=[]
    i=0
    for level2_user in level2_user_queue:
        level2_user_data = UserData(level2_user.user_url)
        user_list.append(level2_user_data)
        i += 1
        # level3_user_set=level2_user_data.getFollowees()
        # for level3_user in level3_user_set:
        #    level3_user_data=UserData(level3_user.user_url)
        #    userList.append(level3_user_data)
    dao = UserDataDAO()
    dao.addMany(user_list)
    return user_list

if __name__ == '__main__':
    # multi_process_get_user_data()
    p =ParallelFetch()
    p.multi_process_get_user_data()
    # print sys.getdefaultencoding()

