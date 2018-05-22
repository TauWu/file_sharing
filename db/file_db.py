#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import time

import pymongo
import requests

MONGO_URI = 'localhost'
MONGO_DB = 'FileUser'
NAME = 'file'


class file_db(object):
    def __init__(self,user_name='',filename='',new_filename=''):
        self.mongo_uri = MONGO_URI
        self.mongo_db = MONGO_DB
        self.mongo_name = NAME
        self.user = user_name
        self.filename = filename
        self.new_filename = new_filename

    def open_db(self):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    
    def find_filename(self):
        try:
            quary = {'filename':self.filename}
            projectionFields = {'_id':False, 'user':True ,'filename':True} 
            responses = self.db[self.mongo_name].find_one(quary,projection = projectionFields)
            return responses
        except:
            return None

    def insert_filename(self):
        try:
            insert_item = {'user':self.user ,'filename':self.filename}
            self.db[self.mongo_name].insert(insert_item)
        except:
            print(error)
            pass

    def update_filename(self):
        item = {'user':self.user ,'filename':self.new_filename}
        updateFilter = {'filename': self.filename}
        updateRes = self.db[self.mongo_name].update_one(filter = updateFilter,update = {'$set': dict(item)})

    def delete_filename(self):
        try:
            quary = {'filename':self.filename}
            responses = self.db[self.mongo_name].find_one(quary)
            if responses:
                self.db[self.mongo_name].remove(quary)
                return 'successful delete '+self.filename
            else:
                return 'no such user'
        
        except:
            return 'delete failed'

def new_filename(name,filename): 
    db_connect = file_db(user_name = name , filename = filename)
    db_connect.open_db()
    if find_filename(filename):
        return 'user existed'
    else:
        db_connect.insert_filename()
        return 'successful create user '+name

def find_filename(filename):
    try:
        db_connect = file_db(filename = filename)
        db_connect.open_db()
        return db_connect.find_filename()
    except:
        return None


def change_filename(filename,new_filename):
    old_item = find_filename(filename)
    if old_item:
        db_connect = file_db(user_name =old_item['user'], filename = filename, new_filename = new_filename)
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
