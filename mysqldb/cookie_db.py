#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import time

import pymysql
import requests
import random
import string

MYSQLHOST = 'localhost'
PORT = 3306
USERER = 'root'
PASSWD = '123123'
DATABASENAME = 'FileUser'
NAME = 'cookie'


class cookie_db(object):

    def __init__(self,user_name = '',cookie = ''):
        self.mysql_host = MYSQLHOST
        self.port = PORT
        self.db_user = USERER
        self.db_pwd = PASSWD
        self.db_name = DATABASENAME
        self.table_name = NAME
        self.user = user_name
        self.cookie = cookie

    def open_db(self):
        self.conn = pymysql.connect(host=self.mysql_host, port=self.port, user=self.db_user, 
        passwd=self.db_pwd, db=self.db_name, charset='utf8')
        self.cursor = self.conn.cursor()


    
    def find_cookie(self):
        try:
            sql = "select * from %s where cookie = '%s'"
            self.cursor.execute(sql % (self.table_name,self.cookie))
            return self.cursor.fetchall()
        except:
            return None
        finally:
            self.cursor.close()
            self.conn.close()

    def find_user(self):
        try:
            sql = "select * from %s where user = '%s'"
            self.cursor.execute(sql % (self.table_name,self.user))
            return self.cursor.fetchall()
        except:
            return None
        finally:
            self.cursor.close()
            self.conn.close()            

    def insert_user(self):
        try:
            sql = "insert into %s(user,cookie) values ('%s','%s')" % (self.table_name,self.user,self.cookie)
            self.cursor.execute(sql)
            self.conn.commit()
            return self.cursor.fetchall()
        except:
            print('error')
            pass
        finally:
            self.cursor.close()

    def delete_user(self):
        try:
            sql = "delete from %s where user = '%s'" % (self.table_name,self.user)
            self.cursor.execute(sql)
            self.conn.commit()
            return self.cursor.fetchall()    
        except:
            return 'delete failed'


def new_cookie(name,cookie): 
    db_connect = cookie_db(user_name = name , cookie = cookie)
    db_connect.open_db()
    if find_user_cookie(name):
        db_connect.delete_user()
        db_connect.insert_user()
        return 'successful create user '+name
    else:
        db_connect.insert_user()
        return 'successful create user '+name

def find_user_cookie(name):
    try:
        db_connect = cookie_db(user_name = name)
        db_connect.open_db()
        return db_connect.find_user()
    except:
        return None

def find_cookie_user(cookie):
    try:
        db_connect = cookie_db(cookie = cookie)
        db_connect.open_db()
        return db_connect.find_cookie()
    except:
        return None

def judge_cookie(cookie):
    db_connect = cookie_db(cookie = cookie)
    db_connect.open_db()
    user_message = db_connect.find_cookie()
    print(user_message)
    try:
        if user_message[0][1]:
            return user_message[0][0]
        else:
            return False
    except:
        return ''


def remove_cookie(name):
    db_connect = cookie_db(user_name = name)
    db_connect.open_db()
    a = input('delete user '+name+' Y/N: ')
    if a == 'y' or a =='Y':
        return db_connect.delete_user()

def random_cookie():
    return ''.join(random.sample(string.ascii_letters+string.digits,50))


if __name__ == '__main__':
    a = random_cookie()
    print(new_cookie('cxw',a))
    print(judge_cookie('W9s1A2XDxCyKMiLqujUZzFpbEvn8eBo37SlOfcTadGk0Nr4Hg6'))
    print(find_user_cookie('cxw'))
    print(remove_cookie('cxw'))
    pass
