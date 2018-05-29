#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import time

import pymongo
import requests

MONGO_URI = 'localhost'
MONGO_DB = 'FileUser'
NAME = 'user'


class user_db(object):
    def __init__(self,user_name='',user_pwd = ''):
        self.mongo_uri = MONGO_URI
        self.mongo_db = MONGO_DB
        self.mongo_name = NAME
        self.user = user_name
        self.pwd = user_pwd

    def open_db(self):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    
    def find_user(self):
        try:
            quary = {'user':self.user}
            projectionFields = {'_id':False, 'user':True ,'pwd':True} 
            responses = self.db[self.mongo_name].find_one(quary,projection = projectionFields)
            return responses
        except:
            return None

    def insert_user(self):
        try:
            insert_item = {'user':self.user ,'pwd':self.pwd}
            self.db[self.mongo_name].insert(insert_item)
        except:
            print(error)
            pass

    def update_pwd(self):
        item = {'user':self.user ,'pwd':self.pwd}
        updateFilter = {'user': item['user']}
        updateRes = self.db[self.mongo_name].update_one(filter = updateFilter,update = {'$set': dict(item)})

    def delete_user(self):
        try:
            quary = {'user':self.user}
            responses = self.db[self.mongo_name].find_one(quary)
            if responses:
                self.db[self.mongo_name].remove(quary)
                return 'successful delete '+self.user
            else:
                return 'no such user'
        
        except:
            return 'delete failed'

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
    if user_message['pwd'] == pwd:
        return True
    else:
        return False

def change_pwd(name,pwd,new_pwd):
    db_connect = user_db(user_name = name,user_pwd = new_pwd)
    db_connect.open_db()
    user_message = db_connect.find_user()
    if user_message['pwd'] == pwd:
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
    #print(new_user('cxwc','123456'))
    #print(judge_user('cxwc','123456'))
    #print(find_user_mes('cxwc'))
    #print(change_pwd('cxwc','123456','1234'))
    #print(remove_user('cxwc'))
    pass
