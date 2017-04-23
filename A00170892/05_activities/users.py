from flask import Flask, abort, request
from users_commands import get_all_users, add_user, remove_user, get_users_recently_logged, change_password, get_commands_by_user, get_user_info, get_users_by_groupID
import json
import datetime

app = Flask(__name__)
api_url = '/v1.0'

@app.route(api_url+'/users',methods=['POST'])
def create_user():
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

#variacion con parametros ---> users?group=root&lastlog=30&commands
#time = request.args.get("time")
@app.route(api_url+'/users',methods=['GET'])
def read_users():
    respuesta = {};
    group = request.args.get("group")
    lastlog = request.args.get("lastlog")
    comandos = request.args.get("commands")

    if group is None or lastlog is None or comandos is None:
        lista = {}
        lista["users"] = get_all_users()
        return json.dumps(lista), 200
    else:
        x = get_users_by_groupID(group)
        y = get_users_recently_logged(lastlog)
        x = set(x)
        y = set(y)
        users = list(x&y)
        for user in users:
            respuesta[user] = get_commands_by_user(user)

    return json.dumps(respuesta),200

@app.route(api_url+'/users',methods=['DELETE'])
def delete_users():
  error = False
  for username in get_all_users():
    if not remove_user(username):
        error = True

  if error:
    return 'some users were not deleted', 400
  else:
    return 'all users were deleted', 200

#imprime el nombre del usuario
@app.route(api_url+'/users/<string:username>',methods=['GET'])
def read_one_user(username):
    if username not in get_all_users():
        return "el usuario no existe", 400
    else:
        list = get_user_info(username)
        return json.dumps(list), 200


#cambia el password del usuario
@app.route(api_url+'/users/<string:username>',methods=['PUT'])
def update_user(username):
  content = request.get_json(silent=True)
  password = content['password']
  if not password:
    return "se debe especificar un password", 400
  if username not in get_all_users():
    return "el usuario no existe", 400
  if change_password(username,password):
    return "se cambio el password del usuario", 201
  else:
    return "error", 400

#elimina el usuario
@app.route(api_url+'/users/<string:username>',methods=['DELETE'])
def delete_user(username):
    if username not in get_all_users():
        return "el usuario no existe", 400
    else:
        if not remove_user(username):
            return 'el usuario no pudo ser eliminado', 400
        else:
            return 'el usuario fue eliminado', 200


#obtiene los comandos utilizados por un usuario
@app.route(api_url+'/users/<string:username>/commands',methods=['GET'])
def get_commands_one_user(username):
    if username not in get_all_users():
        return "el usuario no existe", 400
    else:
        respuesta = get_commands_by_user(username)
        list = {}
        list["comandos ejecutados"] = respuesta
        return json.dumps(list),200


#recently_logged?time=5
@app.route(api_url+'/users/recently_logged',methods=['GET'])
def read_user_filter():
    list = {}
    respuesta = []
    time = request.args.get("time")
    if time is None:
        respuesta.append("Debe especificar un tiempo en minutos, ej: para 5 minutos --> recently_logged?time=5")
    else:
        respuesta = get_users_recently_logged(time)
        if not respuesta:
            respuesta.append("ningun usuario ingreso en los ultimos " + time + " minutos")

    list["user "] = respuesta
    return json.dumps(list),200



if __name__ == "__main__":
  app.run(host='0.0.0.0',port=5000,debug='True')
