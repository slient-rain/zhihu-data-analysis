#!/usr/bin/env python
#  -*- coding: utf-8 -*-

'''
    该类通过多进程方式抓取网知乎用户信息
'''
import traceback

from UserData import  UserData
import datetime,time,random
from multiprocessing import  Pool
import os
from DAO import UserDataDAO ,Level3UserDataDAO
from Log import  FinalLogger
def proxy(cls_instance, i):
    return cls_instance.get_user_data(i)

def proxy3(cls_instance, i):
    return cls_instance.get_user_data(i)


class ParallelFetch:
    PROCESSNUM = 4 #并行计算进程数，最大为16

    #Master进程，获取第一节点的关注人url，然后分配给Worker进程去抓取相应用户的用户信息
    def multi_process_get_user_data(self):
        print 'Master process  %s.' % os.getpid() ,'start to get user url list'
        level1_user_url = "http://www.zhihu.com/people/zheng-li-jiu"
        level1_user_data = UserData(level1_user_url)
        level2_user_set = level1_user_data.getFollowees()


        i = 0
        level2_user_list=[]
        for i in range(self.PROCESSNUM):
            level2_user_list.append([])

        for level2_user in level2_user_set:
            if i%self.PROCESSNUM==0:
                level2_user_list[0].append(level2_user)
            elif i%self.PROCESSNUM==1:
                level2_user_list[1].append(level2_user)
            elif i%self.PROCESSNUM==2:
                level2_user_list[2].append(level2_user)
            elif i%self.PROCESSNUM==3:
                level2_user_list[3].append(level2_user)
            elif i%self.PROCESSNUM==4:
                level2_user_list[4].append(level2_user)
            elif i%self.PROCESSNUM==5:
                level2_user_list[5].append(level2_user)
            elif i%self.PROCESSNUM==6:
                level2_user_list[6].append(level2_user)
            elif i%self.PROCESSNUM==7:
                level2_user_list[7].append(level2_user)
            elif i%self.PROCESSNUM==8:
                level2_user_list[8].append(level2_user)
            elif i%self.PROCESSNUM==9:
                level2_user_list[9].append(level2_user)
            elif i % self.PROCESSNUM == 10:
                level2_user_list[10].append(level2_user)
            elif i % self.PROCESSNUM == 11:
                level2_user_list[11].append(level2_user)
            elif i % self.PROCESSNUM == 12:
                level2_user_list[12].append(level2_user)
            elif i % self.PROCESSNUM == 13:
                level2_user_list[13].append(level2_user)
            elif i % self.PROCESSNUM == 14:
                level2_user_list[14].append(level2_user)
            else :
                level2_user_list[15].append(level2_user)
            i+=1
        #
        result_set=[]
        user_list = []
        starttime = datetime.datetime.now()

        print 'Master process  %s.' % os.getpid(), 'start to create process pool and distribute task'
        p=Pool(self.PROCESSNUM)
        for i in range(self.PROCESSNUM):
            result_set.append(p.apply_async(proxy , args=(self,level2_user_list[i],)))
        p.close()
        p.join()
        for result in result_set:
            user_list.extend(result.get())

        endtime = datetime.datetime.now()
        print '计算时间(秒)：  ', (endtime - starttime).seconds
        for user in user_list:
            user.toString()
        print self.get_validated_user_num(user_list)


    #worker进程，根据Master进程分配的url列表去抓取相应用户的用户信息，并保存到数据库中
    def get_user_data(self,level2_user_queue):
        print 'Worker process  %s.' % os.getpid(), 'start to get %d user url' % len(level2_user_queue)
        user_list=[]
        i=0
        for level2_user in level2_user_queue:
            level2_user_data = UserData(level2_user.user_url)
            if(level2_user_data.getAnswerNum()!=-1 and level2_user_data.getAgreeNum()!=-1 and level2_user_data.getThanksNum()!=-1 and level2_user_data.getFolloweeNum()!=-1 and level2_user_data.getFollowerNum()!=-1):
                user_list.append(level2_user_data)
            i += 1
            # level3_user_set=level2_user_data.getFollowees()
            # for level3_user in level3_user_set:
            #    level3_user_data=UserData(level3_user.user_url)
            #    userList.append(level3_user_data)
        dao = UserDataDAO()
        dao.addMany(user_list)
        return user_list


    def get_validated_user_num(self,user_list):
        count = 0
        for user in user_list:
            if user.getFolloweeNum() != -1:
                count += 1
        return count

class Level3ParallelFetch:
    PROCESSNUM = 1 #并行计算进程数，最大为16

    #Master进程从数据库中提取level2用户信息，分配Worker进程，让worker分别去抓取level3用户的用户信息
    def multi_process_get_user_data(self):
        print 'Master process  %s.' % os.getpid(), 'start to start worker process'
        dao=UserDataDAO()
        level2_user_data_set=dao.queryAll()

        p = Pool(1)
        for level2_user_data in level2_user_data_set:
            p.apply_async(proxy3, args=(self, level2_user_data,))

        p.close()
        p.join()

        # for level2_user in level2_user_data_set:
        #     if i % self.PROCESSNUM == 0:
        #         level2_user_list[0].append(level2_user)
        #     elif i % self.PROCESSNUM == 1:
        #         level2_user_list[1].append(level2_user)
        #     elif i % self.PROCESSNUM == 2:
        #         level2_user_list[2].append(level2_user)
        #     elif i % self.PROCESSNUM == 3:
        #         level2_user_list[3].append(level2_user)
        #     elif i % self.PROCESSNUM == 4:
        #         level2_user_list[4].append(level2_user)
        #     elif i % self.PROCESSNUM == 5:
        #         level2_user_list[5].append(level2_user)
        #     elif i % self.PROCESSNUM == 6:
        #         level2_user_list[6].append(level2_user)
        #     elif i % self.PROCESSNUM == 7:
        #         level2_user_list[7].append(level2_user)
        #     elif i % self.PROCESSNUM == 8:
        #         level2_user_list[8].append(level2_user)
        #     elif i % self.PROCESSNUM == 9:
        #         level2_user_list[9].append(level2_user)
        #     elif i % self.PROCESSNUM == 10:
        #         level2_user_list[10].append(level2_user)
        #     elif i % self.PROCESSNUM == 11:
        #         level2_user_list[11].append(level2_user)
        #     elif i % self.PROCESSNUM == 12:
        #         level2_user_list[12].append(level2_user)
        #     elif i % self.PROCESSNUM == 13:
        #         level2_user_list[13].append(level2_user)
        #     elif i % self.PROCESSNUM == 14:
        #         level2_user_list[14].append(level2_user)
        #     else:
        #         level2_user_list[15].append(level2_user)
        #     i += 1



        # for level2_user in level2_user_list[0] :
        #     # print level2_user
        #     level2_user_url=level2_user[2]
        #     print 'start to get user url  %s followee' % level2_user_url
        #     level2_user_data = UserData(level2_user_url)
        #     level3_user_set = level2_user_data.getFollowees()
        #
        #     level3_user_data_list=[]
        #     starttime = datetime.datetime.now()
        #     index=0
        #     i=0
        #     for level3_user in level3_user_set:
        #         level3_user_data=UserData(level3_user.user_url)
        #         if level3_user_data.getAnswerNum() != -1 and level3_user_data.getAgreeNum() != -1 and level3_user_data.getThanksNum() != -1 and level3_user_data.getFolloweeNum() != -1 and level3_user_data.getFollowerNum() != -1:
        #             level3_user_data_list.append(level3_user_data)
        #             i+=1
        #         # time.sleep(random.randint(0,2))
        #         index+=1
        #         print index
        #     print 'Worker process  %s.' % os.getpid(), 'has got user url  %s all  %d followee,start to store them' % (level2_user_url,i)
        #     endtime = datetime.datetime.now()
        #     print '计算时间(秒)：  ', (endtime - starttime).seconds
        #     level3dao = Level3UserDataDAO()
        #     level3dao.addMany(level3_user_data_list)
        #     level3dao.add(level2_user_data)
        #     print 'Worker process  %s.' % os.getpid(), 'has stored user url  %s all %d followee,and start to delete it from leve2_user_data database' % (level2_user_url,i)
        #     dao=UserDataDAO()
        #     dao.deleteById(level2_user[0])
        #     print 'Worker process  %s.' % os.getpid(), 'has finish deleting  leve2_user_data '


        # p=Pool(1)
        # for i in range(self.PROCESSNUM):
        #     p.apply_async(proxy3 , args=(self,level2_user_list[i]))
        # p.close()
        # p.join()




    #worker进程，按条提取level2 user 的url，然后抓取相应用户的关注着信息保存，并将level2 user的信息存入level3数据库中，并从level2数据库中删除相应记录
    def get_user_data(self,level2_user):
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
            print 'Worker process  %s.' % os.getpid(), 'has got user url  %s all  %d followee,start to store them' % (level2_user_url,i)
            endtime = datetime.datetime.now()
            print '计算时间(秒)：  ', (endtime - starttime).seconds
            level3dao = Level3UserDataDAO()
            level3dao.addMany(level3_user_data_list)
            level3dao.add(level2_user_data)
            print 'Worker process  %s.' % os.getpid(), 'has stored user url  %s all %d followee,and start to delete it from leve2_user_data database' % (level2_user_url,i)
            dao=UserDataDAO()
            dao.deleteById(level2_user[0])
            print 'Worker process  %s.' % os.getpid(), 'has finish deleting  leve2_user_data '
        except:
            s = traceback.format_exc()
            s += ('error url is %s' % self.user_url)
            print s
            logger=FinalLogger.getLogger()
            logger.error(s)
            time.sleep(10)





