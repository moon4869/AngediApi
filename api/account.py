#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from flask import abort, request
from flask_restful import Resource, abort, reqparse
from sql.sql import MSSQL

account = MSSQL(host='localhost', user='', pwd='', db='angedi')


class Account(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('page', type=int)

    # 分页查询以及全部查询
    def get(self):
        page = self.parser.parse_args().get('page')
        if page:
            sql_page = 'SELECT TOP {1} ID,UserID,Name,RoleID,FatherID FROM T_Account ' \
                       'WHERE ID NOT IN (SELECT TOP {0} ID FROM T_Account)'.format(10 * (page - 1), 10)
            results = account.query(sql_page)
            return {"page{}_account".format(page): results}
        else:
            results = account.query('SELECT * FROM T_Account')
            return {"all_account": results}

    def put(self):
        if not request.json:
            abort(400)
        update_account = request.json
        print(update_account)  # 可删除
        pass  # 生成一个ID

        results = account.query('SELECT * FROM T_Account')
        results = list(filter(lambda t: t['ID'] == update_account['ID'], results))
        if len(results) == 0:
            abort(404)  # 数据库内未找到

        values = "ID='{}',UserID='{}',Name='{}',RoleID='{}',FatherID='{}',Psd='{}'". \
            format(update_account['ID'], update_account['UserID'], update_account['Name'], update_account['RoleID'],
                   update_account['FatherID'], update_account['Psd'])
        print(values)
        sql_update = "UPDATE T_Account SET {} WHERE ID='{}'".format(values, update_account['ID'])
        print(sql_update)
        account.update(sql_update)

        if account.flag:  # 判断更新数据库操作是否错误
            account.flag = False
            abort(400)
        return {'result': True}

    def post(self):
        if not request.json:
            abort(400)
        new_account = request.json
        print(new_account)  # 可删除
        pass  # 生成一个ID

        sql_insert = 'INSERT INTO T_Account (ID, FatherID, Name, UserID, Psd, RoleID, Abled, Remark) VALUES '
        values = (new_account['ID'], new_account['FatherID'], new_account['Name'], new_account['UserID'],
                  new_account['Psd'], new_account['RoleID'], new_account['Abled'], new_account['Remark'])
        print(sql_insert + str(values))
        account.insert(sql_insert + str(values))  # 写入数据库
        if account.flag:  # 判断写入数据库操作是否错误
            account.flag = False
            abort(400)
        return {'success': new_account['ID']}


class AccountID(Resource):
    def get(self, account_id):
        results = account.query('SELECT ID,UserID,Name,RoleID,FatherID FROM T_Account')
        results = list(filter(lambda t: t['ID'] == account_id, results))
        if len(results) == 0:
            abort(404)
        return {'one_account': results[0]}

    def delete(self, account_id):
        results = account.query('SELECT * FROM T_Account')
        results = list(filter(lambda t: t['ID'] == account_id, results))
        if len(results) == 0:
            abort(404)  # 数据库内未找到

        # 数据库删除操作
        sql_del = 'DELETE FROM T_Account WHERE ID=' + account_id
        account.delete(sql_del)

        if account.flag:  # 判断删除数据库操作是否错误
            account.flag = False
            abort(400)
        return {'result': True}