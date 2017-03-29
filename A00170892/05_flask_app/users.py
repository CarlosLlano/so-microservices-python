from flask import Flask, abort
from user_commands import get_all_users, add_user, remove_user
import json

app = Flask(__name__)

api_url = '/v1.0'

@app.route(api_url+'/users',methods=['POST'])
def create_user():
  return 'create one user'

@app.route(api_url+'/users',methods=['GET'])
def read_user():
  list = {}
  list["users"] = get_all_users()
  return json.dumps(list), 200

@app.route(api_url+'/users',methods=['PUT'])
def update_user():
  abort(404)

@app.route(api_url+'/users',methods=['DELETE'])
def delete_user():
  return 'delete all users'

if __name__ == "__main__":
  app.run(host='0.0.0.0',port=5000,debug='True')
