from flask import Flask,session,render_template,redirect,request
import re
app = Flask(__name__)
app.secret_key = 'This is a app.secret_Key , You Know ?'

from views.page import page
from views.user import user

# 将蓝图注册到Flask，方便分层管理
app.register_blueprint(page.pb)
app.register_blueprint(user.ub)

# 设置默认路由地址
@app.route('/')
def index():
    return redirect('/user/login')

# 设置静态资源地址
@app.before_request
def before_request():
    pat = re.compile(r'^/static')
    if re.search(pat,request.path):
        return
    if request.path == '/user/login':
        return
    if request.path == '/user/register':
        return
    uname = session.get('username')
    if uname:
        return None

    return redirect('/user/login')

@app.route('/<path:path>')
def catch_all(path):
    return render_template('404.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
