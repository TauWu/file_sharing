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
NAME = 'file'


class file_db(object):
    def __init__(self,user_name='',filename='',new_filename=''):
        self.mysql_host = MYSQLHOST
        self.port = PORT
        self.db_user = USER
        self.db_pwd = PASSWD
        self.db_name = DATABASENAME
        self.table_name = NAME
        self.user = user_name
        self.filename = filename
        self.new_filename = new_filename

    def open_db(self):
        self.conn = pymysql.connect(host=self.mysql_host, port=self.port, user=self.db_user, 
        passwd=self.db_pwd, db=self.db_name, charset='utf8')
        self.cursor = self.conn.cursor()


    
    def find_filename(self):
        try:
            sql = "select * from %s where filename = '%s'"
            self.cursor.execute(sql % (self.table_name,self.filename))
            return self.cursor.fetchall()
        except:
            return None
        finally:
            self.cursor.close()
            self.conn.close()

    def insert_filename(self):
        try:
            sql = "insert into %s(user,filename) values ('%s','%s')" % (self.table_name,self.user,self.filename)
            self.cursor.execute(sql)
            self.conn.commit()
            return self.cursor.fetchall()
        except Exception as e:
            print(e)
            pass
        finally:
            self.cursor.close()
            self.conn.close()

    def update_filename(self):
        try:
            sql = "update %s set filename = '%s' where filename = '%s'" % (self.table_name,self.new_filename,self.filename)
            self.cursor.execute(sql)
            self.conn.commit()
            return self.cursor.fetchall()
        except:
            return 'no such filename'
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



    def delete_filename(self):
        try:
            sql = "delete from %s where filename = '%s'" % (self.table_name,self.filename)
            self.cursor.execute(sql)
            self.conn.commit()
            return self.cursor.fetchall()
        except:
            return 'no such filename'
        finally:
            self.cursor.close()
            self.conn.close()

def new_filename(name,filename): 
    db_connect = file_db(user_name = name , filename = filename)
    db_connect.open_db()
    if find_filename(filename):
        return 'user existed'
    else:
        db_connect.insert_filename()
        return 'successful create filename '+filename
    

def find_filename(filename):
    try:
        db_connect = file_db(filename = filename)
        db_connect.open_db()
        return db_connect.find_filename()
    except:
        return None

def find_user_filename(user):
    try:
        db_connect = file_db(user_name= user)
        db_connect.open_db()
        return db_connect.find_filename()
    except:
        return None

def change_filename(filename,new_filename):
    old_item = find_filename(filename)
    if old_item:
        db_connect = file_db(user_name =old_item[0][0], filename = filename, new_filename = new_filename)
        db_connect.open_db()
        db_connect.update_filename()
        return 'successful change filename'
    else:
        return 'wrong filename'

def remove_filename(filename):
    db_connect = file_db(filename = filename)
    db_connect.open_db()
    a = input('delete user '+filename+' Y/N: ')
    if a == 'y' or a =='Y':
        return db_connect.delete_filename()

if __name__ == '__main__':
    print(new_filename('cxw','123456'))
    #print(judge_user('cxw','123456'))
    print(find_filename('123456'))
    print(change_filename('123456','1234'))
    print(remove_filename('1234'))
    pass
