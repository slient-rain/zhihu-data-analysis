#!/usr/bin/env python
#-*- coding:utf-8 -*-
import traceback

from Log import FinalLogger
from user import User
#entity 类
class UserData:
    _name=None
    _url=None
    _followeeNum=None
    _followerNum=None
    _anserNum=None
    _agreeNum=None
    _thanksNum=None
    def __init__(self, user_url):
        try:

                user=User(user_url)
                self._url=user_url
                self._name=user.get_user_id()
                self._followeeNum=user.get_followees_num()
                self._followerNum=user.get_followers_num()
                self._anserNum=user.get_answers_num()
                self._agreeNum=user.get_agree_num()
                self._thanksNum=user.get_thanks_num()


        except:
            s = traceback.format_exc()
            s += ('error url is %s' % self._url)
            print s
            logger=FinalLogger.getLogger()
            logger.error(s)


    def setName(self,name):
        self._name=name

    def setUrl(self,url):
        self._url=url

    def setFolloweeNum(self,feenum):
        self._followeeNum=feenum

    def setFollowerNum(self,fernum):
        self._followerNum=fernum

    def setAnswerNum(self,annum):
        self._anserNum=annum

    def setAgreeNum(self,agnum):
        self._agreeNum=agnum

    def setThanksNum(self,tnum):
        self._thanksNum=tnum

    def getName(self):
        return self._name

    def getUrl(self):
        return self._url

    def getFolloweeNum(self):
        return self._followeeNum

    def getFollowerNum(self):
        return self._followerNum

    def getAnswerNum(self):
        return self._anserNum

    def getAgreeNum(self):
        return self._agreeNum

    def getThanksNum(self):
        return self._thanksNum

    def toString(self):
        print 'name:  ' , self._name , '  followeeNum:  ' , self._followeeNum , \
                '  followerNum:  ' , self._followerNum , '  answerNum  ' , self._anserNum , \
                '  agreeNum:  ' , self._agreeNum , ' thanksNum:  ' , self._thanksNum


    def getFollowees(self):
        user = User(self._url)
        return user.get_followees()


    def getFollowers(self):
        user = User(self._url)
        return user.get_followers()

    #标准写法是这样的，Python语言特定的序列化模块是pickle，但如果要把序列化搞得更通用、更符合Web标准，就可以使用json模块
    # def dict2UserData(d):
    #     return UserData(d['url'], d['name'], d['thanksnum'])

