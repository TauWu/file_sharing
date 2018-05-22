
import os
from flask import Flask, render_template, request, send_from_directory, url_for,redirect,jsonify,abort,make_response,config,Blueprint
from module import *
from db.user_db import *
from db.cookie_db import *


app = Flask(__name__)

'''@app.route('/login',methods=['POST','get'])
def login():
    mycss=url_for('static', filename='style.css')
    return render_template('login.html',mycss=mycss)
'''
'''def relogin():
    mycss=url_for('static', filename='style.css')
    return render_template('relogin.html',mycss=mycss)
'''
#main页面


@app.route('/')
def hello():
    mycss=url_for('static', filename='style.css')
    res = request.cookies.get('name_cookie_save')
    try:
        if judge_cookie(res):
            return redirect('/up')
        else:
            return redirect('/login')
    except:
        pass

@app.route('/login', methods=['POST','get'])
def login_in():
    mycss=url_for('static', filename='style.css')
    res = request.cookies.get('name_cookie_save')
    user_cookie = judge_cookie(res)
    try:
        if user_cookie:
            return redirect('/up')
        else:
            if request.method=='GET':
                return render_template('login.html',mycss=mycss)
            if request.method=='POST':
                req_name = request.form.get('user_name')
                req_pwd = request.form.get('user_pwd')
                try:
                    if judge_user(req_name,req_pwd):
                        resp = make_response(render_template('upload.html',mycss=mycss))
                        r = random_cookie()
                        resp.set_cookie('name_cookie_save',r)
                        new_cookie(req_name,r)
                        return resp
                    else:
                        return render_template('login.html',mycss=mycss,errMsg = '用户不存在或密码有误')
                except:
                   # return render_template('login.html',mycss=mycss,errMsg = '用户不存在或密码有误')
                    pass
    finally:
        pass


@app.route('/uploadfile', methods=['POST','get'])
def upload():
    res = request.cookies.get('name_cookie_save')
    try:
        if judge_cookie(res):
            if request.method=='GET':
                return '<h3>get 222 </h3>'
            if request.method=='POST':
                relativepath='./uploadfile/'
                upfilename=request.form['upfilename']
                f=request.files['file']
                fname=f.filename
                for i in range(len(fname)):
                    if fname[i] in r'!@#$%^&*+|\=-,/?><";’' or fname[i] in r':][}{￥……、。，？》《“：}{】【‘；':
                        return render_template('uploadfile_ok.html',file_msg =  'upload failed : '+fname[i]+', change file name')
                file_exit = getfile()
                if fname in file_exit:
                    return render_template('uploadfile_ok.html',file_msg =  fname + ' exited, upload failed, change file name')
                f.save(os.path.join(relativepath,fname))
                print(upfilename)
                print(fname)
                return render_template('uploadfile_ok.html',file_msg = 'upload OK : ' + fname)
        else:
            return redirect('/login')
    finally:
        pass

#显示上传页面 同时也是主页面
@app.route('/up', methods=['POST','get'])
def up():
    mycss=url_for('static', filename='style.css')
    res = request.cookies.get('name_cookie_save')
    try:
        user = judge_cookie(res)
        if user:
            return render_template('upload.html',mycss=mycss,user = user)
        else:
            return redirect('/login')
    except:
        pass



@app.route('/file', methods=['POST','get'])
def file():
    mycss=url_for('static', filename='style.css')
    return redirect('/')


@app.route('/down', methods=['GET'])
def downloadpage():
    mycss=url_for('static', filename='style.css')
    res = request.cookies.get('name_cookie_save')
    try:
        user = judge_cookie(res)
        if user:
            flist=getfile()
            print(flist)
            return render_template('downloadpage.html',mycss=mycss,fl=flist,user = user)
        else:
            return redirect('/login')
    except:
        pass        


#下载要下载的文件，要下载的文件是通过get方法来传递的
@app.route('/downloadfile', methods=['GET'])
def downloadfile():
    res = request.cookies.get('name_cookie_save')
    try:
        if judge_cookie(res):
            if request.method=='GET':
                downloadfilename=request.args.get('filename')
                flist=getfile()
                print ()
                if isHavefile(downloadfilename):
                    resp_file = make_response(send_from_directory('uploadfile',downloadfilename,as_attachment=True))
                    resp_file.headers["Content-Disposition"] = "attachment; filename={}".format(downloadfilename.encode().decode('latin-1'))
                    return send_from_directory('uploadfile',downloadfilename,as_attachment=True)
                else:
                    abort(404)
        else:
            return redirect('/login')
    except:
        pass        

if __name__ == '__main__':
    app.run(host = '0.0.0.0',port=5003,debug=True)
