#!/usr/bin/env python
#-*- coding:utf-8 -*-
import traceback

from Log import FinalLogger
from user import User
#entity 类
class UserData2:
    _name=None
    _url=None
    _followeeNum=None
    _followerNum=None
    _anserNum=None
    _agreeNum=None
    _thanksNum=None
    def __init__(self, user_url=None,name=None,followeeNum=None,followerNum=None,anserNum=None,agreeNum=None,thanksNum=None):

                self._url = user_url
                self._name = name
                self._followeeNum = followeeNum
                self._followerNum = followerNum
                self._anserNum = anserNum
                self._agreeNum = agreeNum
                self._thanksNum=thanksNum



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

