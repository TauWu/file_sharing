
import os
from flask import Flask, render_template, request, send_from_directory, url_for,redirect,jsonify,abort,make_response,config,Blueprint
from module import *
from mysqldb.user_db import *
from mysqldb.cookie_db import *
from mysqldb.file_db import *
import gunicorn
import string

app = Flask(__name__)
app.route

#main页面


@app.route('/')
def hello():
    mycss=url_for('static', filename='style.css')
    res = request.cookies.get('name_cookie_save')
    try:
        if judge_cookie(res):
            return redirect('/uploadfile')
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
            return redirect('/uploadfile')
        else:
            if request.method=='GET':
                return render_template('login.html',mycss=mycss)
            if request.method=='POST':
                req_name = request.form.get('user_name')
                req_pwd = request.form.get('user_pwd')
                try:
                    if judge_user(req_name,req_pwd):
                        resp = make_response(redirect('/uploadfile'))
                        r = random_cookie()
                        resp.set_cookie('name_cookie_save',r)
                        new_cookie(req_name,r)
                        return resp
                    else:
                        return render_template('login.html',mycss=mycss,errMsg = '用户不存在或密码有误')
                except:
                    return render_template('login.html',mycss=mycss,errMsg = '用户不存在或密码有误')
                    pass
    except:
        return render_template('login.html',mycss=mycss,errMsg = '用户不存在或密码有误')
    finally:
        pass


@app.route('/uploadfile', methods=['POST','get'])
def upload():
    mycss=url_for('static', filename='style.css')
    res = request.cookies.get('name_cookie_save')
    try:
        user = judge_cookie(res)
        if user:
            if request.method=='GET':
                try:
                    user = judge_cookie(res)
                    if user:
                        return render_template('upload.html',mycss=mycss,user = user)
                    else:
                        return redirect('/login')
                except:
                    pass
            if request.method=='POST':
                relativepath='./uploadfile/'+user+'/'
                upfilename = ''
                file_msg = ''
                upfilename=request.form['upfilename']
                f=request.files['file']
                fname=f.filename
                for i in range(len(fname)):
                    if fname[i] in r'!@#%$^&\| /' :
                        file_msg = '文件名非法: '+fname[i]+', change file name'
                        return render_template('upload.html',mycss = mycss,user = user, file_msg = file_msg)
                if fname.find('.') == -1:
                    file_msg = '文件名非法,缺少类型, change file name'
                    return render_template('upload.html',mycss = mycss,user = user, file_msg = file_msg)
                file_exit = getfile(user)[0]
                if fname in file_exit:
                    file_msg =  '文件存在: '+fname+' , change file name'
                    return render_template('upload.html',mycss = mycss,user = user, file_msg = file_msg)
                f.save(os.path.join(relativepath,fname))
                print(new_filename(name = user,filename = fname))
                print(upfilename)
                print(fname)
                file_msg =  '保存成功 : ' + fname
                return render_template('upload.html',mycss = mycss,user = user, file_msg = file_msg)
        else:
            return redirect('/login')
    except:
        return render_template('upload.html',mycss=mycss,user = user)





@app.route('/file/', methods=['POST','get'])
def file_page():
    mycss=url_for('static', filename='style.css')
    return redirect('/')



@app.route('/down/',  methods=['POST','get'])
def downloadpage():
    mycss=url_for('static', filename='style.css')
    res = request.cookies.get('name_cookie_save')
    try:
        user = judge_cookie(res)
        if 1:
            flist=getfile()
            fl = []
            for i in range(len(flist[1])):
                if flist[1][i]:
                    fl.append([flist[0][i],flist[1][i][1:]])
                else:
                    fl.append([flist[0][i],'文件夹'])
            print(flist)
            return render_template('downloadpage.html',mycss=mycss,fl=flist[0],user =user)
        else:
            return redirect('/login')
    except:
        pass        


#下载要下载的文件，要下载的文件是通过get方法来传递的
@app.route('/downloadfile/', methods=['GET','post'])
def downloadfile():
    res = request.cookies.get('name_cookie_save')
    downloadfilename=request.args.get('filename')

    try:
        if 1:
            if request.method=='GET':
                print ()
                if isHavefile(downloadfilename):
                    flist=getfile()[0]
                    resp_file = make_response(send_from_directory('uploadfile',downloadfilename,as_attachment=True))
                    return resp_file
                else:
                    return redirect('/userdownloadpage/{}'.format(downloadfilename),code=301)
        else:
            return redirect('/login')
    except:
        pass        

@app.route('/userdownloadpage/<user_name>', methods=['GET'])
def userdownloadpage(user_name):
    mycss=url_for('static', filename='style.css')
    res = request.cookies.get('name_cookie_save')
    try:
        user = judge_cookie(res)
        if 1:
            flist=getfile(user_name)
            fl = []
            for i in range(len(flist[1])):
                if flist[1][i]:
                    fl.append([flist[0][i],flist[1][i][1:]])
                else:
                    fl.append([flist[0][i],'文件夹'])
            print(flist)
            if user_name == user:
                style_in = '"inline"'    
            else :
                style_in = 'display: none'
            return render_template('userdownloadpage.html',mycss=mycss,fl=flist[0],user =user,user_name=user_name,style_in =style_in)
        else:
            return redirect('/login')
    except:
        pass     

@app.route('/userdownloadpage/<user_name>',methods=['post'])
def delete_file(user_name):
    mycss=url_for('static', filename='style.css')
    user = user_name
    try:
        if request.method=='GET':
            return 'wrong try'    
        if request.method=='POST':
            res = request.cookies.get('name_cookie_save')
            user = judge_cookie(res)
            if user:
                file_name = request.form['file_name']
                os.remove('./uploadfile/'+user+'/'+file_name)
                return '''<script type="text/javascript">
    alert("删除{}成功");
    window.history.back()
</script>'''.format(file_name)
    except Exception as e:
        print(e)


if __name__ == '__main__':

    from werkzeug.contrib.fixers import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run(host = '0.0.0.0',port=5003,debug=True)
