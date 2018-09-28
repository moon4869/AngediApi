#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import pymssql


class MSSQL:
    def __init__(self, host='localhost', user='', pwd='', db=''):  # 类的构造函数，初始化数据库连接ip或者域名，以及用户名，密码，要连接的数据库名称
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
        self.conn = None
        self.flag = False  # 判断数据库操作中是否有错

    def get_connect(self):  # 得到数据库连接信息函数， 返回: conn.cursor()
        self.conn = pymssql.connect(host=self.host, user=self.user, password=self.pwd, database=self.db, charset='utf8')
        cur = self.conn.cursor(as_dict=True)  # 将数据库连接信息，赋值给cur。
        if not cur:
            raise(NameError, "连接数据库失败")
        else:
            return cur

    # 执行查询语句,返回的是一个包含tuple的list，list的元素是记录行，tuple的元素是每行记录的字段
    def query(self, sql_query):  # 执行Sql语句函数，返回结果
        cur = self.get_connect()   # 获得数据库连接信息
        try:
            cur.execute(sql_query)  # 执行sql语句
            results = cur.fetchall()  # 获取查询的所有记录
        except Exception as q:
            raise q
        finally:
            self.conn.close()  # 关闭连接
        return results  # 返回查询结果

    # 执行插入语句
    def insert(self, sql_insert):
        cur = self.get_connect()  # 获得数据库连接信息
        try:
            cur.execute(sql_insert)
            self.conn.commit()    # 提交
        except Exception as i:
            # 错误回滚
            print('insert error')
            self.flag = True
            self.conn.rollback()
        finally:
            self.conn.close()

    # 执行更新语句
    def update(self, sql_update):
        cur = self.get_connect()  # 获得数据库连接信息
        try:
            cur.execute(sql_update)
            self.conn.commit()    # 提交
        except Exception as u:
            # 错误回滚
            print('update error')
            self.flag = True
            self.conn.rollback()
        finally:
            self.conn.close()

    # 执行删除语句
    def delete(self, sql_delete):
        cur = self.get_connect()  # 获得数据库连接信息
        try:
            cur.execute(sql_delete)
            self.conn.commit()    # 提交
        except Exception as d:
            # 错误回滚
            print('delete error')
            self.flag = True
            self.conn.rollback()
        finally:
            self.conn.close()