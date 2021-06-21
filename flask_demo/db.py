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
        return [data, err]
        cursor.close()

    def call_proc(self, *args):
        '''执行创建好的存储过程'''
        pass

    def showtablecnt(self):
        '''主页面展示各table的rowcount'''
        tabs = self.execute("show tables")[0]
        res = list()
        for tab in tabs:
            row_cnt = self.execute("select count(*) from " + tab[0])[0]
            res.append((tab[0], row_cnt[0][0]))
        return res

    def showcustomer(self):
        '''用户管理'''
        res = self.execute("select * from 客户")[0]
        return res

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
        print("sql is: " + sql)
        # 错误信息
        res = self.execute(sql)
        print(res)
        return res

    def customer_test(self):
        data = self.execute("select * from 客户")
        print(data)
        self.execute("delete from 客户 where 客户身份证号=372301200006110310")



    def __reduce__(self):
        '''关闭连接'''
        if self.conn is not None:
            self.conn.close()
        del self.conn

