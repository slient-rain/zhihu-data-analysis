#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import MySQLdb
class DBUtil:
    @staticmethod
    def getConnection():
        conn=None
        try:
            conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='root',  port=3306,charset='utf8')
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return conn;

    @staticmethod
    def closeAll(conn,cur):
        try:
            if(conn != None) :
                conn.close()
            if(cur != None):
                cur.close()
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])