#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from flask import Flask
from flask import jsonify
from flask import abort
from flask import make_response
from flask import request
from sql.sql import MSSQL

app = Flask(__name__)
menu = MSSQL(host='localhost', user='', pwd='', db='angedi')


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/angedi/menu/', methods=['GET'])
def get_all_menu():
    results = menu.query('SELECT * FROM T_Menu')
    return jsonify({"all_menu": results})


@app.route('/angedi/menu/<string:menu_id>', methods=['GET'])
def get_one_menu(menu_id):
    results = menu.query('SELECT * FROM T_Menu')
    results = list(filter(lambda t: t['ID'] == menu_id, results))
    if len(results) == 0:
        abort(404)
    return jsonify({'one_menu': results[0]})


@app.route('/angedi/menu/', methods=['POST'])
def create_one_menu():
    if not request.json:
        abort(400)
    new_menu = request.json
    print(new_menu)   # 可删除
    pass  # 生成一个ID

    # 判断是否有父ID,默认无
    sql_insert = 'INSERT INTO T_Menu (ID, Name, Url) VALUES '
    values = (new_menu['ID'], new_menu['Name'], new_menu['Url'])
    if len(new_menu['FatherID']):
        sql_insert = 'INSERT INTO T_Menu (ID, Name, Url, FatherID) VALUES '
        values = (new_menu['ID'], new_menu['Name'], new_menu['Url'])
    menu.insert(sql_insert + str(values))  # 写入数据库
    if menu.flag:  # 判断写入数据库操作是否错误
        menu.flag = False
        abort(400)
    return jsonify({'success': new_menu['ID']})


@app.route('/angedi/menu/', methods=['PUT'])
def update_one_menu():
    if not request.json:
        abort(400)
    update_menu = request.json
    print(update_menu)   # 可删除
    pass  # 生成一个ID

    results = menu.query('SELECT * FROM T_Menu')
    menu.conn.close()
    results = list(filter(lambda t: t['ID'] == update_menu['ID'], results))
    if len(results) == 0:
        abort(404)  # 数据库内未找到

    values = "ID='{}',Name='{}',Url='{}',FatherID='{}'".format(update_menu['ID'], update_menu['Name'], update_menu['Url'], update_menu['FatherID'])
    print(values)
    sql_update = "UPDATE T_Menu SET {} WHERE ID='{}'".format(values, update_menu['ID'])
    print(sql_update)
    menu.update(sql_update)

    if menu.flag:  # 判断更新数据库操作是否错误
        menu.flag = False
        abort(400)
    return jsonify({'result': True})


@app.route('/angedi/menu/<string:menu_id>', methods=['DELETE'])
def delete_one_menu(menu_id):
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
    return jsonify({'result': True})
