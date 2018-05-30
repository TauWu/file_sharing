#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import time

import pymysql
import requests

MYSQLHOST = 'localhost'
PORT = 3306
USER = 'root'
PASSWD = '123123'
DATABASENAME = 'FileUser'
NAME = 'user'


class user_db(object):
    def __init__(self,user_name='',user_pwd = ''):
        self.mysql_host = MYSQLHOST
        self.port = PORT
        self.db_user = USER
        self.db_pwd = PASSWD
        self.db_name = DATABASENAME
        self.table_name = NAME
        self.user = user_name
        self.pwd = user_pwd

    def open_db(self):
        self.conn = pymysql.connect(host=self.mysql_host, port=self.port, user=self.db_user, 
        passwd=self.db_pwd, db=self.db_name, charset='utf8')
        self.cursor = self.conn.cursor()

    
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
            sql = "insert into %s(user,pwd) values ('%s','%s')" % (self.table_name,self.user,self.pwd)
            self.cursor.execute(sql)
            self.conn.commit()
            return self.cursor.fetchall()
        except:
            print('error')
            pass
        finally:
            self.cursor.close()
            self.conn.close()

    def update_pwd(self):
        try:
            sql = "update %s set pwd = '%s' where user = '%s'" % (self.table_name,self.pwd,self.user)
            self.cursor.execute(sql)
            self.conn.commit()
            return self.cursor.fetchall()
        except:
            return 'no such filename'
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
        finally:
            self.cursor.close()
            self.conn.close()

def new_user(name,pwd): 
    db_connect = user_db(user_name = name , user_pwd = pwd)
    db_connect.open_db()
    if find_user_mes(name):
        return 'user existed'
    else:
        db_connect.insert_user()
        os.mkdir('./uploadfile'+name)
        return 'successful create user '+name

def find_user_mes(name):
    try:
        db_connect = user_db(user_name = name)
        db_connect.open_db()
        return db_connect.find_user()
    except:
        return None

def judge_user(name,pwd):
    db_connect = user_db(user_name = name)
    db_connect.open_db()
    user_message = db_connect.find_user()
    if user_message[0][1] == pwd:
        return True
    else:
        return False

def change_pwd(name,pwd,new_pwd):
    db_connect = user_db(user_name = name,user_pwd = new_pwd)
    db_connect.open_db()
    user_message = db_connect.find_user()
    if user_message[0][1] == pwd:
        db_connect.update_pwd()
        return 'successful change pwd'
    else:
        return 'wrong pwd'

def remove_user(name):
    db_connect = user_db(user_name = name)
    db_connect.open_db()
    a = input('delete user '+name+' Y/N: ')
    if a == 'y' or a =='Y':
        return db_connect.delete_user()

if __name__ == '__main__':
    print(new_user('cq','123456'))
    print(new_user('lwz','123456'))
    #print(judge_user('cxwc','123456'))
    #print(find_user_mes('cxwc'))
    #print(change_pwd('cxwc','123456','1234'))
    print(remove_user('cq'))
    pass
