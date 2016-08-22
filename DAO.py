#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import MySQLdb
from DBUtil import DBUtil

class UserDataDAO:
    #按条添加纪录
    def add(self,userData):
        flag=False

        conn=None
        cur=None

        try:
            conn=DBUtil.getConnection()
            cur=conn.cursor()
            conn.select_db('zhihu')

            sql="insert into level2_user_data (name,url,agreenum,thanksnum,answernum,followeenum,followernum) values(%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(sql,(userData.getName(),userData.getUrl(),userData.getAgreeNum(),userData.getThanksNum(),userData.getAnswerNum(),userData.getFolloweeNum(),userData.getFollowerNum()))

            conn.commit()
            DBUtil.closeAll(conn,cur)

        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    #添加多条记录
    def addMany(self,userDataset):
        flag=False

        conn=None
        cur=None
        list=[]
        for userData in userDataset:
            list.append((userData.getName(),userData.getUrl(),userData.getAgreeNum(),userData.getThanksNum(),userData.getAnswerNum(),userData.getFolloweeNum(),userData.getFollowerNum()))

        try:
            conn=DBUtil.getConnection()
            cur=conn.cursor()
            conn.select_db('zhihu')

            sql="insert into level2_user_data (name,url,agreenum,thanksnum,answerNum,followeenum,followernum) values(%s,%s,%s,%s,%s,%s,%s)"
            cur.executemany(sql,list)

            conn.commit()
            DBUtil.closeAll(conn,cur)

        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])


    #查询所有纪录
    def queryAll(self):

        conn=None
        cur=None

        try:
            conn=DBUtil.getConnection()
            cur=conn.cursor()
            conn.select_db('zhihu')

            sql="select * from level2_user_data "
            num=cur.execute(sql)

            list=cur.fetchall()

            conn.commit()
            DBUtil.closeAll(conn,cur)


            return list

        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    # 按顺序查询一条纪录
    def query(self):

        conn = None
        cur = None

        try:
            conn = DBUtil.getConnection()
            cur = conn.cursor()
            conn.select_db('zhihu')

            sql = "select * from level2_user_data "
            num = cur.execute(sql)

            list = cur.fetchone()

            conn.commit()
            DBUtil.closeAll(conn, cur)

            return list

        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    def deleteById(self,id):

        conn = None
        cur = None

        try:
            conn = DBUtil.getConnection()
            cur = conn.cursor()
            conn.select_db('zhihu')

            sql = "delete from level2_user_data where id=%s"
            cur.execute(sql, (id,))
            conn.commit()
            DBUtil.closeAll(conn, cur)

        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

class Level3UserDataDAO:
    #按条添加纪录
    def add(self,userData):
        flag=False

        conn=None
        cur=None

        try:
            conn=DBUtil.getConnection()
            cur=conn.cursor()
            conn.select_db('zhihu')

            sql="insert into level3_user_data (name,url,agreenum,thanksnum,answernum,followeenum,followernum) values(%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(sql,(userData.getName(),userData.getUrl(),userData.getAgreeNum(),userData.getThanksNum(),userData.getAnswerNum(),userData.getFolloweeNum(),userData.getFollowerNum()))

            conn.commit()
            DBUtil.closeAll(conn,cur)

        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    #添加多条记录
    def addMany(self,userDataset):
        flag=False

        conn=None
        cur=None
        list=[]
        for userData in userDataset:
            list.append((userData.getName(),userData.getUrl(),userData.getAgreeNum(),userData.getThanksNum(),userData.getAnswerNum(),userData.getFolloweeNum(),userData.getFollowerNum()))

        try:
            conn=DBUtil.getConnection()
            cur=conn.cursor()
            conn.select_db('zhihu')

            sql="insert into level3_user_data (name,url,agreenum,thanksnum,answerNum,followeenum,followernum) values(%s,%s,%s,%s,%s,%s,%s)"
            cur.executemany(sql,list)

            conn.commit()
            DBUtil.closeAll(conn,cur)

        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])


    #查询所有纪录
    def queryAll(self):

        conn=None
        cur=None

        try:
            conn=DBUtil.getConnection()
            cur=conn.cursor()
            conn.select_db('zhihu')

            sql="select * from level3_user_data "
            num=cur.execute(sql)

            list=cur.fetchall()

            conn.commit()
            DBUtil.closeAll(conn,cur)


            return list

        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    # 按顺序查询一条纪录
    def query(self):

        conn = None
        cur = None

        try:
            conn = DBUtil.getConnection()
            cur = conn.cursor()
            conn.select_db('zhihu')

            sql = "select * from level3_user_data "
            num = cur.execute(sql)

            list = cur.fetchone()

            conn.commit()
            DBUtil.closeAll(conn, cur)

            return list

        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])


class UserUrlDAO:
    # 添加多条记录
    def addMany(self, userUrlset):
        flag = False

        conn = None
        cur = None

        try:
            list=[]
            for url in userUrlset:
                list.append((url,))
            conn = DBUtil.getConnection()
            cur = conn.cursor()
            conn.select_db('zhihu')

            sql = "insert into urlset (url) values(%s)"
            print list
            cur.executemany(sql, list)

            conn.commit()
            DBUtil.closeAll(conn, cur)

        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])


    #查询所有纪录
    def queryAll(self):

        conn=None
        cur=None

        try:
            conn=DBUtil.getConnection()
            cur=conn.cursor()
            conn.select_db('zhihu')

            sql="select * from urlset"
            num=cur.execute(sql)

            list=cur.fetchall()

            conn.commit()
            DBUtil.closeAll(conn,cur)


            return list

        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])