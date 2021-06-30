# coding=UTF-8
import MySQLdb
from util import *

# 注意：jinja2模板只支持Unicode或ASCII码，所以需要转换到数据库支持的字符集，再执行sql语句

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
        '''单账户开户，data是dict型的；涉及多个表操作互相影响，故需要组合查询'''
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
            if new_assets<0:
                return '-1'
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
        '''单账户相关信息修改，data是dict型的；涉及多个表操作互相影响，故需要组合执行'''
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
            sql = "update `支票账户` set 透支额=" + data[u"透支额"].encode('utf-8') + " where 账户号=" + data[u"账户.账户号"].encode('utf-8')
        sqls.append(sql)
        # 判断需不需要更新支行资产
        pre_balance = self.execute("select 余额 from 账户 where 账户号=" + data[u"账户.账户号"].encode('utf-8'))[0][0][0]
        if float(data[u"余额"])!=float(pre_balance):
            # 更新了余额，故需要相应更新支行资产
            pre_assets = self.execute("select 支行资产 from 支行 where 支行名称='" + data[u"支行名称"].encode('utf-8') + "'")[0][0][0]
            new_assets = pre_assets + float(data[u"余额"].encode('utf-8')) - float(pre_balance)
            if new_assets<0:
                return '-1'
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
        '''单账户相关信息删除，data是dict型的；涉及多个表操作互相影响，故需要组合执行'''
        # 构造sql语句
        sqls = []
        # 删除仅一种账户约束
        sql = "delete from `客户在银行的账户` where 支行名称='" + data[u"支行名称"].encode('utf-8') + "' and 客户身份证号='" + data[u"客户身份证号"].encode('utf-8') + "' and 账户类型="
        if issaving:
            sql = sql + "TRUE"
        else:
            sql = sql + "FALSE"
        sqls.append(sql)
        # 删具体账户细节
        if issaving:
            sql = "delete from `储蓄账户` where 账户号=" + data[u"账户.账户号"].encode('utf-8')
        else:
            sql = "delete from `支票账户` where 账户号=" + data[u"账户.账户号"].encode('utf-8')
        sqls.append(sql)
        # 最后删除账户，因为有外键依赖它（其实组合操作中顺序没区别了就）
        sql = "delete from `账户`"
        head = ""
        body = "where 账户号=" + data[u"账户.账户号"].encode('utf-8')
        sql = sql + ' ' + head + ' ' + body
        sqls.append(sql)
        # 判断需不需要更新支行资产
        pre_balance = self.execute("select 余额 from 账户 where 账户号=" + data[u"账户.账户号"].encode('utf-8'))[0][0][0]
        if float(pre_balance) != 0:
            # 尚有余额，需要在销户时结清
            pre_assets = self.execute("select 支行资产 from 支行 where 支行名称='" + data[u"支行名称"].encode('utf-8') + "'")[0][0][0]
            new_assets = pre_assets - float(pre_balance)
            if new_assets<0:
                return '-1'
            sql = "update 支行 set 支行资产=" + str(new_assets) + " where 支行名称='" + data[u"支行名称"].encode('utf-8') + "'"
            sqls.append(sql)
        print("execute sql is:")
        for sql in sqls:
            print(sql)
        # 错误信息
        err = self.execute_all(sqls)[1]
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



    # 贷款管理
    def showloan(self):
        '''贷款管理'''
        sql = '''select 贷款号,支行名称,客户身份证号,所贷金额,逐次支付情况
                from 贷款
                '''
        datas = self.execute(sql)[0]
        res = []
        for data in datas:
            # 逐个根据付款个数与逐次支付情况，将末尾元素修改为贷款状态
            l = len(data)
            re = list(data)
            count = self.execute("select count(付款码) from 贷款付款 where 贷款号={0}".format(data[0]))[0][0][0]
            if int(count)==0:
                # 未开始发放
                re.append(u'未开始发放')
            elif int(count)<int(re[l-1]):
                # 发放中
                re.append(u'发放中，已发放次数={0}'.format(int(count)))
            else:
                # 已全部发放，需要在下面保证不会大于它
                re.append(u'已全部发放')
            res.append(re)
        return res

    def loan_insert(self, data):
        '''单条贷款相关信息插入，data是dict型的'''
        # 构造sql语句
        sql = "insert into 贷款"
        head = "("
        body = "values ("
        i = 0
        for key,value in data.items():
            # 迭代dict的key和value，方便构造sql语句
            if key.encode('utf-8')=='当前状态':
                # 贷款插入的时候，都是未发放的状态
                continue
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

    def loan_release(self, data):
        '''单条贷款发放'''
        # 已经全部发放的不可继续发放
        count = self.execute("select count(付款码) from 贷款付款 where 贷款号="+data[u"贷款号"].encode('utf-8'))[0][0][0]
        num = self.execute("select 逐次支付情况 from 贷款 where 贷款号=" + data[u"贷款号"].encode('utf-8'))[0][0][0]
        count=int(count)
        num=int(num)
        if count==num:
            return '-3'
        # 查询贷款的所贷金额和逐次支付情况
        sql = "select 所贷金额,逐次支付情况 from 贷款 where 贷款号=" + data[u"贷款号"].encode('utf-8')
        res = self.execute(sql)[0][0]
        release_amount = int(res[0])/int(res[1])  # 单次发放的金额，默认均匀发放
        # print("data is {0}".format(release_amount))
        sqls = []
        # 插入贷款付款
        sql = "insert into 贷款付款 values (" + data[u"贷款号"].encode('utf-8') + ',' + str(count+1) + ',' + 'CURDATE()' + ',' + str(release_amount) + ')'
        sqls.append(sql)
        # 相应修改银行资产
        pre_assets = self.execute("select 支行资产 from 支行 where 支行名称='" + data[u"支行名称"].encode('utf-8') + "'")[0][0][0]
        new_assets = pre_assets - float(release_amount)
        if new_assets<0:
            return '-1'
        sql = "update 支行 set 支行资产=" + str(new_assets) + " where 支行名称='" + data[u"支行名称"].encode('utf-8') + "'"
        sqls.append(sql)
        print("execute sql is:")
        for sql in sqls:
            print(sql)
        # 错误信息
        err = self.execute_all(sqls)[1]
        print("err is: " + err)
        return err

    def loan_del(self, data):
        '''单条贷款相关信息删除，data是dict型的'''
        sqls = []
        # 处于发放中状态的贷款记录不允许删除
        count = self.execute("select count(付款码) from 贷款付款 where 贷款号="+data[u"贷款号"].encode('utf-8'))[0][0][0]
        num = self.execute("select 逐次支付情况 from 贷款 where 贷款号=" + data[u"贷款号"].encode('utf-8'))[0][0][0]
        count=int(count)
        num=int(num)
        if count>0 and count<num:
            return '-2'
        # 删除贷款付款信息
        sql = "delete from 贷款付款 where 贷款号=" + data[u"贷款号"].encode('utf-8')
        sqls.append(sql)
        # 删除贷款信息
        sql = "delete from 贷款 where 贷款号=" + data[u"贷款号"].encode('utf-8')
        sqls.append(sql)
        print("execute sql is:")
        for sql in sqls:
            print(sql)
        # 错误信息
        err = self.execute_all(sqls)[1]
        print("err is: " + err)
        return err

    def loan_search(self, searchinfo):
        if len(searchinfo)==0:
            res = self.showloan()
        else:
            sql = "select 贷款号,支行名称,客户身份证号,所贷金额,逐次支付情况 from 贷款 where"
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
            [datas,err] = self.execute(sql)
            print("err is: " + err)
            res = []
            for data in datas:
                # 逐个根据付款个数与逐次支付情况，将末尾元素修改为贷款状态
                l = len(data)
                re = list(data)
                count = self.execute("select count(付款码) from 贷款付款 where 贷款号={0}".format(data[0]))[0][0][0]
                if int(count)==0:
                    # 未开始发放
                    re.append(u'未开始发放')
                elif int(count)<int(re[l-1]):
                    # 发放中
                    re.append(u'发放中，已发放次数={0}'.format(int(count)))
                else:
                    # 已全部发放，需要在下面保证不会大于它
                    re.append(u'已全部发放')
                res.append(re)
        return res



    # 业务统计
    def statistic_month(self):
        '''返回业务的统计信息，返回dict型，基本全是后端处理；按月'''
        # 获取日期区间
        min_date = self.execute('''select least(date1,date2) from
                                (select min(开户日期) as date1 from 账户) table1,
                                (select min(付款日期) as date2 from 贷款付款) table2
                                ''')[0][0][0]
        max_date = self.execute("select CURDATE()")[0][0][0]
        print("mindate is {0}, maxdate is {1}".format(min_date, max_date))
        # print(type(max_date))
        # 获取所有月份字串list
        between_months = GetBetweenMonth(min_date, max_date)
        res = []
        subbanks = self.execute('''select 支行名称 from 支行''')[0]
        for subbank in subbanks:
            # 对每个支行，逐个取
            re = {}
            re['name'] = subbank[0]
            datas = []
            for month in between_months:
                # 按月份查
                data = []
                data.append(month)
                # 查该月账户开户人次
                sql = "select count(账户号) from 账户 where DATE_FORMAT(开户日期, '%Y-%m' ) = '"+ month +"'"
                print("sql is: "+sql)
                account_num = self.execute(sql)[0][0][0]
                print("res is: {0}".format(account_num))
                data.append(account_num)
                # 查该月贷款发放金额数
                sql = "select sum(付款金额) from 贷款付款 where DATE_FORMAT(付款日期, '%Y-%m' ) = '"+ month +"'"
                print("sql is: "+sql)
                loanrelease_sum = self.execute(sql)[0][0][0]
                if loanrelease_sum==None:
                    loanrelease_sum=0
                print("res is: {0}".format(loanrelease_sum))
                data.append(loanrelease_sum)
                datas.append(data)
            re['data'] = datas
            res.append(re)
        return res
        
                                
        

    def statistic_quarter(self):
        '''返回业务的统计信息，返回dict型，基本全是后端处理；按季度'''
        # 获取日期区间
        min_date = self.execute('''select least(date1,date2) from
                                (select min(开户日期) as date1 from 账户) table1,
                                (select min(付款日期) as date2 from 贷款付款) table2
                                ''')[0][0][0]
        max_date = self.execute("select CURDATE()")[0][0][0]
        print("mindate is {0}, maxdate is {1}".format(min_date, max_date))
        # print(type(max_date))
        # 获取所有季度字串list
        between_quarters = GetBetweenQuarter(min_date, max_date)
        res = []
        subbanks = self.execute('''select 支行名称 from 支行''')[0]
        for subbank in subbanks:
            # 对每个支行，逐个取
            re = {}
            re['name'] = subbank[0]
            datas = []
            for quarter in between_quarters:
                # 按月份查
                data = []
                data.append(quarter)
                # 查该月账户开户人次
                sql = "select count(账户号) from 账户 where concat(DATE_FORMAT(开户日期, '%Y'),'-',QUARTER(开户日期)) = '"+ quarter +"'"
                print("sql is: "+sql)
                account_num = self.execute(sql)[0][0][0]
                print("res is: {0}".format(account_num))
                data.append(account_num)
                # 查该月贷款发放金额数
                sql = "select sum(付款金额) from 贷款付款 where concat(DATE_FORMAT(付款日期, '%Y'),'-',QUARTER(付款日期)) = '"+ quarter +"'"
                print("sql is: "+sql)
                loanrelease_sum = self.execute(sql)[0][0][0]
                if loanrelease_sum==None:
                    loanrelease_sum=0
                print("res is: {0}".format(loanrelease_sum))
                data.append(loanrelease_sum)
                datas.append(data)
            re['data'] = datas
            res.append(re)
        return res

    def statistic_year(self):
        '''返回业务的统计信息，返回dict型，基本全是后端处理；按年'''
        # 获取日期区间
        min_date = self.execute('''select least(date1,date2) from
                                (select min(开户日期) as date1 from 账户) table1,
                                (select min(付款日期) as date2 from 贷款付款) table2
                                ''')[0][0][0]
        max_date = self.execute("select CURDATE()")[0][0][0]
        print("mindate is {0}, maxdate is {1}".format(min_date, max_date))
        # print(type(max_date))
        # 获取所有月份字串list
        between_years = GetBetweenYear(min_date, max_date)
        res = []
        subbanks = self.execute('''select 支行名称 from 支行''')[0]
        for subbank in subbanks:
            # 对每个支行，逐个取
            re = {}
            re['name'] = subbank[0]
            datas = []
            for year in between_years:
                # 按月份查
                data = []
                data.append(year)
                # 查该月账户开户人次
                sql = "select count(账户号) from 账户 where DATE_FORMAT(开户日期, '%Y' ) = '"+ year +"'"
                print("sql is: "+sql)
                account_num = self.execute(sql)[0][0][0]
                print("res is: {0}".format(account_num))
                data.append(account_num)
                # 查该月贷款发放金额数
                sql = "select sum(付款金额) from 贷款付款 where DATE_FORMAT(付款日期, '%Y' ) = '"+ year +"'"
                print("sql is: "+sql)
                loanrelease_sum = self.execute(sql)[0][0][0]
                if loanrelease_sum==None:
                    loanrelease_sum=0
                print("res is: {0}".format(loanrelease_sum))
                data.append(loanrelease_sum)
                datas.append(data)
            re['data'] = datas
            res.append(re)
        return res




    def __reduce__(self):
        '''关闭连接'''
        if self.conn is not None:
            self.conn.close()
        del self.conn

