from flask import Flask, session, render_template, redirect, Blueprint, request, jsonify
from utils.errorResponse import *
import time
from utils.query import querys
ub = Blueprint('user',__name__,url_prefix='/user',template_folder='templates')

@ub.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        request.form = dict(request.form)

        def filter_fns(item):
            return request.form['username'] in item and request.form['password'] in item

        users = querys('select * from user where is_delete = 0', [], 'select')
        login_success = list(filter(filter_fns, users))
        print(login_success)
        if not len(login_success):
            return errorResponse('输入的密码或账号出现问题')

        session['username'] = request.form['username']
        session['user_id'] = login_success[0][0]
        session['createTime'] = login_success[0][-2]
        session['is_admin'] = login_success[0][-3]
        return redirect('/page/home', 301)
    else:
        return render_template('login.html')


# [新增点 8]：新增管理员强制重置他人密码路由
@ub.route('/resetPassword', methods=['POST'])
def resetPassword():
    # 鉴权：只有管理员可重置
    if session.get('is_admin') != 1:
        return jsonify({'code': 403, 'msg': '无权限操作'})

    uid = request.form.get('id')
    if not uid:
        return jsonify({'code': 400, 'msg': '参数错误'})

    # 重置密码为 123456
    querys('update user set password=%s where id=%s', ['123456', uid])
    return jsonify({'code': 200, 'msg': '成功重置为 123456'})


@ub.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        request.form = dict(request.form)
        if request.form['password'] != request.form['passwordCheked']:
            return '两次密码不符'
        else:
            def filter_fn(item):
                return request.form['username'] in item

            users = querys('select * from user', [], 'select')
            filter_list = list(filter(filter_fn, users))
            if len(filter_list):
                return errorResponse('该用户名已被注册')
            else:
                time_tuple = time.localtime(time.time())
                querys('insert into user(username,password,createTime,isDelete) values(%s,%s,%s,0)',
                       [request.form['username'], request.form['password'],
                        str(time_tuple[0]) + '-' + str(time_tuple[1]) + '-' + str(time_tuple[2])])

        return redirect('/user/login', 301)

    else:
        return render_template('register.html')

@ub.route('/logOut',methods=['GET','POST'])
def logOut():
    session.clear()
    return redirect('/user/login')