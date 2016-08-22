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
            self.user=User(user_url)
            self._url=user_url
            self._name=self.user.get_user_id()
            self._followeeNum=self.user.get_followees_num()
            self._followerNum=self.user.get_followers_num()
            self._anserNum=self.user.get_answers_num()
            self._agreeNum=self.user.get_agree_num()
            self._thanksNum=self.user.get_thanks_num()
        except:
            s = traceback.format_exc()
            s += ('error url is %s' % self._url)
            print s
            logger=FinalLogger.getLogger()
            logger.error(s)

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
        return self.user.get_followees()


    def getFollowers(self):
        return self.user.get_followers()