from flask import Flask
from flask import jsonify
from flask import abort
from flask import make_response
from flask import request
from sql.sql import MSSQL

app = Flask(__name__)
role = MSSQL(host='localhost',user='',pwd='',db='angedi')

@app.errorhandler(404)
def not_found(errror):
    return make_response(jsonify({'error':'Not found'}),404)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/angedi/role/',methonds=['POST'])
def create_one_role():
    if not request.json:
        abort(400)
    new_role = request.json
    print(new_role)
    pass

@app.route('/angedi/role/',methods=['PUT'])
def update_one_role():
    if not request.json:
        abort(400)
    update_role = request.json
    print(update_role)
    pass

    results = role.query('SELECT * FROM T_Role')
    role.conn.close()
    results = list(filter(lambda t:t['ID'] == update_role['ID'],results))
    if len(results) == 0:
        abort(404)

    values = 'ID={},Name={},Url={},SelectedID={}'.format(update_role['ID'],update_role['Name'],update_role['ID'],update_role['SelectesID'])
    print(values)
    sql_update = 'UPDATE T_Role {} WHERE ID={}'.format(values,update_role['ID'])
    print(sql_update)
    role.update(sql_update)

    if role.flag:
        role.flag = False
        abort(400)
    return jsonify({'result':True})

@app.route('/angedi/rale/<string:role_id>',methods=['GET'])
def get_one_role(role_id):
    results = role.query('SELECT * FROM T_Role')
    results = list(filter(lambda t:t['ID'] == role_id,results))
    if len(results) == 0:
        abort(404)
    return jsonify({'one_role':results[0]})

@app.route('/angedi/role/<string:role_id>',methods=['DELETE'])
def delete_one_role(role_id):
    results = role.query('SELECT * FROM T_Role')
    results = list(filter(lambda t:t['ID'] == role.id,results))
    if len(results) == 0:
        abort(404)

    sql_del = 'DELETE FROM T_Role WHERE ID=' + role_id
    role.delete(sql_del)

    if role.flag:
        role.flsg = False
        abort(400)
    return jsonify({'result':True})


if __name__ == '__main__':
    app.run(debug=True)
