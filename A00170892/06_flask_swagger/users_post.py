import json
from flask import Flask, abort, request
from flask_restplus import Resource, Api
from flask_restplus import fields

from users_commands import get_all_users, add_user, remove_user

app = Flask(__name__)
api = Api(app,version='1.0', title='API for users management', description='A demonstration of a Flask RestPlus powered API')

os_user = api.model('User', {
    'username': fields.String(required=True, description='username to be created', example='operativos'),
    'password': fields.String(required=True, description='password for the username', example='mysecurepass'),
})

ns = api.namespace('v1.0/users', description='Operations related to create users')

@ns.route('/')
class UserCollection(Resource):
    @api.response(200, 'List of users successfully returned.')
    def get(self):
        """ returns a list of users """
        list = {}
        list["users"] = get_all_users()
        return json.dumps(list), 200

    @api.response(201, 'User successfully created.')
    @api.response(400, 'User already exist.')
    @api.expect(os_user)
    def post(self):
        """ creates a user """
        content = request.get_json(silent=True)
        username = content['username']
        password = content['password']
        if not username or not password:
            return "empty username or password", 400
        if username in get_all_users():
            return "user already exist", 400
        if add_user(username,password):
            return "user created", 201
        else:
            return "error while creating user", 400

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug='True')
