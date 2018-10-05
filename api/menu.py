#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from flask import abort, request
from flask_restful import Resource, abort
from sql.sql import MSSQL

menu = MSSQL(host='localhost', user='', pwd='', db='angedi')


class Menu(Resource):
    def get(self):
        results = menu.query('SELECT * FROM T_Menu')
        return {"all_menu": results}

    def post(self):
        if not request.json:
            abort(400)
        new_menu = request.json

        pass  # 生成一个ID

        # 判断是否有父ID,默认无
        sql_insert = 'INSERT INTO T_Menu (ID, Name, Url) VALUES '
        values = (new_menu['ID'], new_menu['Name'], new_menu['Url'])
        if len(new_menu['FatherID']):
            sql_insert = 'INSERT INTO T_Menu (ID, Name, Url, FatherID) VALUES '
            values = (new_menu['ID'], new_menu['Name'], new_menu['Url'], new_menu['FatherID'])
        menu.insert(sql_insert + str(values))  # 写入数据库
        if menu.flag:  # 判断写入数据库操作是否错误
            menu.flag = False
            abort(400)
        return {'success': new_menu['ID']}

    def put(self):
        if not request.json:
            abort(400)
        update_menu = request.json
        pass  # 生成一个ID

        results = menu.query('SELECT * FROM T_Menu')
        results = list(filter(lambda t: t['ID'] == update_menu['ID'], results))
        if len(results) == 0:
            abort(404)  # 数据库内未找到

        values = "ID='{}',Name='{}',Url='{}',FatherID='{}'".format(update_menu['ID'], update_menu['Name'],
                                                                   update_menu['Url'], update_menu['FatherID'])
        sql_update = "UPDATE T_Menu SET {} WHERE ID='{}'".format(values, update_menu['ID'])
        menu.update(sql_update)

        if menu.flag:  # 判断更新数据库操作是否错误
            menu.flag = False
            abort(400)
        return {'result': True}


class MenuID(Resource):
    def get(self, menu_id):
        results = menu.query('SELECT * FROM T_Menu')
        results = list(filter(lambda t: t['ID'] == menu_id, results))
        if len(results) == 0:
            abort(404)
        return {'one_menu': results[0]}

    def delete(self, menu_id):
        results = menu.query('SELECT * FROM T_Menu')
        results = list(filter(lambda t: t['ID'] == menu_id, results))
        if len(results) == 0:
            abort(404)  # 数据库内未找到

        # 数据库删除操作
        sql_del = 'DELETE FROM T_Menu WHERE ID=' + menu_id
        menu.delete(sql_del)

        if menu.flag:  # 判断删除数据库操作是否错误
            menu.flag = False
            abort(400)
        return {'result': True}