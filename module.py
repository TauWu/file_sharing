import os

import pymysql
from werkzeug.utils import secure_filename



def insert(user ,idea):
    db=pymysql.connect("localhost","root","root","test3")
    cursor=db.cursor()
    sql="insert into dosomething (user,idea) values ('{}','{}')".format(user,idea)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    db.close()

def getfile():
    print (os.getcwd())
    path1=os.getcwd()+'/uploadfile'
    path2=os.getcwd()
    #跳转目录 跳转到下载文件的目录，获得下载文件目录里面的ｌｉｓｔ之后，然后再跳转出来
    os.chdir(path1)
    flist=os.listdir()
    os.chdir(path2)
    print (os.getcwd())
    return flist

def isHavefile(filename):
    print (os.getcwd())
    path1=os.getcwd()+'/uploadfile'
    path2=os.getcwd()
    os.chdir(path1)
    flag=os.path.isfile(filename)
    os.chdir(path2)
    print (os.getcwd())
    return flag


