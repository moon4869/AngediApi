# from api.menu import *
from api.menu import MenuID, Menu
from api.account import Account, AccountID
from flask import Flask
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

api.add_resource(Menu, '/angedi/menu/', endpoint='menus')
api.add_resource(MenuID, '/angedi/menu/<string:menu_id>', endpoint='menu')

api.add_resource(Account, '/angedi/account/', endpoint='accounts')
api.add_resource(AccountID, '/angedi/account/<string:account_id>', endpoint='account')

if __name__ == '__main__':
    app.run(debug=True)
