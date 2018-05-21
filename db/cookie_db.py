#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import time

import pymongo
import requests
import random
import string

MONGO_URI = 'localhost'
MONGO_DB = 'FileUser'
NAME = 'cookie'


class cookie_db(object):
    def __init__(self,user_name = '',cookie = ''):
        self.mongo_uri = MONGO_URI
        self.mongo_db = MONGO_DB
        self.mongo_name = NAME
        self.user = user_name
        self.cookie = cookie

    def open_db(self):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    
    def find_cookie(self):
        try:
            quary = {'cookie':self.cookie}
            projectionFields = {'_id':False, 'user':True ,'cookie':True} 
            responses = self.db[self.mongo_name].find_one(quary,projection = projectionFields)
            return responses
        except:
            return None

    def find_user(self):
        try:
            quary = {'user':self.user}
            projectionFields = {'_id':False, 'user':True ,'cookie':True} 
            responses = self.db[self.mongo_name].find_one(quary,projection = projectionFields)
            return responses
        except:
            return None

    def insert_user(self):
        try:
            insert_item = {'user':self.user ,'cookie':self.cookie}
            self.db[self.mongo_name].insert(insert_item)
        except:
            print(error)
            pass


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
    try:
        if user_message['cookie']:
            return user_message['user']
        else:
            return False
    except:
        return False


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
    #print(judge_cookie('6yh9zTmNKsqpwriC03cJ5Yg7vWFaXZnLUM8QeuHfDxj4V1PbGO'))
    #print(find_user_cookie('cxw'))
    #print(remove_cookie('cxw'))
    pass
