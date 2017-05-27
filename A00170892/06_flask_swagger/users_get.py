import json
from flask import Flask, abort, request
from flask_restplus import Resource, Api

from users_commands import get_all_users, add_user, remove_user

app = Flask(__name__)
api = Api(app,version='1.0', title='API for users management', description='A demonstration of a Flask RestPlus powered API')


ns = api.namespace('v1.0/users',description='Operations related to create users')

@ns.route('/')
class UserCollection(Resource):
    @api.response(200, 'List of users successfully returned.')
    def get(self):
        """ returns a list of users """
        list = {}
        list["users"] = get_all_users()
        return json.dumps(list), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug='True')
