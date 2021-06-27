# coding=UTF-8
import MySQLdb

class MyDefSQL:
    '''自定义python-MySQL连接类'''

    def __init__(self, user, passwd, server_addr, dbname):
        '''初始化'''
        self.user = user
        self.passwd = passwd
        self.server_addr = server_addr
        self.dbname = dbname

    def login(self):
        '''打开数据库连接'''
        err = 0
        try:
            self.conn = MySQLdb.connect(self.server_addr, self.user, self.passwd, self.dbname, charset = "utf8")
        except MySQLdb.Error as e:
            # print(e[0])
            err = e[0]
            self.conn = None
        err = str(err)
        return err

    def execute(self, sql):
        '''执行一条语句sql'''
        # 使用cursor()方法获取操作游标（保存当前操作的结果状态）
        cursor = self.conn.cursor()
        data = None
        err = 0
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            self.conn.commit()
            # 使用fetchall()方法获取所有数据
            data = cursor.fetchall()
        except MySQLdb.Error as e:
            # 回滚
            self.conn.rollback()
            err = e[0]
        err = str(err)
        return [data, err]
        cursor.close()

    def execute_all(self, sqls):
        '''执行一组语句sql'''
        # 使用cursor()方法获取操作游标（保存当前操作的结果状态）
        cursor = self.conn.cursor()
        data = None
        err = 0
        try:
            # 执行所有sql语句
            for sql in sqls:
                cursor.execute(sql)
            # 提交到数据库执行
            self.conn.commit()
            # 使用fetchall()方法获取所有数据
            data = cursor.fetchall()
        except MySQLdb.Error as e:
            # 回滚
            self.conn.rollback()
            err = e[0]
        err = str(err)
        return [data, err]
        cursor.close()

    def call_proc(self, *args):
        '''执行创建好的存储过程'''
        pass


    # 业务逻辑部分
    # table
    def showtablecnt(self):
        '''主页面展示各table的rowcount'''
        tabs = self.execute("show tables")[0]
        res = list()
        for tab in tabs:
            row_cnt = self.execute("select count(*) from " + tab[0])[0]
            res.append((tab[0], row_cnt[0][0]))
        return res

    # customer
    def showcustomer(self):
        '''用户管理'''
        res = self.execute("select * from 客户")[0]
        return res

    def customer_insert(self, data):
        '''单条用户相关信息插入，data是dict型的'''
        # 构造sql语句
        sql = "insert into 客户"
        head = "("
        body = "values ("
        i = 0
        for key,value in data.items():
            # 迭代dict的key和value，方便构造sql语句
            if i:
                head = head + ','
                body = body + ','
            i = i + 1
            head = head + key.encode('utf-8')
            # 需要判断是不是字符串，来加单引号
            if value.isdigit():
                body = body + value.encode('utf-8')
            else:
                body = body + "'" + value.encode('utf-8') + "'"
        head = head + ")"
        body = body + ")"
        sql = sql + ' ' + head + ' ' + body
        print("execute sql is: " + sql)
        # 错误信息
        err = self.execute(sql)[1]
        print("err is: " + err)
        return err

    def customer_update(self, data):
        '''单条用户相关信息修改，data是dict型的'''
        # 构造sql语句
        sql = "update 客户"
        head = "set "
        body = "where 客户身份证号=" + data[u"客户身份证号"].encode('utf-8')
        i = 0
        for key,value in data.items():
            if i:
                head = head + ','
            i = i + 1
            head = head + key.encode('utf-8') + '='
            if value.isdigit():
                head = head + value.encode('utf-8')
            else:
                head = head + "'" + value.encode('utf-8') + "'"
        sql = sql + ' ' + head + ' ' + body
        print("execute sql is: " + sql)
        # 错误信息
        err = self.execute(sql)[1]
        print("err is: " + err)
        return err

    def customer_del(self, data):
        '''单条用户相关信息删除，data是dict型的'''
        # 构造删除语句
        sql = "delete from 客户 where 客户身份证号=" + data[u"客户身份证号"].encode('utf-8')
        # i = 0
        # for key,value in data.items():
        #     if i:
        #         sql = sql + " and"
        #     i = i + 1
        #     sql = sql + ' ' + key.encode('utf-8') + "="
        #     if value.isdigit():
        #         sql = sql + value.encode('utf-8')
        #     else:
        #         sql = sql + "'" + value.encode('utf-8') + "'"
        print("execute sql is: " + sql)
        # 错误信息
        err = self.execute(sql)[1]
        print("err is: " + err)
        return err

    def customer_search(self, searchinfo):
        if len(searchinfo)==0:
            data = self.execute("select * from 客户")[0]
        else:
            sql = "select * from 客户 where"
            i = 0
            for key,value in searchinfo.items():
                if i:
                    sql = sql + ' and'
                sql = sql + ' ' + key.encode('utf-8') + '='
                if value.isdigit():
                    sql = sql + value.encode('utf-8')
                else:
                    sql = sql + "'" + value.encode('utf-8') + "'"
            print("execute sql is: " + sql)
            # 错误信息
            [data,err] = self.execute(sql)
            print("err is: " + err)
        return data

    
    # account，涉及多个表，故采用组合语句的方式
    def showaccount(self, issaving):
        '''账户管理，issaving为True表明是储蓄账户'''
        sql = "select 账户.账户号,支行名称,余额,开户日期,客户身份证号,最近访问日期,"
        if issaving:
            head = "利率,货币类型"
            body = "from 账户,储蓄账户 where 账户.账户号=储蓄账户.账户号"
        else:
            head = "透支额"
            body = "from 账户,支票账户 where 账户.账户号=支票账户.账户号"
        sql = sql + head + ' ' + body
        res = self.execute(sql)[0]
        return res

    def account_insert(self, data, issaving):
        '''单账户开户，data是dict型的；涉及多个表操作，故需要组合查询'''
        # 构造sql语句
        sqls = []
        # 插仅一种账户约束
        sql = "insert into `客户在银行的账户` values ('" + data[u"支行名称"].encode('utf-8') + "','" + data[u"客户身份证号"].encode('utf-8') + "',"
        if issaving:
            sql = sql + "TRUE" + ")"
        else:
            sql = sql + "FALSE" + ")"
        sqls.append(sql)
        # 插账户
        sql = "insert into `账户`"
        head = "("
        body = "values ("
        i = 0
        for key,value in data.items():
            if key.encode('utf-8')=="利率" or key.encode('utf-8')=="货币类型" or key.encode('utf-8')=="透支额":
                continue
            if i:
                head = head + ','
                body = body + ','
            i = i + 1
            head = head + key.encode('utf-8')
            # 时间设置为当前时间
            if key.encode('utf-8')=="开户日期" or key.encode('utf-8')=="最近访问日期":
                body = body + 'CURDATE()'
                continue
            if value.isdigit():
                body = body + value.encode('utf-8')
            else:
                body = body + "'" + value.encode('utf-8') + "'"
        head = head + ")"
        body = body + ")"
        sql = sql + ' ' + head + ' ' + body
        sqls.append(sql)
        # 插具体账户
        if issaving:
            sql = "insert into `储蓄账户` values (" + data[u"账户.账户号"].encode('utf-8') + ',' + data[u"利率"].encode('utf-8') + ",'" + data[u"货币类型"].encode('utf-8') + "')"
        else:
            sql = "insert into `支票账户` values (" + data[u"账户.账户号"].encode('utf-8') + ',' + data[u"透支额"].encode('utf-8') + ")"
        sqls.append(sql)
        # 判断需不需要更新支行资产
        if data[u"余额"]!=u'0':
            # 认为余额为正总代表银行欠用户钱
            pre_assets = self.execute("select 支行资产 from 支行 where 支行名称='" + data[u"支行名称"].encode('utf-8') + "'")[0][0][0]
            new_assets = pre_assets + float(data[u"余额"].encode('utf-8'))
            sql = "update 支行 set 支行资产=" + str(new_assets) + " where 支行名称='" + data[u"支行名称"].encode('utf-8') + "'"
            sqls.append(sql)
        print("execute sql is:")
        for sql in sqls:
            print(sql)
        # 错误信息
        err = self.execute_all(sqls)[1]
        print("err is: " + err)
        return err

    def account_update(self, data, issaving):
        '''单账户相关信息修改，data是dict型的；涉及多个表操作，故需要组合执行'''
        # 构造sql语句
        sqls = []
        # 默认无法更改账户类型、账户号、所在支行、客户身份证号
        # 更改账户，只能修改余额、开户日期、最近访问日期
        sql = "update `账户`"
        head = "set 余额=" + data[u"余额"].encode('utf-8') + ",开户日期='" + data[u"开户日期"].encode('utf-8') + "',最近访问日期=CURDATE()"
        body = "where 账户号=" + data[u"账户.账户号"].encode('utf-8')
        sql = sql + ' ' + head + ' ' + body
        sqls.append(sql)
        # 更改具体账户细则
        if issaving:
            sql = "update `储蓄账户` set 利率=" + data[u"利率"].encode('utf-8') + ",货币类型='" + data[u"货币类型"].encode('utf-8') + "' where 账户号=" + data[u"账户.账户号"].encode('utf-8')
        else:
            sql = "update `储蓄账户` set 透支额=" + data[u"透支额"].encode('utf-8') + " where 账户号=" + data[u"账户.账户号"].encode('utf-8')
        sqls.append(sql)
        # 判断需不需要更新支行资产
        pre_balance = self.execute("select 余额 from 账户 where 账户号=" + data[u"账户.账户号"].encode('utf-8'))[0][0][0]
        if float(data[u"余额"])!=float(pre_balance):
            # 更新了余额，故需要相应更新支行资产
            pre_assets = self.execute("select 支行资产 from 支行 where 支行名称='" + data[u"支行名称"].encode('utf-8') + "'")[0][0][0]
            new_assets = pre_assets + float(data[u"余额"].encode('utf-8')) - float(pre_balance)
            sql = "update 支行 set 支行资产=" + str(new_assets) + " where 支行名称='" + data[u"支行名称"].encode('utf-8') + "'"
            sqls.append(sql)
        print("execute sql is:")
        for sql in sqls:
            print(sql)
        # 错误信息
        err = self.execute_all(sqls)[1]
        print("err is: " + err)
        return err

    def account_del(self, data, issaving):
        '''单账户相关信息删除，data是dict型的；涉及多个表操作，故需要组合执行'''
        # 构造删除语句
        sql = "delete from 客户 where 客户身份证号="
        print("execute sql is: " + sql)
        # 错误信息
        err = self.execute(sql)[1]
        print("err is: " + err)
        return err

    def account_search(self, searchinfo, issaving):
        if len(searchinfo)==0:
            data = self.showaccount(issaving)
        else:
            sql = "select 账户.账户号,支行名称,余额,开户日期,客户身份证号,最近访问日期,"
            if issaving:
                head = "利率,货币类型"
                body = "from 账户,储蓄账户 where 账户.账户号=储蓄账户.账户号"
            else:
                head = "透支额"
                body = "from 账户,支票账户 where 账户.账户号=支票账户.账户号"
            sql = sql + head + ' ' + body
            for key,value in searchinfo.items():
                sql = sql + ' and ' + key.encode('utf-8') + '='
                if value.isdigit():
                    sql = sql + value.encode('utf-8')
                else:
                    sql = sql + "'" + value.encode('utf-8') + "'"
            print("execute sql is: " + sql)
            # 错误信息
            [data,err] = self.execute(sql)
            print("err is: " + err)
        return data



    def __reduce__(self):
        '''关闭连接'''
        if self.conn is not None:
            self.conn.close()
        del self.conn

