# coding=utf-8
import functools

from flask import Flask, session
from flask import redirect
from flask import request, make_response
from flask import render_template
from flask import url_for
from flask_bootstrap import Bootstrap
# 数据库处理
from db import *
# json
import json

# 生成一个app
app = Flask(__name__, instance_relative_config=True)
bootstrap=Bootstrap(app)
app.secret_key = 'lab3'

# 对app执行请求页面地址到函数的绑定
@app.route("/", methods=("GET", "POST"))
@app.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        # 客户端在login页面发起的POST请求
        username = request.form["username"]
        password = request.form["password"]
        ipaddr   = request.form["ipaddr"]
        database = request.form["database"]

        db = MyDefSQL(username, password, ipaddr, database)
        err = db.login()

        if err != '0':
            return render_template("login_fail.html", err=err)
        else:
            #print(err)
            session['username'] = username
            session['password'] = password
            session['ipaddr'] = ipaddr
            session['database'] = database

            return redirect(url_for('home'))
    else :
        # 客户端GET 请求login页面时
        return render_template("login.html")

# 主页面
@app.route("/home", methods=(["GET", "POST"]))
def home():
    return render_template("home.html")


# 请求url为host/table的页面返回结果
@app.route("/table", methods=(["GET", "POST"]))
def table():
    # 出于简单考虑，每次请求都需要连接数据库，可以尝试使用其它context保存数据库连接
    if 'username' in session:
        db = MyDefSQL(session['username'], session['password'], 
                        session['ipaddr'], session['database'])
        err = db.login()
    else:
        return redirect(url_for('login'))
    
    tabs = db.showtablecnt()

    if request.method == "POST":
        if 'clear' in request.form:
            return render_template("table.html", rows = '', dbname=session['database'])
        elif 'search' in request.form:
            return render_template("table.html", rows = tabs, dbname=session['database'])

    else:
        return render_template("table.html", rows = tabs, dbname=session['database'])


# 客户管理页面
@app.route("/customer", methods=(["GET", "POST"]))
def customer():
    if 'username' in session:
        db = MyDefSQL(session['username'], session['password'], 
                        session['ipaddr'], session['database'])
        err = db.login()
    else:
        return redirect(url_for('login'))
    
    tabs = db.showcustomer()
    if tabs==None:
        tabs=""

    if request.method == "POST":
        if 'search' in request.form:
            # 是由search表单提交的post请求
            searchinfo = {}
            # print(len(request.form[u"客户身份证号"]))
            for key,value in request.form.items():
                # 注意这里key和value仍然是unicode编码，统一在db.py中处理！
                if len(value) != 0 and key!='search':
                    # 做第一层过滤，使得可以表单中某块信息不填
                    searchinfo[key] = value
            tabs = db.customer_search(searchinfo)
            return render_template("customer.html", rows = tabs, dbname=session['database'])
        # 其它删改查需求，是由Ajax提交的post
        datas = json.loads(request.get_data(as_text=True))
        function = datas["function"]
        datas = datas["inputdata"]
        # print(function)
        # print(datas[0][u"客户身份证号"])
        if function == "delete":
            res = {'info':'删除成功！', 'errs':[]}
            for data in datas:
                err = db.customer_del(data)
                if err != '0':
                    res['errs'].append([data[u"客户身份证号"],err])
            if len(res['errs']) != 0:
                res['info'] = "删除失败！"
            return json.dumps(res)
        elif function == "insert":
            res = {'info':'插入成功！', 'errs':[]}
            for data in datas:
                err = db.customer_insert(data)
                if err != '0':
                    res['errs'].append([data[u"客户身份证号"],err])
            if len(res['errs']) != 0:
                res['info'] = "插入失败！"
            return json.dumps(res)
        elif function == "update":
            res = {'info':'修改成功！', 'errs':[]}
            for data in datas:
                err = db.customer_update(data)
                if err != '0':
                    res['errs'].append([data[u"客户身份证号"],err])
            if len(res['errs']) != 0:
                res['info'] = "修改失败！"
            return json.dumps(res)

    else:
        return render_template("customer.html", rows = tabs, dbname=session['database'])


# 账户管理页面
# 储蓄账户
@app.route("/account/saving", methods=(["GET", "POST"]))
def saving():
    if 'username' in session:
        db = MyDefSQL(session['username'], session['password'], 
                        session['ipaddr'], session['database'])
        err = db.login()
    else:
        return redirect(url_for('login'))
    
    tabs = db.showaccount(True)
    if tabs==None:
        tabs=""

    if request.method == "POST":
        if 'search' in request.form:
            # 是由search表单提交的post请求
            searchinfo = {}
            for key,value in request.form.items():
                # 注意这里key和value仍然是unicode编码，统一在db.py中处理！
                if len(value) != 0 and key!='search':
                    # 做第一层过滤，使得可以表单中某块信息不填
                    searchinfo[key] = value
            tabs = db.account_search(searchinfo, True)
            return render_template("account_saving.html", rows = tabs, dbname=session['database'])
        # 其它删改查需求，是由Ajax提交的post
        datas = json.loads(request.get_data(as_text=True))
        function = datas["function"]
        datas = datas["inputdata"]
        # print(function)
        if function == "delete":
            res = {'info':'删除成功！', 'errs':[]}
            for data in datas:
                err = db.account_del(data, True)
                if err != '0':
                    res['errs'].append([data[u"账户.账户号"],err])
            if len(res['errs']) != 0:
                res['info'] = "删除失败！"
            return json.dumps(res)
        elif function == "insert":
            res = {'info':'插入成功！', 'errs':[]}
            for data in datas:
                err = db.account_insert(data, True)
                if err != '0':
                    res['errs'].append([data[u"账户.账户号"],err])
            if len(res['errs']) != 0:
                res['info'] = "插入失败！"
            return json.dumps(res)
        elif function == "update":
            res = {'info':'修改成功！', 'errs':[]}
            for data in datas:
                err = db.account_update(data, True)
                if err != '0':
                    res['errs'].append([data[u"账户.账户号"],err])
            if len(res['errs']) != 0:
                res['info'] = "修改失败！"
            return json.dumps(res)

    else:
        return render_template("account_saving.html", rows = tabs, dbname=session['database'])



# 支票账户
@app.route("/account/checking", methods=(["GET", "POST"]))
def checking():
    if 'username' in session:
        db = MyDefSQL(session['username'], session['password'], 
                        session['ipaddr'], session['database'])
        err = db.login()
    else:
        return redirect(url_for('login'))
    
    tabs = db.showaccount(False)
    if tabs==None:
        tabs=""

    if request.method == "POST":
        if 'search' in request.form:
            # 是由search表单提交的post请求
            searchinfo = {}
            for key,value in request.form.items():
                # 注意这里key和value仍然是unicode编码，统一在db.py中处理！
                if len(value) != 0 and key!='search':
                    # 做第一层过滤，使得可以表单中某块信息不填
                    searchinfo[key] = value
            tabs = db.account_search(searchinfo, False)
            return render_template("account_checking.html", rows = tabs, dbname=session['database'])
        # 其它删改查需求，是由Ajax提交的post
        datas = json.loads(request.get_data(as_text=True))
        function = datas["function"]
        datas = datas["inputdata"]
        # print(function)
        if function == "delete":
            res = {'info':'删除成功！', 'errs':[]}
            for data in datas:
                err = db.account_del(data, False)
                if err != '0':
                    res['errs'].append([data[u"账户.账户号"],err])
            if len(res['errs']) != 0:
                res['info'] = "删除失败！"
            return json.dumps(res)
        elif function == "insert":
            res = {'info':'插入成功！', 'errs':[]}
            for data in datas:
                err = db.account_insert(data, False)
                if err != '0':
                    res['errs'].append([data[u"账户.账户号"],err])
            if len(res['errs']) != 0:
                res['info'] = "插入失败！"
            return json.dumps(res)
        elif function == "update":
            res = {'info':'修改成功！', 'errs':[]}
            for data in datas:
                err = db.account_update(data, False)
                if err != '0':
                    res['errs'].append([data[u"账户.账户号"],err])
            if len(res['errs']) != 0:
                res['info'] = "修改失败！"
            return json.dumps(res)

    else:
        return render_template("account_checking.html", rows = tabs, dbname=session['database'])


# 贷款管理页面
@app.route("/loan", methods=(["GET", "POST"]))
def loan():
    if 'username' in session:
        db = MyDefSQL(session['username'], session['password'], 
                        session['ipaddr'], session['database'])
        err = db.login()
    else:
        return redirect(url_for('login'))
    
    tabs = db.showloan()
    if tabs==None:
        tabs=""

    if request.method == "POST":
        if 'search' in request.form:
            # 是由search表单提交的post请求
            searchinfo = {}
            for key,value in request.form.items():
                # 注意这里key和value仍然是unicode编码，统一在db.py中处理！
                if len(value) != 0 and key!='search':
                    # 做第一层过滤，使得可以表单中某块信息不填
                    searchinfo[key] = value
            tabs = db.loan_search(searchinfo)
            return render_template("loan.html", rows = tabs, dbname=session['database'])
        # 其它删改查需求，是由Ajax提交的post
        datas = json.loads(request.get_data(as_text=True))
        function = datas["function"]
        datas = datas["inputdata"]
        # print(function)
        if function == "delete":
            res = {'info':'删除成功！', 'errs':[]}
            for data in datas:
                err = db.loan_del(data)
                if err != '0':
                    res['errs'].append([data[u"客户身份证号"],err])
            if len(res['errs']) != 0:
                res['info'] = "删除失败！"
            return json.dumps(res)
        elif function == "insert":
            res = {'info':'插入成功！', 'errs':[]}
            for data in datas:
                err = db.loan_insert(data)
                if err != '0':
                    res['errs'].append([data[u"客户身份证号"],err])
            if len(res['errs']) != 0:
                res['info'] = "插入失败！"
            return json.dumps(res)
        elif function == "release":
            res = {'info':'贷款发放成功！', 'errs':[]}
            for data in datas:
                err = db.loan_release(data)
                if err != '0':
                    res['errs'].append([data[u"客户身份证号"],err])
            if len(res['errs']) != 0:
                res['info'] = "贷款发放失败！"
            return json.dumps(res)

    else:
        return render_template("loan.html", rows = tabs, dbname=session['database'])



# 测试新html页面
@app.route("/test")
def test():
    if 'username' in session:
        db = MyDefSQL(session['username'], session['password'], 
                        session['ipaddr'], session['database'])
        err = db.login()
    else:
        return redirect(url_for('login'))
    
    tabs = db.showtablecnt()

    return render_template("test.html", rows = tabs)

# 测试URL下返回html page
@app.route("/hello")
def hello():
    return "hello world!"

#返回不存在页面的处理
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")

if __name__ == "__main__":

    app.run(host = "0.0.0.0", debug=True)