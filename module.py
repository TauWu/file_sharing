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

        


def getfile(dir_name = ''):
    if dir_name :
        dir_name = '/'+dir_name
    else:
        dir_name = ''
    print(dir_name)
    print (os.getcwd())
    path1=os.getcwd()+'/uploadfile'+dir_name
    path2=os.getcwd()
    #跳转目录 跳转到下载文件的目录，获得下载文件目录里面的ｌｉｓｔ之后，然后再跳转出来
    os.chdir(path1)
    flist=os.listdir()
    print(flist)
    os.chdir(path2)
    print (os.getcwd())
    flist = sorted(flist , key = lambda x:os.path.splitext(x)[1])
    file_type = []
    for files in flist:
        file_type.append(os.path.splitext(files)[1])
        if os.path.splitext(files)[1] == []:
            files = os.path.abspath(os.path.dirname(path2))
    return flist,file_type

def isHavefile(filename):
    print (os.getcwd())
    path1=os.getcwd()+'/uploadfile'
    path2=os.getcwd()
    os.chdir(path1)
    flag=os.path.isfile(filename)
    os.chdir(path2)
    print (os.getcwd())
    return flag

if __name__ == '__main__':
    print(getfile())

